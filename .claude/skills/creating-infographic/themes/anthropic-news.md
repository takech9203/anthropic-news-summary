# Anthropic News インフォグラフィックテーマ

Anthropic ニュースレポート専用のインフォグラフィックテーマ。Anthropic ブランドカラーを使用し、Claude や Anthropic のアップデート情報をシングルカラムレイアウトで視覚的に表現します。

## ブランドカラー

Anthropic の公式ブランドカラーを基調としたカラーパレット。

```css
:root {
    /* Anthropic Brand Colors */
    --anthropic-coral: #D4A574;        /* メインアクセント */
    --anthropic-dark: #1a1a2e;         /* ダーク背景 */
    --anthropic-light: #FFF8F0;        /* ライト背景 */
    --anthropic-cream: #F5EDE4;        /* セカンダリ背景 */

    /* Semantic Colors */
    --text-primary: #1a1a2e;
    --text-secondary: #4a4a5a;
    --text-muted: #6a6a7a;
    --success: #10B981;
    --warning: #F59E0B;
    --info: #3B82F6;

    /* Gradients */
    --gradient-header: linear-gradient(135deg, #1a1a2e 0%, #2d2d44 100%);
    --gradient-accent: linear-gradient(135deg, #D4A574 0%, #E8C9A8 100%);
}
```

## 適用条件

以下の場合にこのテーマを使用します。

- `reports/` フォルダ内の Anthropic ニュースレポート (.md) からインフォグラフィックを生成する場合
- ユーザーが「Anthropic ニュースのインフォグラフィック」「レポートを視覚化」などと言った場合

## ファイル名規則

- **形式**: `YYYY-MM-DD-{slug}.html`
- **slug**: レポートファイル名から日付部分を除いた部分を使用
- **例**: `reports/2026/2026-03-07-claude-sonnet-4-6.md` → `infographic/2026-03-07-claude-sonnet-4-6.html`
- **出力先**: `infographic/` フォルダ

## コンテンツ構成

### 必須セクション (この順序で配置)

1. **ヘッダー**: タイトル、日付、カテゴリバッジ
2. **概要セクション**: キーポイント + Before/After 比較 (該当する場合)
3. **主要機能セクション**: 3-5 個の機能カード
4. **技術詳細**: アーキテクチャ図、コードサンプル
5. **ユースケース/影響**: 2-3 個のユースケース
6. **フッター**: 出典 URL、関連リンク

### 推奨セクション (情報がある場合は追加)

- **統計情報**: パフォーマンス向上率、数値データ
- **コードサンプル**: Python/TypeScript の実装例
- **API 変更点**: エンドポイント、パラメータの変更
- **料金情報**: コスト比較、料金変更
- **タイムライン**: リリーススケジュール

## CSS テンプレート

