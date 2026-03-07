# Project Documentation Guidelines

This file contains guidelines and best practices for creating documentation in this workspace. Claude Code will automatically reference these guidelines when working on documents.

## Project Overview

Anthropic の最新ニュースを収集し、日本語でレポートを作成するプロジェクト。

### 情報ソース

1. **Anthropic News** (https://www.anthropic.com/news)
   - 公式発表、新モデル、研究成果

2. **Claude API Release Notes** (https://platform.claude.com/docs/en/release-notes/overview)
   - API の更新、新機能、SDK の変更

3. **Claude Code Changelog** (https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)
   - Claude Code CLI の更新履歴

### ディレクトリ構造

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

### 使用方法

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

## Document Writing Standards

### General Writing Principles

以下の原則に従ってドキュメントを作成する。

- Use clear, direct language
- Avoid unnecessary jargon or complex terminology
- Write for your audience's level of expertise
- Use active voice when possible
- Keep sentences and paragraphs concise
- Use consistent terminology throughout documents
- Follow established naming conventions
- Write for global audiences and use inclusive language

### Japanese Document Guidelines

**Character Spacing Rules:**

1. **Space Between Japanese and Alphanumeric Characters**: Add one space between Japanese text and alphabetic/numeric characters, except when next to punctuation marks (、。)
   - ✓ Correct: `Claude API`, `4 時間`, `2026 年`, `API 仕様`
   - ✗ Incorrect: `Claude API`, `4時間`, `2026年`, `API仕様`

2. **Hyphenated Terms**: Add spaces around hyphens when connecting Japanese and English terms
   - ✓ Correct: `AI - 人間協働`
   - ✗ Incorrect: `AI-人間協働`

3. **Exception - No Space Next to Punctuation**: Do not add spaces when adjacent to Japanese punctuation marks (、。)
   - ✓ Correct: `Claude、Opus`
   - ✗ Incorrect: `Claude 、Opus`

4. **Exception - No Period in Headings**: Headings should not end with a period (。)
   - ✓ Correct: `# メインタイトル`
   - ✗ Incorrect: `# メインタイトル。`

5. **Bold Labels**: Use colons (:) instead of periods (。) for bold labels followed by explanatory text
   - ✓ Correct: `**システム要件**: 説明文`
   - ✗ Incorrect: `**システム要件**。 説明文`

**Parentheses and Punctuation:**

1. **Use Half-Width Parentheses**: Use `()` instead of `（）` with proper spacing
   - ✓ Correct: `Anthropic (Claude) は`
   - ✗ Incorrect: `Anthropic(Claude)は`

2. **Use Half-Width Colons and Semicolons**: Use `:` and `;` instead of full-width versions

3. **Use Period Before Lists**: In Japanese, use a period (。) instead of colon (:) before lists
   - ✓ Correct: `以下の機能が含まれています。`
   - ✗ Incorrect: `以下の機能が含まれています:`

### Japanese Localization Style Guide

**Basic Principles:**

- 明確で客観的: シンプルで理解しやすい言語を使用
- 正確で具体的: 複雑な構造を最小限に抑え、正確な表現を使用
- 丁寧でプロフェッショナル: 礼儀正しく信頼できるアプローチ

**Avoid:**

- 複雑すぎる言語構造
- スラング、専門用語、インフォーマルな言語
- 否定的な表現
- 曖昧で不明確な表現

**Pronouns:**

- Avoid using personal pronouns when possible
- Use 「お客様」「ユーザー」 instead of 「あなた」
- Use 「当社」「私たち」 instead of 「私たち」 alone

**Numbers and Punctuation:**

- Use half-width Arabic numerals
- Use commas for thousands separator: `1,526,987`
- Use half-width % with no space: `50%`
- For UI elements, use half-width square brackets: `[今すぐサインアップ]`

**Katakana Words:**

- Do not use spaces or middle dots (・) between katakana words
- ✓ Correct: `ブラウザウィンドウ`
- ✗ Incorrect: `ブラウザ ウィンドウ`

## Architecture Diagram Guidelines

### Design Principles

- **Clarity over decoration**: Prioritize readability, minimize visual noise
- **Consistent visual hierarchy**: Use color, size, and position to convey importance
- **Logical grouping**: Group related components using subgraphs/containers
- **Flow direction**: Maintain consistent flow (top-down or left-right)
- **Appropriate abstraction**: Match detail level to audience (executive vs. technical)

### Mermaid (Default)

Use Mermaid unless Draw.io is explicitly requested.

**Syntax:**

- Use `flowchart` instead of `graph`

**Emoji:**

- Use emojis to indicate component types (e.g., `"🤖 Claude"`, `"🗄️ Database"`)

**Layout:**

- Use top-down (TD) flow as default
- Align shapes horizontally within subgraphs
- Group related components in subgraphs with clear boundaries

**Subgraph Layout:**

`direction LR` alone may not align elements horizontally within a subgraph. To ensure horizontal layout, add invisible links (`~~~`) between nodes.

```mermaid
subgraph Models["🤖 Claude Models"]
    direction LR
    Opus["Opus 4.6"]
    Sonnet["Sonnet 4.6"]
    Haiku["Haiku 4.5"]
    Opus ~~~ Sonnet ~~~ Haiku
end
```

**Connection Lines:**

- Solid (`-->`): Data flow, synchronous calls
- Dotted (`-.->`): Logical connection, async, optional
- Use straight lines or 90-degree angles only

**Multi-line Text:**

- Use `<br/>` for line breaks in node labels (better text visibility)
- Do NOT use `\n` for line breaks
- ✓ Correct: `Node["First Line<br/>Second Line"]`
- ✗ Incorrect: `Node["First Line\nSecond Line"]`

**Complexity:**

- Split into multiple diagrams when needed
- Create overview diagram + detailed diagrams for complex systems

**Template:**

```mermaid
flowchart TD
    subgraph Anthropic["🏢 Anthropic"]
        subgraph API["🔌 Claude API"]
            Messages["Messages API"]
            Tools["Tool Use"]
        end
        subgraph Models["🤖 Models"]
            Opus["Opus 4.6"]
            Sonnet["Sonnet 4.6"]
        end
    end

    User(["👤 User"]) --> Messages
    Messages --> Opus
    Messages --> Sonnet
    Opus --> Tools

    classDef company fill:none,stroke:#CCCCCC,stroke-width:2px,color:#666666
    classDef api fill:#FFE0B2,stroke:#FFCC80,stroke-width:2px,color:#5D4037
    classDef model fill:#E8EAF6,stroke:#C5CAE9,stroke-width:2px,color:#283593
    classDef user fill:#E3F2FD,stroke:#BBDEFB,stroke-width:2px,color:#1565C0

    class Anthropic company
    class API,Messages,Tools api
    class Models,Opus,Sonnet model
    class User user
```

**Color Palette:**

Use colors semantically to convey meaning. Stroke color should be slightly darker than fill (not too dark) for visual harmony.

| Purpose | Fill | Stroke | Use Case |
|---------|------|--------|----------|
| Container/Boundary | `none` | `#CCCCCC` | Regions, logical groups |
| General Process | `#FFFFFF` | `#4A90E2` | Standard processing steps |
| Internal/Auto | `#E8F1FF` | `#4A90E2` | Background jobs, internal calls |
| External Input | `#E9F7EC` | `#66BB6A` | User input, external API calls |
| Decision/Branch | `#F3E5F5` | `#7B61FF` | Conditional logic, routing |
| Warning/Attention | `#FFF3E0` | `#FF9800` | Rate limits, potential issues |
| Error/Critical | `#FFEBEE` | `#F44336` | Failure paths, alerts |

**Shape Semantics:**

| Shape | Syntax | Use Case |
|-------|--------|----------|
| Rectangle | `[Name]` | Services, processes |
| Rounded | `(Name)` | Start/end points |
| Stadium | `([Name])` | User actions, triggers |
| Cylinder | `[(Name)]` | Databases, storage |
| Diamond | `{Name}` | Decisions, conditions |
| Hexagon | `{{Name}}` | External systems |

**Diagram Type Selection:**

| Diagram Type | When to Use |
|--------------|-------------|
| `flowchart TD` | System architecture, component relationships |
| `flowchart LR` | Data pipelines, horizontal workflows |
| `sequenceDiagram` | API interactions, request/response flows |
| `stateDiagram-v2` | State machines, lifecycle management |
| `C4Context` | High-level system context (C4 model) |

**Sequence Diagram:**

Use `sequenceDiagram` for interaction flows between participants.

```mermaid
sequenceDiagram
    participant U as 👤 User
    participant A as 🔌 API
    participant M as 🤖 Model

    U->>A: Request
    A->>M: Process
    alt Success
        M-->>A: Response
        A-->>U: Result
    else Error
        M-->>A: Error
        A-->>U: Error Message
    end
```

### Mermaid Diagram Restrictions

**CRITICAL: Sequence Diagrams Do NOT Support Styling**

Mermaid sequence diagrams (`sequenceDiagram`) **do not support** `classDef` and `class` styling commands.

**CRITICAL: Avoid Parentheses in Node Labels**

Mermaid flowcharts have parsing issues with parentheses `()` in node labels, subgraph labels, and link labels.

**Problematic patterns:**

- ✗ `CMK["🔑 キー (CMK)"]` - parentheses in node label
- ✗ `subgraph CrossAccount["🏢 別アカウント (オプション)"]` - parentheses in subgraph label

**Safe patterns:**

- ✓ `CMK["🔑 キー CMK"]` - no parentheses
- ✓ `subgraph CrossAccount["🏢 別アカウント"]` - no parentheses

## Quality Standards

### Mandatory Pre-Publication Checklist (Japanese Documents)

Scan the ENTIRE document for these patterns:

1. Numbers touching Japanese: `1つ` → `1 つ`
2. English touching Japanese: `Claudeが` → `Claude が`
3. Japanese touching numbers: `フェーズ1` → `フェーズ 1`
4. File extensions: `.mdを` → `.md を`
5. Full-width colons: `以下：` → `以下:`
6. Full-width parentheses: `（例）` → `(例)`
7. Periods in headings: `## タイトル。` → `## タイトル`
8. Bold labels with periods: `**ラベル**。 説明` → `**ラベル**: 説明`

**Document is ONLY approved when:**

- Zero violations remain in the entire document
- All formatting is consistent throughout
- Text remains natural and readable

### General Quality Checklist

- [ ] Content follows appropriate language guidelines
- [ ] Spacing rules are correctly applied (Japanese documents)
- [ ] Technical terminology is accurate and consistent
- [ ] All links and references are functional
- [ ] Content is clear and accessible to the target audience
- [ ] Formatting is consistent throughout
- [ ] Diagrams use appropriate colors and styles

## Evidence-Based Approach

**推測で結論を出さない。必ず証拠を収集してから判断・提案する。**

### 適用場面

- 問題やバグの調査
- 解決策の提案
- 設定変更の推奨
- ドキュメントへの情報追記

### 行動プロセス

1. **状況の把握**: 現在の状態と期待される状態の差異を確認
2. **証拠の収集**: ログ、エラーメッセージ、ドキュメント、設定情報を収集
3. **仮説の検証**: 推測を立てたら、必ず実際に確認して検証
4. **提案と実行**: 証拠を明示し、根拠を説明して提案

### 禁止事項

| 禁止 | 正しい対応 |
|------|-----------|
| 証拠なしに原因を断定する | 「可能性があります。確認しましょう」と提案 |
| 推測に基づいて変更を適用する | 原因を特定してから修正を提案 |
| 一般論で結論づける | 実際のデータを確認して検証 |
| 確認せずに推奨する | 現在の状態を確認してから提案 |
| ドキュメントを読まずに記述する | 公式ドキュメントで事実を確認してから記述 |

### 確認すべき質問

- 何が起きているか具体的に把握できているか?
- 関連するログやエラーメッセージを確認したか?
- **公式ドキュメントで事実を確認したか?**
- 推測ではなく、証拠に基づいて判断しているか?
- 提案する変更の影響範囲を理解しているか?

### 例: 正しいアプローチ vs 間違ったアプローチ

**正しいアプローチ:**

- ✓ ドキュメントを WebFetch で取得し、内容を確認してから記述
- ✓ 「ドキュメントによると X です」と根拠を示す
- ✓ 確認できなかった場合は「確認が必要です」と明示

**間違ったアプローチ:**

- ✗ ドキュメントを読まずに「X という機能があります」と記述
- ✗ ユーザーのフィードバックだけで推測し、確認せずに修正
- ✗ 一般的な知識だけで断定的に記述

# currentDate

Today's date is 2026-03-07.

IMPORTANT: this context may or may not be relevant to your tasks. You should not respond to this context unless it is highly relevant to your task.
