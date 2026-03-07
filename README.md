# Anthropic News Summary

Anthropic の最新ニュースを自動収集し、日本語で詳細なレポートを作成するツール。

## 機能

- Anthropic News、Claude API リリースノート、Claude Code Changelog から最新情報を自動収集
- 日本語での詳細なレポート生成
- Mermaid 形式のアーキテクチャ図を自動作成
- GitHub Actions による日次自動実行

## 情報ソース

| ソース | URL | 内容 |
|--------|-----|------|
| Anthropic News | https://www.anthropic.com/news | 公式発表、新モデル |
| Claude API Release Notes | https://platform.claude.com/docs/en/release-notes | API 更新、新機能 |
| Claude Code Changelog | https://github.com/anthropics/claude-code | CLI 更新履歴 |

## GitHub Pages

レポートとインフォグラフィックは GitHub Pages で公開されています。

- **サイト**: https://takech9203.github.io/anthropic-news-summary/
- **レポート**: https://takech9203.github.io/anthropic-news-summary/reports/
- **インフォグラフィック**: https://takech9203.github.io/anthropic-news-summary/infographic/

## セットアップ

CI/CD の詳細なセットアップ手順は [docs/SETUP.md](docs/SETUP.md) を参照してください。

### 必要条件

- Python 3.11+
- AWS アカウント (Bedrock アクセス権限)
- Claude Agent SDK

### インストール

```bash
git clone https://github.com/takech9203/anthropic-news-summary.git
cd anthropic-news-summary
pip install -r requirements.txt
```

### AWS 認証情報の設定

```bash
export AWS_REGION=us-east-1
aws configure
```

## 使用方法

### 手動実行

```bash
# デフォルト (過去 7 日間)
python run.py

# 期間指定
python run.py --days 14

# カスタムプロンプト
python run.py "Claude Opus 4.6 について詳しくレポートしてください"
```

### GitHub Actions

リポジトリの Actions タブから `Daily Anthropic News Report` を手動実行できます。

## 出力

レポートは `reports/YYYY/YYYY-MM-DD-<slug>.md` 形式で保存されます。

### レポート構造

1. **メタデータ**: 日付、ソース、カテゴリ
2. **概要**: 1-2 段落での要約
3. **詳細**: 技術的な説明
4. **開発者への影響**: 必要なアクション
5. **関連リンク**: 公式ドキュメント

## 開発

### プロジェクト構造

```
anthropic-news-summary/
├── .claude/
│   └── skills/
│       └── anthropic-news-summary/
│           ├── SKILL.md
│           ├── report_template.md
│           └── scripts/
├── .github/
│   └── workflows/
│       └── daily-report.yml
├── reports/
├── run.py
└── requirements.txt
```

### パーサースクリプト

- `parse_anthropic_news.py`: Anthropic News ページのパーサー
- `parse_release_notes.py`: Claude API リリースノートのパーサー
- `parse_claude_code_changelog.py`: Claude Code Changelog のパーサー

## ライセンス

MIT License