```css
@import url('https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@400;500;700&display=swap');

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Zen Maru Gothic', sans-serif;
    background: var(--anthropic-light);
    color: var(--text-primary);
    line-height: 1.7;
}

.container {
    max-width: 900px;
    margin: 0 auto;
    padding: 40px 24px;
}

/* Header */
.header {
    background: var(--gradient-header);
    color: white;
    padding: 48px 32px;
    border-radius: 24px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
}

.header::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -20%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(212, 165, 116, 0.15) 0%, transparent 70%);
    border-radius: 50%;
}

.header-content {
    position: relative;
    z-index: 1;
}

.category-badge {
    display: inline-block;
    background: var(--anthropic-coral);
    color: var(--anthropic-dark);
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 16px;
}

.header h1 {
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 12px;
    line-height: 1.3;
}

.header .date {
    font-size: 14px;
    opacity: 0.8;
}

/* Section */
.section {
    background: white;
    border-radius: 20px;
    padding: 32px;
    margin-bottom: 24px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
    border: 1px solid rgba(212, 165, 116, 0.1);
}

.section-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 12px;
}

.section-title::before {
    content: '';
    width: 4px;
    height: 24px;
    background: var(--anthropic-coral);
    border-radius: 2px;
}

/* Key Points */
.key-points {
    display: grid;
    gap: 16px;
}

.key-point {
    display: flex;
    align-items: flex-start;
    gap: 16px;
    padding: 20px;
    background: var(--anthropic-cream);
    border-radius: 12px;
}

.key-point-icon {
    width: 48px;
    height: 48px;
    background: var(--gradient-accent);
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    flex-shrink: 0;
}

.key-point-content h3 {
    font-size: 1rem;
    font-weight: 700;
    margin-bottom: 6px;
}

.key-point-content p {
    font-size: 14px;
    color: var(--text-secondary);
}

/* Feature Cards */
.feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
}

.feature-card {
    background: linear-gradient(135deg, #FFFFFF 0%, var(--anthropic-cream) 100%);
    border: 2px solid rgba(212, 165, 116, 0.2);
    border-radius: 16px;
    padding: 24px;
    transition: transform 0.2s, box-shadow 0.2s;
}

.feature-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 30px rgba(212, 165, 116, 0.15);
}

.feature-card h3 {
    font-size: 1rem;
    font-weight: 700;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.feature-card p {
    font-size: 14px;
    color: var(--text-secondary);
    line-height: 1.6;
}

/* Before/After Comparison */
.comparison {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
}

@media (max-width: 600px) {
    .comparison {
        grid-template-columns: 1fr;
    }
}

.comparison-card {
    padding: 24px;
    border-radius: 16px;
}

.comparison-card.before {
    background: linear-gradient(135deg, #FEE2E2 0%, #FECACA 100%);
    border: 2px solid #F87171;
}

.comparison-card.after {
    background: linear-gradient(135deg, #D1FAE5 0%, #A7F3D0 100%);
    border: 2px solid #34D399;
}

.comparison-card h4 {
    font-size: 14px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 12px;
}

.comparison-card.before h4 {
    color: #DC2626;
}

.comparison-card.after h4 {
    color: #059669;
}

/* Stats */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 20px;
}

.stat-card {
    background: var(--gradient-header);
    color: white;
    padding: 24px;
    border-radius: 16px;
    text-align: center;
}

.stat-value {
    font-size: 2.5rem;
    font-weight: 700;
    color: var(--anthropic-coral);
    margin-bottom: 8px;
}

.stat-label {
    font-size: 14px;
    opacity: 0.9;
}

/* Code Block */
.code-block {
    background: #1a1a2e;
    border-radius: 12px;
    overflow: hidden;
    margin: 20px 0;
}

.code-header {
    background: #2d2d44;
    padding: 12px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.code-lang {
    color: var(--anthropic-coral);
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
}

.code-title {
    color: #a0a0b0;
    font-size: 12px;
}

.code-block pre {
    margin: 0;
    padding: 0;
}

.code-block code {
    font-family: 'JetBrains Mono', 'Fira Code', monospace;
    font-size: 13px;
    line-height: 1.6;
    padding: 20px !important;
}

/* Use Cases */
.use-case {
    background: linear-gradient(135deg, var(--anthropic-cream) 0%, #FFF8F0 100%);
    border-left: 4px solid var(--anthropic-coral);
    padding: 20px 24px;
    border-radius: 0 12px 12px 0;
    margin-bottom: 16px;
}

.use-case h4 {
    font-size: 1rem;
    font-weight: 700;
    margin-bottom: 8px;
    color: var(--anthropic-dark);
}

.use-case p {
    font-size: 14px;
    color: var(--text-secondary);
}

/* Mermaid */
.mermaid-container {
    background: #FFFFFF;
    border-radius: 12px;
    padding: 24px;
    margin: 20px 0;
    border: 2px solid rgba(212, 165, 116, 0.2);
    overflow-x: auto;
}

.mermaid {
    display: flex;
    justify-content: center;
}

/* Footer */
.footer {
    margin-top: 40px;
    padding: 24px 32px;
    background: var(--anthropic-cream);
    border-radius: 16px;
    font-size: 13px;
    color: var(--text-muted);
}

.footer a {
    color: var(--anthropic-coral);
    text-decoration: none;
    word-break: break-all;
}

.footer a:hover {
    text-decoration: underline;
}

/* Responsive */
@media (max-width: 600px) {
    .header {
        padding: 32px 24px;
    }

    .header h1 {
        font-size: 1.5rem;
    }

    .section {
        padding: 24px;
    }

    .feature-grid {
        grid-template-columns: 1fr;
    }
}
```

