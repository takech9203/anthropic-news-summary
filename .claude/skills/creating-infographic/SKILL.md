---
name: creating-infographic
description: グラフィックレコーディング風の HTML インフォグラフィックを生成するスキル。手書き風のビジュアル要素、日本語フォント、カラフルな配色を使用して、テキストコンテンツを視覚的に魅力的なインフォグラフィックに変換します。
---

# グラフィックレコーディング風インフォグラフィック変換

## 目的

テキストコンテンツを、超一流デザイナーが作成したような日本語グラフィックレコーディング風 HTML インフォグラフィックに変換します。情報設計とビジュアルデザインの両面で最高水準を目指し、手書き風の図形やアイコンを活用して内容を視覚的に表現します。

## テーマ

Anthropic ブランドカラーを使用したテーマを適用します。

**テーマファイル**: #[[file:themes/anthropic-news.md]]

## グラフィックレコーディング表現技法

インフォグラフィック生成時に適用する表現技法です。

- テキストと視覚要素のバランスを重視
- キーワードを囲み線や色で強調
- 簡易的なアイコンや図形で概念を視覚化
- 数値データは簡潔なグラフや図表で表現
- 接続線や矢印で情報間の関係性を明示
- 余白を効果的に活用して視認性を確保
- 絵文字やアイコンを効果的に配置

## アーキテクチャ図・シーケンス図の活用

インフォグラフィックには、可能な限りアーキテクチャ図やシーケンス図などのビジュアルを含めること。

### 図を含めるべきケース

- **システムアーキテクチャ**: サービス間の連携、データフロー
- **処理フロー**: リクエスト/レスポンスの流れ、ワークフロー
- **Before/After 比較**: アップデート前後の構成変更、改善点の視覚化
- **コンポーネント関係**: サービス間の依存関係
- **シーケンス**: API 呼び出し順序、認証フロー、マルチステップ処理

### ソースに Mermaid 図がある場合

**必須**: ソース (レポート、記事など) に Mermaid 図 (` ```mermaid ` ブロック) が含まれている場合は、**必ず** Mermaid.js で HTML に埋め込むこと。HTML/CSS で独自に図を再作成してはならない。

### Mermaid の実装方法

**重要**: Mermaid 図の背景は必ず白にすること。

```html
<!-- Mermaid.js の読み込み -->
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<script>
    mermaid.initialize({
        startOnLoad: true,
        theme: 'base',
        themeVariables: {
            primaryColor: '#D4A574',
            primaryTextColor: '#1a1a2e',
            primaryBorderColor: '#D4A574',
            lineColor: '#D4A574',
            secondaryColor: '#F5F5F5',
            tertiaryColor: '#FAFAFA',
            background: '#FFFFFF',
            mainBkg: '#FFF8F0',
            nodeBorder: '#D4A574',
            clusterBkg: '#FFF8F0',
            clusterBorder: '#D4A574',
            edgeLabelBackground: '#FFFFFF',
            textColor: '#1a1a2e'
        }
    });
</script>

<!-- Mermaid 図の定義 -->
<div class="mermaid-container">
    <pre class="mermaid">
    flowchart TD
        ...
    </pre>
</div>
```

### Mermaid コンテナのスタイリング

```css
.mermaid-container {
    background: #FFFFFF;
    border-radius: 12px;
    padding: 24px;
    margin: 20px 0;
    border: 2px solid rgba(212, 165, 116, 0.3);
    overflow-x: auto;
}
.mermaid {
    display: flex;
    justify-content: center;
}
```

## コードサンプルの活用

技術的なコンテンツでは、実装例やコードサンプルを含めることを推奨します。

### コードブロックのスタイリング (highlight.js)

```html
<!-- highlight.js の読み込み -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11/build/styles/atom-one-dark.min.css">
<script src="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11/build/highlight.min.js"></script>
<script>hljs.highlightAll();</script>
```

**コードブロックの HTML 構造:**

```html
<div class="code-block">
    <div class="code-header">
        <span class="code-lang">Python</span>
        <span class="code-title">Claude API 呼び出し例</span>
    </div>
    <pre><code class="language-python">import anthropic

client = anthropic.Anthropic()
message = client.messages.create(
    model="claude-sonnet-4-5-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello!"}]
)
print(message.content)</code></pre>
</div>
```

## 全体的な指針

- 読み手が自然に視線を移動できる配置
- 情報の階層と関連性を視覚的に明確化
- 手書き風の要素で親しみやすさを演出
- 視覚的な記憶に残るデザイン
- フッターに出典情報を明記
- 生成した HTML は単一ファイルで完結 (Mermaid.js と highlight.js の CDN 読み込みは許可)

### ストーリー構成

1. **導入**: 何についての話か、なぜ重要かを簡潔に
2. **本題**: 核心となる情報を論理的な順序で展開
3. **まとめ**: 要点の整理、次のアクションや展望

## ソースコンテンツの完全性

**重要**: インフォグラフィックは、ソース (レポート、記事など) の内容を視覚的に表現したものである。ソースの情報を省略せず、全ての内容を含めること。

### 必須ルール

1. **ソースの全セクションを含める**: ソースに含まれるセクションは、原則として全てインフォグラフィックに含める
2. **情報を省略しない**: 視覚的なバランスのために情報を削除してはならない
3. **Mermaid 図はそのまま使用**: ソースに Mermaid 図がある場合は、Mermaid.js でそのまま埋め込む

## 出典 URL の表示

元記事や参照元の URL がある場合は、必ず HTML 内に出典として含めること。

```html
<footer style="margin-top: 24px; padding-top: 16px; border-top: 1px dashed #ccc; font-size: 12px; color: #666;">
  <p>出典: <a href="https://www.anthropic.com/news/..." target="_blank" rel="noopener noreferrer" style="color: #D4A574; text-decoration: underline;">https://www.anthropic.com/news/...</a></p>
</footer>
```

## ファイル名規則

- **形式**: `YYYY-MM-DD-<slug>.html`
- **例**: `2026-03-07-claude-sonnet-4-6.html`
- **出力先**: `infographic/` フォルダ
