#!/usr/bin/env python3
"""
Anthropic News Summary 自動化スクリプト

Claude Agent SDK (Amazon Bedrock) を使用して anthropic-news-summary スキルを実行します。
GitHub Actions または GitLab CI で毎日自動実行されることを想定しています。

使用方法:
    python run.py                           # デフォルト設定で実行
    python run.py "カスタムプロンプト"       # カスタムプロンプトで実行
    python run.py --prompt "カスタムプロンプト"  # カスタムプロンプト (明示的フラグ)
    python run.py --days 14                 # 過去 14 日間のニュースを取得

環境変数:
    DEBUG=1         デバッグモード (詳細ログ出力)
    VERBOSE=1       詳細モード (タイミング情報出力)
    AWS_REGION      Bedrock の AWS リージョン (デフォルト: us-east-1)
"""

import argparse
import asyncio
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path

import boto3
from claude_agent_sdk import AgentDefinition, ClaudeAgentOptions, query

from claude_agent_sdk.types import (
    AssistantMessage,
    ResultMessage,
    SystemMessage,
    UserMessage,
    TextBlock,
    ToolUseBlock,
)

# =============================================================================
# 設定
# =============================================================================

# 遡って取得する日数のデフォルト値。
DEFAULT_DAYS = 7

# オーケストレーターに渡すデフォルトのプロンプトテンプレート。
DEFAULT_PROMPT_TEMPLATE = (
    "Report Anthropic news from the past {days} days. "
    "Fetch news from Anthropic News page, Claude API release notes, and Claude Code changelog. "
    "Check for duplicates, and delegate report creation to subagents."
)

# モデル設定
PRIMARY_MODEL = "global.anthropic.claude-opus-4-6-v1"
FALLBACK_MODEL = "global.anthropic.claude-sonnet-4-5-20250929-v1:0"

# オーケストレーターと report-generator サブエージェントが使用するツール。
COMMON_TOOLS = [
    "Skill",
    "Read",
    "Write",
    "Edit",
    "MultiEdit",
    "Glob",
    "Grep",
    "Bash",
    "WebFetch",
]


# =============================================================================
# ロギング
# =============================================================================


class Logger:
    """デバッグモードと詳細モードに対応したロガー。"""

    def __init__(self) -> None:
        self.debug = os.environ.get("DEBUG", "").lower() in ("1", "true", "yes")
        self.verbose = os.environ.get("VERBOSE", "").lower() in ("1", "true", "yes") or self.debug
        self.start_time = time.time()
        self.last_timestamp = self.start_time

    def elapsed(self) -> str:
        return f"{time.time() - self.start_time:.1f}s"

    def delta(self) -> str:
        now = time.time()
        delta = now - self.last_timestamp
        self.last_timestamp = now
        return f"+{delta:.1f}s"

    def log(self, message: str, *, level: str = "INFO", force: bool = False) -> None:
        if force or self.verbose:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] [{level}] {message}", flush=True)

    def log_debug(self, message: str) -> None:
        if self.debug:
            self.log(message, level="DEBUG")

    def log_verbose(self, message: str) -> None:
        if self.verbose:
            self.log(message, level="VERBOSE")

    def log_error(self, message: str) -> None:
        self.log(message, level="ERROR", force=True)

    def log_warn(self, message: str) -> None:
        self.log(message, level="WARN", force=True)


logger = Logger()


def print_separator(char: str = "=", length: int = 60) -> None:
    print(char * length)


def get_latest_reports(output_dir: Path, limit: int = 5) -> list[str]:
    """最新のレポートファイルを取得する。"""
    reports = []

    try:
        if not output_dir.exists():
            return reports

        year_dirs = [
            d for d in output_dir.iterdir()
            if d.is_dir() and d.name.isdigit()
        ]
        year_dirs.sort(reverse=True)

        for year_dir in year_dirs:
            for md_file in year_dir.glob("*.md"):
                reports.append({
                    "name": md_file.name,
                    "path": md_file,
                    "mtime": md_file.stat().st_mtime,
                })

        reports.sort(key=lambda x: x["mtime"], reverse=True)
        return [r["name"] for r in reports[:limit]]

    except Exception as e:
        print(f"Warning: Could not read report directory: {e}", file=sys.stderr)
        return []