## HTML テンプレート

```html
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>タイトル - Anthropic News Summary</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11/build/styles/atom-one-dark.min.css">
    <style>
        /* CSS テンプレートをここに挿入 */
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <header class="header">
            <div class="header-content">
                <span class="category-badge">Claude API</span>
                <h1>タイトル</h1>
                <p class="date">2026-03-07</p>
            </div>
        </header>

        <!-- Key Points -->
        <section class="section">
            <h2 class="section-title">概要</h2>
            <div class="key-points">
                <div class="key-point">
                    <div class="key-point-icon">🚀</div>
                    <div class="key-point-content">
                        <h3>ポイント 1</h3>
                        <p>説明文</p>
                    </div>
                </div>
                <!-- 他のポイント -->
            </div>
        </section>

        <!-- Before/After (該当する場合) -->
        <section class="section">
            <h2 class="section-title">Before / After</h2>
            <div class="comparison">
                <div class="comparison-card before">
                    <h4>Before</h4>
                    <p>変更前の状態</p>
                </div>
                <div class="comparison-card after">
                    <h4>After</h4>
                    <p>変更後の状態</p>
                </div>
            </div>
        </section>

        <!-- Features -->
        <section class="section">
            <h2 class="section-title">主な機能</h2>
            <div class="feature-grid">
                <div class="feature-card">
                    <h3>✨ 機能名</h3>
                    <p>機能の説明</p>
                </div>
                <!-- 他の機能 -->
            </div>
        </section>

        <!-- Stats (数値データがある場合) -->
        <section class="section">
            <h2 class="section-title">数字で見る改善</h2>
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-value">50%</div>
                    <div class="stat-label">パフォーマンス向上</div>
                </div>
                <!-- 他の統計 -->
            </div>
        </section>

        <!-- Code Sample (コードがある場合) -->
        <section class="section">
            <h2 class="section-title">コードサンプル</h2>
            <div class="code-block">
                <div class="code-header">
                    <span class="code-lang">Python</span>
                    <span class="code-title">使用例</span>
                </div>
                <pre><code class="language-python">import anthropic

client = anthropic.Anthropic()
# コード例
</code></pre>
            </div>
        </section>

        <!-- Architecture (Mermaid図がある場合) -->
        <section class="section">
            <h2 class="section-title">アーキテクチャ</h2>
            <div class="mermaid-container">
                <pre class="mermaid">
flowchart TD
    A[Client] --> B[Claude API]
    B --> C[Response]
                </pre>
            </div>
        </section>

        <!-- Use Cases -->
        <section class="section">
            <h2 class="section-title">ユースケース</h2>
            <div class="use-case">
                <h4>ユースケース 1</h4>
                <p>説明</p>
            </div>
        </section>

        <!-- Footer -->
        <footer class="footer">
            <p><strong>出典:</strong> <a href="https://www.anthropic.com/news/..." target="_blank" rel="noopener noreferrer">https://www.anthropic.com/news/...</a></p>
        </footer>
    </div>

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
                background: '#FFFFFF',
                mainBkg: '#FFF8F0'
            }
        });
    </script>
    <script src="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11/build/highlight.min.js"></script>
    <script>hljs.highlightAll();</script>
</body>
</html>
```

## 注意事項

- インフォグラフィックは単一の HTML ファイルで完結させる (Mermaid.js と highlight.js の CDN 読み込みは許可)
- 情報は簡潔に、視覚的に理解しやすく
- 技術的な詳細とユースケースをバランスよく含める
- 収集した情報の出典を明記
- モバイル対応のレスポンシブデザインを維持
