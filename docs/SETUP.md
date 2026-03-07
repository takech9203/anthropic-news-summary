# CI/CD セットアップガイド <!-- omit in toc -->

[← README に戻る](../README.md)

このガイドでは、OpenID Connect (OIDC) 認証を使用して GitHub Actions で Anthropic News Summary の自動化を設定する方法を説明する。

- [概要](#概要)
- [前提条件](#前提条件)
- [パート 1: AWS セットアップ](#パート-1-aws-セットアップ)
  - [Amazon Bedrock モデルアクセスを有効化](#amazon-bedrock-モデルアクセスを有効化)
  - [OIDC プロバイダーと IAM ロールを作成](#oidc-プロバイダーと-iam-ロールを作成)
- [パート 2: GitHub リポジトリ設定](#パート-2-github-リポジトリ設定)
  - [ステップ 1: リポジトリシークレットを設定](#ステップ-1-リポジトリシークレットを設定)
  - [ステップ 2: GitHub Pages を有効化](#ステップ-2-github-pages-を有効化)
  - [ステップ 3: ワークフローをテスト](#ステップ-3-ワークフローをテスト)
- [トラブルシューティング](#トラブルシューティング)
  - [よくある問題](#よくある問題)
- [参考資料](#参考資料)


## 概要

GitHub Actions は AWS との OIDC 認証をサポートしており、長期間有効な AWS 認証情報を保存せずに CI/CD パイプラインで IAM ロールを引き受けることができる。これはセキュリティ上推奨されるアプローチである。

```mermaid
sequenceDiagram
    participant GHA as GitHub Actions
    participant IDP as OIDC Provider
    participant AWS as AWS IAM
    participant Bedrock as Amazon Bedrock

    GHA->>IDP: Request OIDC Token
    IDP-->>GHA: OIDC Token
    GHA->>AWS: AssumeRoleWithWebIdentity
    AWS-->>GHA: Temporary Credentials
    GHA->>Bedrock: Invoke Claude Model
    Bedrock-->>GHA: Response
```

## 前提条件

- Amazon Bedrock アクセスが有効な AWS アカウント
- IAM ID プロバイダーとロールを作成する権限
- GitHub リポジトリ

## パート 1: AWS セットアップ

### Amazon Bedrock モデルアクセスを有効化

1. [Amazon Bedrock コンソール](https://console.aws.amazon.com/bedrock/) を開く
2. 左サイドバーで **Model access** に移動
3. **Modify model access** をクリック
4. 以下のモデルへのアクセスを有効化する。
   - `Anthropic Claude Opus 4.5` (または最新の Opus)
   - `Anthropic Claude Sonnet 4.5` (フォールバック用)
5. **Save changes** をクリック

### OIDC プロバイダーと IAM ロールを作成

#### OIDC プロバイダーの作成

**AWS CLI を使用する場合:**

```bash
aws iam create-open-id-connect-provider \
    --url https://token.actions.githubusercontent.com \
    --client-id-list sts.amazonaws.com
```

**AWS コンソールを使用する場合:**

1. [IAM コンソール - Identity providers](https://console.aws.amazon.com/iam/home#/identity_providers) を開く
2. **Add provider** をクリック
3. 以下を設定する。
   - **Provider type**: OpenID Connect
   - **Provider URL**: `https://token.actions.githubusercontent.com`
   - **Audience**: `sts.amazonaws.com`
4. **Get thumbprint** をクリック
5. **Add provider** をクリック

#### IAM ポリシーの作成

1. [IAM コンソール - Policies](https://console.aws.amazon.com/iam/home#/policies) を開く
2. **Create policy** をクリック
3. **JSON** タブを選択し、以下を貼り付ける。

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "BedrockInvokeModel",
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream"
            ],
            "Resource": [
                "arn:aws:bedrock:*:*:inference-profile/global.anthropic.claude-*",
                "arn:aws:bedrock:*::foundation-model/anthropic.claude-*",
                "arn:aws:bedrock:*::foundation-model/us.anthropic.claude-*",
                "arn:aws:bedrock:::foundation-model/anthropic.claude-*"
            ]
        }
    ]
}
```

4. **Next** をクリック
5. ポリシー名を入力 (例: `GitHubActions-AnthropicNewsSummary-BedrockInvoke`)
6. **Create policy** をクリック

#### IAM ロールの作成

1. [IAM コンソール - Roles](https://console.aws.amazon.com/iam/home#/roles) を開き、**Create role** をクリック
2. **Custom trust policy** を選択
3. 以下の信頼ポリシーを貼り付ける (プレースホルダーを置換)。

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Federated": "arn:aws:iam::<AWS_ACCOUNT_ID>:oidc-provider/token.actions.githubusercontent.com"
            },
            "Action": "sts:AssumeRoleWithWebIdentity",
            "Condition": {
                "StringEquals": {
                    "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
                },
                "StringLike": {
                    "token.actions.githubusercontent.com:sub": "repo:<OWNER>/anthropic-news-summary:*"
                }
            }
        }
    ]
}
```

4. **Next** をクリック
5. 先ほど作成したポリシー (`GitHubActions-AnthropicNewsSummary-BedrockInvoke`) を選択
6. **Next** をクリック
7. ロール名を入力 (例: `GitHubActions-AnthropicNewsSummary`)
8. **Create role** をクリック

**置換する値:**

| プレースホルダー | 値 |
|-----------------|-----|
| `<AWS_ACCOUNT_ID>` | AWS アカウント ID (例: `123456789012`) |
| `<OWNER>` | GitHub ユーザー名または組織名 (例: `takech9203`) |

## パート 2: GitHub リポジトリ設定

### ステップ 1: リポジトリシークレットを設定

1. リポジトリ → **Settings** → **Secrets and variables** → **Actions** に移動
2. **Secrets** タブ → **New repository secret** をクリック
3. 以下のシークレットを追加する。

| 名前 | 値 | 説明 |
|------|-----|------|
| `AWS_ROLE_ARN` | `arn:aws:iam::<ACCOUNT_ID>:role/GitHubActions-AnthropicNewsSummary` | IAM ロール ARN |

### ステップ 2: GitHub Pages を有効化

1. リポジトリ → **Settings** → **Pages** に移動
2. **Source** を **GitHub Actions** に設定
3. **Save** をクリック

設定後、以下の URL でサイトが公開される。

- **メインページ**: `https://<OWNER>.github.io/anthropic-news-summary/`
- **レポート**: `https://<OWNER>.github.io/anthropic-news-summary/reports/`
- **インフォグラフィック**: `https://<OWNER>.github.io/anthropic-news-summary/infographic/`

### ステップ 3: ワークフローをテスト

1. リポジトリの **Actions** タブに移動
2. **Daily Anthropic News Report** ワークフローを選択
3. **Run workflow** → **Run workflow** をクリック

## トラブルシューティング

### よくある問題

#### "Not authorized to perform sts:AssumeRoleWithWebIdentity"

以下を確認する。

- 信頼ポリシーの条件がリポジトリパスと正確に一致している
- OIDC プロバイダー URL が一致している (末尾のスラッシュなし)
- Audience が `sts.amazonaws.com` に設定されている

#### Bedrock で "Access denied"

以下を確認する。

- IAM ロールに Bedrock 用ポリシーがアタッチされている
- Bedrock コンソールでモデルアクセスが有効になっている
- サポートされているリージョン (例: `us-east-1`) を使用している

#### GitHub Pages が表示されない

以下を確認する。

- **Settings** → **Pages** で Source が **GitHub Actions** に設定されている
- **Deploy to GitHub Pages** ワークフローが正常に完了している
- `reports/` と `infographic/` ディレクトリにファイルが存在する

#### レポートが生成されない

以下を確認する。

- `run.py` が正しく実行されている
- Claude Agent SDK が正しくインストールされている
- Bedrock へのアクセス権限がある

### OIDC トークンクレームの確認

デバッグ用にワークフローで以下を追加できる。

```yaml
- name: Debug OIDC
  run: |
    echo "Subject: $GITHUB_REPOSITORY:$GITHUB_REF"
```

## 参考資料

### GitHub Actions

- [aws-actions/configure-aws-credentials](https://github.com/aws-actions/configure-aws-credentials) - GitHub Actions で AWS 認証情報を設定するための公式アクション
- [AWS での OpenID Connect の設定](https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services)
- [GitHub Actions のワークフロー構文](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)

### AWS

- [OpenID Connect (OIDC) ID プロバイダーの作成](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc.html)
- [Amazon Bedrock ユーザーガイド](https://docs.aws.amazon.com/bedrock/latest/userguide/)

### Anthropic

- [Claude API ドキュメント](https://docs.anthropic.com/)
- [Claude Agent SDK](https://github.com/anthropics/claude-agent-sdk)