def generate_reports_index(reports_dir: Path) -> bool:
    """レポートディレクトリのインデックスファイルを生成する。"""
    if not reports_dir.exists():
        return False

    # Collect all reports
    all_reports = []
    for year_dir in sorted(reports_dir.iterdir(), reverse=True):
        if not year_dir.is_dir() or not year_dir.name.isdigit():
            continue
        for md_file in sorted(year_dir.glob("*.md"), reverse=True):
            if md_file.name in ("index.md", "README.md"):
                continue
            # Extract title from file
            try:
                with open(md_file, encoding="utf-8") as f:
                    first_line = f.readline().strip()
                    title = first_line.lstrip("# ") if first_line.startswith("#") else md_file.stem
            except Exception:
                title = md_file.stem

            all_reports.append({
                "path": f"{year_dir.name}/{md_file.name}",
                "title": title,
                "date": md_file.name[:10],
                "year": year_dir.name,
            })

    if not all_reports:
        return False

    # Generate index.md
    index_content = "# Anthropic News Reports\n\n"
    index_content += "Anthropic の最新ニュースレポート一覧\n\n"

    current_year = None
    for report in all_reports:
        if report["year"] != current_year:
            current_year = report["year"]
            index_content += f"\n## {current_year}\n\n"
        index_content += f"- [{report['date']}]({report['path']}) - {report['title']}\n"

    index_path = reports_dir / "index.md"
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(index_content)

    # Copy to README.md
    readme_path = reports_dir / "README.md"
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(index_content)

    print(f"  Updated: {index_path}")
    return True


def is_throttling_error(error: Exception) -> bool:
    """スロットリングエラーかどうかを判定する。"""
    error_str = str(error).lower()
    return any(keyword in error_str for keyword in [
        "throttl",
        "rate limit",
        "too many requests",
        "429",
        "serviceunav",
    ])


