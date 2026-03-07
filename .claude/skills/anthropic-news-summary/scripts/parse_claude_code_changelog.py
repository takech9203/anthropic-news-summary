#!/usr/bin/env python3
"""
Claude Code CHANGELOG.md をパースして JSON 形式で出力するスクリプト。

Usage:
    python parse_claude_code_changelog.py --days 7 --feed /tmp/claude_code_changelog.md
    curl -sL "https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md" | python parse_claude_code_changelog.py --days 7
"""

import argparse
import json
import re
import sys
from datetime import datetime, timedelta


def parse_date_string(date_str: str) -> str:
    """様々な日付形式をパースして YYYY-MM-DD 形式に変換する。"""
    # Try ISO format first (2026-03-07)
    if re.match(r"\d{4}-\d{2}-\d{2}", date_str):
        return date_str[:10]

    # Try common formats
    formats = [
        "%B %d, %Y",  # March 7, 2026
        "%b %d, %Y",  # Mar 7, 2026
        "%Y/%m/%d",   # 2026/03/07
    ]

    for fmt in formats:
        try:
            dt = datetime.strptime(date_str.strip(), fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue

    return ""


def extract_changelog_entries(content: str) -> list:
    """CHANGELOG.md をパースしてエントリのリストを返す。"""
    items = []

    # Split by version headers (## 2.1.71 or ## [2.1.69] - 2026-03-06)
    version_pattern = r"##\s+\[?(\d+\.\d+\.\d+)\]?(?:\s*[-–]\s*(\d{4}-\d{2}-\d{2}))?"
    parts = re.split(version_pattern, content)

    # Parts will be: [preamble, version1, date1, content1, version2, date2, content2, ...]
    i = 1
    while i < len(parts):
        version = parts[i] if i < len(parts) else None
        date_str = parts[i + 1] if i + 1 < len(parts) else None
        section_content = parts[i + 2] if i + 2 < len(parts) else ""
        i += 3

        if not version:
            continue

        # Parse date if available
        parsed_date = ""
        if date_str:
            parsed_date = parse_date_string(date_str)

        # If no date in header, try to find it in the content
        if not parsed_date:
            date_match = re.search(r"(\d{4}-\d{2}-\d{2})", section_content[:200])
            if date_match:
                parsed_date = date_match.group(1)

        # If still no date, use today's date for recent versions (assume latest)
        if not parsed_date:
            parsed_date = datetime.now().strftime("%Y-%m-%d")

        # Extract changes by category
        categories = {
            "added": [],
            "changed": [],
            "fixed": [],
            "removed": [],
            "deprecated": [],
            "security": [],
        }

        # Look for category headers
        category_pattern = r"###\s*(Added|Changed|Fixed|Removed|Deprecated|Security)"
        category_parts = re.split(category_pattern, section_content, flags=re.IGNORECASE)

        current_category = "changed"  # Default category
        for j, part in enumerate(category_parts):
            if part.lower() in categories:
                current_category = part.lower()
            else:
                # Extract bullet points
                bullets = re.findall(r"^[-*]\s+(.+?)(?=\n[-*]|\n\n|\n###|$)", part, re.MULTILINE | re.DOTALL)
                for bullet in bullets:
                    text = bullet.strip()
                    text = re.sub(r"\s+", " ", text)
                    if text:
                        categories[current_category].append(text)

        # If no categorized items, try to extract all bullets
        all_changes = []
        for cat, changes in categories.items():
            all_changes.extend(changes)

        if not all_changes:
            # Fallback: extract all bullet points
            bullets = re.findall(r"^[-*]\s+(.+?)(?=\n[-*]|\n\n|\n##|$)", section_content, re.MULTILINE | re.DOTALL)
            all_changes = [b.strip() for b in bullets if b.strip()]

        # Create item for each change
        for change in all_changes:
            # Determine category
            category = "changed"
            change_lower = change.lower()
            if any(kw in change_lower for kw in ["add", "new", "introduce", "launch"]):
                category = "added"
            elif any(kw in change_lower for kw in ["fix", "resolve", "correct", "bug"]):
                category = "fixed"
            elif any(kw in change_lower for kw in ["remove", "delete", "drop"]):
                category = "removed"
            elif any(kw in change_lower for kw in ["deprecate"]):
                category = "deprecated"

            # Create title (first sentence)
            title_match = re.match(r"^(.+?(?:\.|:|\?|!))(?:\s|$)", change)
            if title_match:
                title = title_match.group(1).strip()
            else:
                title = change[:100] + ("..." if len(change) > 100 else "")

            # Remove markdown formatting from title
            title = re.sub(r"\*\*(.+?)\*\*", r"\1", title)
            title = re.sub(r"`(.+?)`", r"\1", title)
            title = re.sub(r"\[(.+?)\]\(.+?\)", r"\1", title)

            items.append({
                "title": title,
                "version": version,
                "date": parsed_date,
                "description": change,
                "category": category,
                "source": "claude-code-changelog",
            })

    return items


def filter_by_days(items: list, days: int) -> list:
    """指定日数以内のアイテムのみをフィルタリングする。"""
    cutoff = datetime.now() - timedelta(days=days)
    filtered = []

    for item in items:
        if not item.get("date"):
            continue
        try:
            item_date = datetime.strptime(item["date"], "%Y-%m-%d")
            if item_date >= cutoff:
                filtered.append(item)
        except ValueError:
            continue

    return filtered


def main():
    parser = argparse.ArgumentParser(description="Parse Claude Code CHANGELOG.md")
    parser.add_argument("--days", type=int, default=7, help="Number of days to look back")
    parser.add_argument("--feed", type=str, help="Path to CHANGELOG.md file (default: stdin)")
    args = parser.parse_args()

    # Read input
    if args.feed:
        with open(args.feed, encoding="utf-8") as f:
            content = f.read()
    else:
        content = sys.stdin.read()

    # Parse changelog
    items = extract_changelog_entries(content)

    # Filter by date
    filtered_items = filter_by_days(items, args.days)

    # Sort by date (newest first)
    filtered_items.sort(key=lambda x: (x.get("date", ""), x.get("version", "")), reverse=True)

    # Output as JSON
    result = {
        "source": "claude-code-changelog",
        "total_items": len(filtered_items),
        "days": args.days,
        "items": filtered_items,
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
