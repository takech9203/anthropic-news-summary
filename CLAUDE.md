# Anthropic News Summary

Anthropic の最新ニュースを収集し、日本語でレポートを作成するプロジェクト。

## プロジェクト概要

このプロジェクトは、Anthropic に関する最新情報を自動的に収集・整理し、日本語の詳細なレポートを生成します。

## 情報ソース

1. **Anthropic News** (https://www.anthropic.com/news)
   - 公式発表、新モデル、研究成果

2. **Claude API Release Notes** (https://platform.claude.com/docs/en/release-notes/overview)
   - API の更新、新機能、SDK の変更

3. **Claude Code Changelog** (https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)
   - Claude Code CLI の更新履歴

## ディレクトリ構造

```
anthropic-news-summary/
├── .claude/
│   └── skills/
│       └── anthropic-news-summary/
│           ├── SKILL.md           # スキル定義
│           ├── report_template.md # レポートテンプレート
│           └── scripts/           # パーサースクリプト
├── reports/                       # 生成されたレポート
│   └── YYYY/
│       └── YYYY-MM-DD-*.md
├── infographic/                   # インフォグラフィック
├── run.py                         # 自動化スクリプト
└── requirements.txt
```

## 使用方法

### 手動実行

```bash
# デフォルト (過去 7 日間)
python run.py

# 期間指定
python run.py --days 14

# カスタムプロンプト
python run.py "Claude API の最新変更をレポートしてください"
```

### 環境変数

| 変数 | 説明 | デフォルト |
|------|------|----------|
| `AWS_REGION` | Bedrock リージョン | us-east-1 |
| `DEBUG` | デバッグモード | 0 |
| `VERBOSE` | 詳細ログ | 0 |

## レポート形式

各レポートは以下の構造を持ちます:

1. **タイトル**: アップデートの要約
2. **メタデータ**: 日付、ソース、カテゴリ
3. **概要**: 1-2 段落での要約
4. **詳細**: 技術的な説明
5. **開発者への影響**: 必要なアクション
6. **関連リンク**: 公式ドキュメント

## 開発

### パーサースクリプト

各ソースに対応したパーサースクリプトがあります:

- `parse_anthropic_news.py`: Anthropic News ページ
- `parse_release_notes.py`: Claude API リリースノート
- `parse_claude_code_changelog.py`: Claude Code Changelog

### スキル定義

`.claude/skills/anthropic-news-summary/SKILL.md` にワークフローが定義されています。

## 注意事項

- レポートは日本語で作成されます
- 重複チェックにより、既存のレポートは再作成されません
- 各ソースへのリクエストは 1 回のみ (レート制限対策)