async def run_skill(prompt: str | None = None, days: int = DEFAULT_DAYS) -> list[str]:
    """Claude Agent SDK を使って anthropic-news-summary スキルを実行する。"""
    if prompt is None:
        prompt = DEFAULT_PROMPT_TEMPLATE.format(days=days)
    print_separator()
    print("Anthropic News Summary Automation (Subagent Mode)")
    print_separator()
    current_time = datetime.now()
    print(f"Start time: {current_time.isoformat()}")
    print(f"Days to look back: {days}")
    print(f"Prompt: {prompt[:80]}{'...' if len(prompt) > 80 else ''}")
    print()

    prompt_with_context = f"""Current date and time: {current_time.strftime('%Y-%m-%d %H:%M:%S %Z')} (JST)

You are the orchestrator for Anthropic news report generation.

1. Invoke the Skill tool with skill='anthropic-news-summary' to get the workflow
2. Follow the skill workflow to fetch and parse news from all sources
3. DELEGATE: For each news item, use the 'report-generator' subagent via Task tool
   - Batch size: 3 subagents at a time (to avoid Bedrock API rate limits)
   - Wait for each batch to complete before starting the next
   - Add 3-second delay between each task creation within a batch
   - TaskOutput timeout: 600000 (10 minutes)
   - CRITICAL: When you receive TaskOutput, respond with ONLY a one-line confirmation per task.

User's request: {prompt}"""

    if logger.debug:
        print("Logging mode: DEBUG (full details)")
    elif logger.verbose:
        print("Logging mode: VERBOSE (timing + details)")
    else:
        print("Logging mode: NORMAL (set DEBUG=1 or VERBOSE=1 for more details)")
    print()

    aws_region = os.environ.get("AWS_REGION", "us-east-1")

    print("Configuration:")
    print(f"  AWS Region: {aws_region}")
    print(f"  Primary Model: {PRIMARY_MODEL}")
    print(f"  Fallback Model: {FALLBACK_MODEL}")
    print("  Using Bedrock: Yes")
    print()

    project_dir = Path(__file__).parent
    output_dir = project_dir / "reports"

    print(f"  Project directory: {project_dir}")
    print(f"  Output directory: {output_dir}")
    print()

    try:
        print("Verifying AWS credentials...")
        sts_client = boto3.client("sts", region_name=aws_region)
        identity = sts_client.get_caller_identity()
        print(f"  AWS Account: {identity['Account']}")
        print(f"  AWS ARN: {identity['Arn']}")
        print()

        existing_reports = set()
        for md_file in output_dir.rglob("*.md"):
            existing_reports.add(str(md_file.relative_to(project_dir)))

        models_to_try = [PRIMARY_MODEL, FALLBACK_MODEL]

        bedrock_env = {
            "CLAUDE_CODE_USE_BEDROCK": "1",
            "AWS_REGION": aws_region,
        }

        report_subagent_prompt = (
            "You are an Anthropic news report generator. "
            "When given a news item and output file path:\n"
            "1. Invoke the Skill tool with skill='anthropic-news-summary'\n"
            "2. Follow the skill's workflow to create the report\n"
            "3. Save to the specified output path"
        )

        for model_index, current_model in enumerate(models_to_try):
            print(f"Executing with model: {current_model}")
            print()
            print("Progress:", end="", flush=True)

            stderr_lines: list[str] = []

            def _on_stderr(line: str) -> None:
                stderr_lines.append(line)
                if logger.debug:
                    print(f"  [CLI stderr] {line[:200]}", flush=True)

            options = ClaudeAgentOptions(
                model=current_model,
                fallback_model=(
                    FALLBACK_MODEL
                    if current_model == PRIMARY_MODEL
                    else None
                ),
                env=bedrock_env,
                cwd=str(project_dir),
                setting_sources=["project"],
                allowed_tools=COMMON_TOOLS + ["Task"],
                agents={
                    "report-generator": AgentDefinition(
                        description="Generate a report from a news item.",
                        prompt=report_subagent_prompt,
                        tools=COMMON_TOOLS,
                    ),
                },
                stderr=_on_stderr,
            )

            result_text = ""
            report_count = 0
            created_reports: list[str] = []
            skipped_reports: list[str] = []
            msg_count = 0

            logger.log_verbose(f"Starting query execution at {logger.elapsed()}")

            try:
                async for message in query(prompt=prompt_with_context, options=options):
                    msg_count += 1

                    if isinstance(message, AssistantMessage):
                        content = getattr(message, "content", [])
                        for block in content if isinstance(content, list) else []:
                            if isinstance(block, TextBlock):
                                result_text += block.text
                                text_lower = block.text.lower()
                                if "skip" in text_lower or "duplicate" in text_lower:
                                    print("s", end="", flush=True)

                            elif isinstance(block, ToolUseBlock):
                                tool_name = block.name
                                if tool_name == "Write":
                                    tool_input = block.input if hasattr(block, "input") else {}
                                    file_path = tool_input.get("file_path", "")
                                    if file_path.endswith(".md") and "reports/" in file_path:
                                        report_count += 1
                                        created_reports.append(file_path)
                                        print("w", end="", flush=True)
                                elif tool_name == "Task":
                                    print("T", end="", flush=True)
                                elif tool_name == "Skill":
                                    print("S", end="", flush=True)
                                elif tool_name == "WebFetch":
                                    print("F", end="", flush=True)
                                elif tool_name == "Bash":
                                    print("B", end="", flush=True)
                                else:
                                    print(".", end="", flush=True)

                    elif isinstance(message, ResultMessage):
                        print()
                        logger.log_verbose(f"Received ResultMessage at {logger.elapsed()}")

                print()
                print()
                print_separator("-")
                print("Execution completed")
                print_separator("-")
                print(f"Total messages processed: {msg_count}")
                print(f"Reports created: {report_count}")

                if created_reports:
                    print("\nCreated reports:")
                    for r in created_reports[:10]:
                        print(f"  - {r}")
                    if len(created_reports) > 10:
                        print(f"  ... and {len(created_reports) - 10} more")

                # Generate index
                if output_dir.exists():
                    print("\nGenerating index files...")
                    generate_reports_index(output_dir)

                return created_reports

            except Exception as e:
                print()
                logger.log_error(f"Error during execution: {e}")

                if is_throttling_error(e) and model_index < len(models_to_try) - 1:
                    logger.log_warn(f"Throttling detected, retrying with fallback model...")
                    continue
                else:
                    raise

    except Exception as e:
        logger.log_error(f"Fatal error: {e}")
        raise


def main():
    parser = argparse.ArgumentParser(
        description="Anthropic News Summary automation script"
    )
    parser.add_argument(
        "prompt",
        nargs="?",
        default=None,
        help="Custom prompt for the skill"
    )
    parser.add_argument(
        "--prompt", "-p",
        dest="prompt_flag",
        default=None,
        help="Custom prompt (alternative syntax)"
    )
    parser.add_argument(
        "--days", "-d",
        type=int,
        default=DEFAULT_DAYS,
        help=f"Number of days to look back (default: {DEFAULT_DAYS})"
    )

    args = parser.parse_args()

    prompt = args.prompt_flag or args.prompt

    try:
        created_reports = asyncio.run(run_skill(prompt=prompt, days=args.days))
        print_separator()
        if created_reports:
            print(f"Success! Created {len(created_reports)} report(s)")
        else:
            print("No new reports created (all items may have been duplicates)")
        print_separator()
        sys.exit(0)
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        sys.exit(130)
    except Exception as e:
        print_separator()
        print(f"Error: {e}")
        print_separator()
        sys.exit(1)


if __name__ == "__main__":
    main()
