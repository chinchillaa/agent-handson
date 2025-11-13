# Azure側の設定手順および設定項目

このドキュメントでは、`agent-handson`プロジェクトで使用するAzureリソースの設定手順をまとめています。

## 📋 目次

- [共通設定](#共通設定)
- [01_multi-llm-reasoning用 Azure設定](#01_multi-llm-reasoning用-azure設定)
- [02_azure-voice-chatbot用 Azure設定](#02_azure-voice-chatbot用-azure設定)
- [コスト管理](#コスト管理)
- [トラブルシューティング](#トラブルシューティング)

---

## 共通設定

両プロジェクトで共通して必要となる設定です。

### Azure CLIのインストール

Azure CLIを使用すると、APIキーなしで認証できます（推奨）。

#### Linuxへのインストール

```bash
# 公式スクリプトを使用
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

#### macOSへのインストール

```bash
# Homebrewを使用
brew update && brew install azure-cli
```

#### Windowsへのインストール

```powershell
# MSIインストーラーをダウンロード
# https://aka.ms/installazurecliwindows
```

### Azure認証

```bash
# Azureにログイン
az login

# ログイン後、ブラウザで認証を完了

# サブスクリプションの確認
az account show

# 使用するサブスクリプションを設定（複数ある場合）
az account set --subscription "サブスクリプション名またはID"
```

### Azureサブスクリプションの確認

```bash
# 利用可能なサブスクリプション一覧
az account list --output table

# 現在のサブスクリプション
az account show --query "{Name:name, ID:id, TenantID:tenantId}" --output table
```

---

## 01_multi-llm-reasoning用 Azure設定

マルチLLM推論システムで使用するAzure OpenAI Serviceの設定手順です。

### 必要なAzureリソース

- **Azure OpenAI Service**: GPT-5/GPT-5-miniモデルのホスティング

### Azure OpenAI Serviceの作成

#### ステップ1: Azure Portalにアクセス

1. https://portal.azure.com にアクセスしてログイン

#### ステップ2: Azure OpenAI Serviceを作成

1. **「リソースの作成」** をクリック
2. 検索ボックスに **「Azure OpenAI」** と入力
3. **「Azure OpenAI」** を選択 → **「作成」** をクリック

#### ステップ3: 基本設定

| 項目 | 設定値 |
|------|--------|
| **サブスクリプション** | 使用するサブスクリプション |
| **リソースグループ** | 新規作成（例: `agent-handson-rg`）または既存 |
| **リージョン** | `Japan East`（推奨）または `East US` |
| **名前** | 任意の名前（例: `agent-handson-openai`） |
| **価格レベル** | `Standard S0` |

4. **「確認および作成」** → **「作成」** をクリック

#### ステップ4: モデルのデプロイメント

リソース作成後、GPT-5とGPT-5-miniをデプロイします。

1. 作成したAzure OpenAIリソースを開く
2. 左メニューから **「モデルのデプロイ」** を選択
3. **「+ モデルのデプロイ」** をクリック

**GPT-5のデプロイ**:
- **モデル**: `gpt-5`
- **デプロイメント名**: `gpt-5`（任意、環境変数で使用）
- **モデルバージョン**: 最新版
- **デプロイメントタイプ**: `Standard`

**GPT-5-miniのデプロイ**:
- **モデル**: `gpt-5-mini`
- **デプロイメント名**: `gpt-5-mini`（任意、環境変数で使用）
- **モデルバージョン**: 最新版
- **デプロイメントタイプ**: `Standard`

#### ステップ5: エンドポイントとキーの取得

1. Azure OpenAIリソースのページを開く
2. 左メニューから **「キーとエンドポイント」** を選択
3. 以下の情報をコピー:
   - **エンドポイント** (例: `https://your-resource.openai.azure.com/`)
   - **キー1** (API Key) - API Key認証を使う場合のみ

### 環境変数の設定

プロジェクトルート（`agent-handson/`）の `.env` ファイルに以下を追加：

```bash
# ========================================
# Azure OpenAI Service 設定
# ========================================

# エンドポイント（必須）
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/

# デプロイメント名（Azure Portalで設定した名前）
AZURE_OPENAI_DEPLOYMENT_GPT5=gpt-5
AZURE_OPENAI_DEPLOYMENT_GPT5_MINI=gpt-5-mini

# ========================================
# 認証方式（以下のいずれか）
# ========================================

# 【方式1】Azure CLI認証（推奨）
# 以下のコマンドを実行後、API Keyの設定は不要
# $ az login

# 【方式2】API Key認証
# Azure Portal から取得したAPI Keyを設定
# AZURE_OPENAI_API_KEY=your_api_key_here
```

### 動作確認

```bash
# 01_multi-llm-reasoningディレクトリで実行
cd 01_multi-llm-reasoning
uv run python main.py "テスト質問"
```

---

## 02_azure-voice-chatbot用 Azure設定

音声対話チャットボットで使用するAzure Speech ServiceとAzure OpenAI Serviceの設定手順です。

### 必要なAzureリソース

- **Azure Speech Service**: 音声認識（Speech-to-Text）と音声合成（Text-to-Speech）
- **Azure OpenAI Service**: GPT-5モデル（01と共通利用可能）

### Azure Speech Serviceの作成

#### ステップ1: Azure Portalにアクセス

1. https://portal.azure.com にアクセスしてログイン

#### ステップ2: Speech Serviceを作成

1. **「リソースの作成」** をクリック
2. **「AI + Machine Learning」** → **「Speech Services」** を選択
3. **「作成」** をクリック

#### ステップ3: 基本設定

| 項目 | 設定値 |
|------|--------|
| **サブスクリプション** | 使用するサブスクリプション |
| **リソースグループ** | 新規作成（例: `voice-chatbot-rg`）または既存 |
| **リージョン** | `Japan East`（推奨）または `East US` |
| **名前** | 任意の名前（例: `voice-chatbot-speech`） |
| **価格レベル** | テスト用: `Free F0`（月5時間まで無料）<br>本格利用: `Standard S0` |

4. **「確認および作成」** → **「作成」** をクリック

#### ステップ4: APIキーとリージョンを取得

1. 作成したSpeech Serviceリソースを開く
2. 左メニューから **「キーとエンドポイント」** を選択
3. 以下の情報をコピー:
   - **キー1** (API Key)
   - **リージョン** (例: `japaneast`)
   - **エンドポイント** (例: `https://japaneast.api.cognitive.microsoft.com/`)

### Azure OpenAI Service

02_azure-voice-chatbotでも Azure OpenAI Service (GPT-5) を使用します。

**オプション1: 01_multi-llm-reasoningと共通のリソースを使用**
- 既に作成済みのAzure OpenAI Serviceリソースを共有
- 追加のデプロイメントは不要（既存のGPT-5を使用）

**オプション2: 新規リソースを作成**
- [01_multi-llm-reasoning用 Azure設定](#01_multi-llm-reasoning用-azure設定)の手順を参照
- GPT-5のみデプロイすればOK（GPT-5-miniは不要）

### 環境変数の設定

プロジェクトルート（`agent-handson/`）の `.env` ファイルに以下を追加：

```bash
# ========================================
# Azure Speech Service 設定
# ========================================

# Speech Service 認証情報
AZURE_SPEECH_API_KEY=your_speech_api_key_here
AZURE_SPEECH_REGION=japaneast

# 音声設定
AZURE_SPEECH_LANGUAGE=ja-JP
AZURE_SPEECH_VOICE_NAME=ja-JP-NanamiNeural

# ========================================
# Azure OpenAI Service 設定（01と共通）
# ========================================
# AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
# AZURE_OPENAI_DEPLOYMENT_GPT5=gpt-5
# （Azure CLI認証の場合、API Keyは不要）
```

### 利用可能な日本語音声（Neural Voice）

Phase 3で5種類の音声プロファイルが使用可能です：

| プロファイル名 | 音声名 | 性別 | 特徴 |
|--------------|--------|------|------|
| **default** | `ja-JP-NanamiNeural` | 女性 | 明るく親しみやすい（標準） |
| **gentle** | `ja-JP-ShioriNeural` | 女性 | 優しく落ち着いた |
| **energetic** | `ja-JP-AoiNeural` | 女性 | 明るく元気な |
| **calm_male** | `ja-JP-KeitaNeural` | 男性 | 落ち着いた声 |
| **friendly_male** | `ja-JP-NaokiNeural` | 男性 | 親しみやすい |

#### その他の利用可能な日本語音声

| 音声名 | 性別 | 特徴 |
|-------|------|------|
| `ja-JP-DaichiNeural` | 男性 | ビジネス向け |
| `ja-JP-MayuNeural` | 女性 | 親しみやすい音声 |

詳細: [Azure Speech Service - 音声ギャラリー](https://learn.microsoft.com/azure/ai-services/speech-service/language-support?tabs=tts#voice-styles-and-roles)

### 認証方法

#### 方法1: APIキー認証（Speech Service）

Speech ServiceはAPIキー認証を使用します（推奨）。

```python
import azure.cognitiveservices.speech as speechsdk

speech_config = speechsdk.SpeechConfig(
    subscription=os.getenv("AZURE_SPEECH_API_KEY"),
    region=os.getenv("AZURE_SPEECH_REGION")
)
```

#### 方法2: Azure CLI認証（OpenAI Service）

Azure OpenAI ServiceはAzure CLI認証が使用できます。

```bash
az login
```

### 動作確認

```bash
# 音声入出力のテスト
cd 02_azure-voice-chatbot
uv run python examples/test_speech.py

# 音声対話の起動
uv run python main.py

# Phase 3機能デモ
uv run python examples/advanced_chat.py
```

---

## コスト管理

### Azure OpenAI Service

**GPT-5モデル**:
- 料金体系: トークンベース課金
- 入力トークン: 約 $X / 1Mトークン（※最新料金はAzure Portalで確認）
- 出力トークン: 約 $Y / 1Mトークン

**GPT-5-miniモデル**:
- 料金体系: トークンベース課金
- GPT-5より低コスト

**コスト削減のヒント**:
- ResearcherエージェントはGPT-5-miniを使用（高速・低コスト）
- 01_multi-llm-reasoningでは役割に応じてモデルを使い分け

### Azure Speech Service

**Speech-to-Text（音声認識）**:
- Standard: 約 ¥120 / 時間
- Free F0: 月5時間まで無料

**Text-to-Speech（音声合成）**:
- Neural Voice: 約 ¥2,000 / 100万文字
- Free F0: 月0.5百万文字まで無料

**料金詳細**:
- [Azure Speech Service 料金](https://azure.microsoft.com/pricing/details/cognitive-services/speech-services/)
- [Azure OpenAI Service 料金](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/)

### Free Tierの活用

テスト・開発時は無料枠を活用できます：

**Speech Service Free F0**:
- Speech-to-Text: 月5時間
- Text-to-Speech (Neural): 月0.5百万文字
- 制限: 同時実行数に制限あり

**注意事項**:
- Free tierは1サブスクリプションあたり1リソースまで
- 本番環境ではStandard S0を推奨

---

## トラブルシューティング

### 共通

#### 環境変数が設定されていない

**エラー**:
```
❌ AZURE_OPENAI_ENDPOINTが設定されていません
```

**解決方法**:
```bash
# .envファイルの確認
cat .env

# プロジェクトルート（agent-handson/）に.envファイルがあるか確認
ls -la | grep .env

# .env.exampleをコピーして.envを作成
cp .env.example .env
```

#### Azure認証エラー

**エラー**:
```
❌ Azure認証エラー
```

**解決方法（Azure CLI認証の場合）**:
```bash
# 再ログイン
az login

# サブスクリプション確認
az account show

# 正しいサブスクリプションを設定
az account set --subscription "サブスクリプション名"
```

**解決方法（API Key認証の場合）**:
```bash
# .envファイルにAPI Keyを追加
nano .env

# 以下を追加
AZURE_OPENAI_API_KEY=your_api_key_here
```

### 01_multi-llm-reasoning

#### モデルが見つからない

**エラー**:
```
❌ Deployment not found: gpt-5
```

**解決方法**:
1. Azure Portalでデプロイメント名を確認
2. `.env`ファイルのデプロイメント名を修正

```bash
# Azure Portalで確認したデプロイメント名を設定
AZURE_OPENAI_DEPLOYMENT_GPT5=実際のデプロイメント名
AZURE_OPENAI_DEPLOYMENT_GPT5_MINI=実際のデプロイメント名
```

#### エンドポイントエラー

**エラー**:
```
❌ Invalid endpoint
```

**解決方法**:
- エンドポイントURLが正しいか確認
- 末尾のスラッシュ（`/`）を含めること

```bash
# 正しい形式
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/

# 間違い（スラッシュなし）
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
```

### 02_azure-voice-chatbot

#### Speech Service認証エラー

**エラー**:
```
❌ Speech Service認証に失敗しました
```

**解決方法**:
```bash
# .envファイルを確認
cat .env | grep AZURE_SPEECH

# API KeyとリージョンがAzure Portalの値と一致しているか確認
# 特にリージョン名に注意（例: "Japan East" → "japaneast"）
```

#### マイクが認識されない

**解決方法**:
- マイクが正しく接続されているか確認
- OSのマイク権限設定を確認
- 他のアプリケーションがマイクを使用していないか確認

#### 音声認識の精度が低い

**解決方法**:
- 静かな環境で使用
- マイクを口に近づける
- バックグラウンドノイズを最小化
- マイクの品質を確認

#### 音声合成エラー

**エラー**:
```
⚠️ 音声合成エラー
```

**解決方法**:
- 音声名が正しいか確認（`ja-JP-NanamiNeural`など）
- リージョンが音声に対応しているか確認
- API制限に達していないか確認

---

## 参考資料

### Azure OpenAI Service
- [Azure OpenAI Service Documentation](https://learn.microsoft.com/azure/ai-services/openai/)
- [Azure OpenAI Quickstart](https://learn.microsoft.com/azure/ai-services/openai/quickstart)
- [GPT-5 Model Documentation](https://learn.microsoft.com/azure/ai-services/openai/concepts/models)

### Azure Speech Service
- [Azure Speech Service Documentation](https://learn.microsoft.com/azure/ai-services/speech-service/)
- [Speech SDK for Python](https://learn.microsoft.com/azure/ai-services/speech-service/quickstarts/setup-platform?pivots=programming-language-python)
- [Speech-to-Text Quickstart](https://learn.microsoft.com/azure/ai-services/speech-service/get-started-speech-to-text)
- [Text-to-Speech Quickstart](https://learn.microsoft.com/azure/ai-services/speech-service/get-started-text-to-speech)
- [音声ギャラリー](https://learn.microsoft.com/azure/ai-services/speech-service/language-support?tabs=tts)

### Azure CLI
- [Azure CLI Documentation](https://learn.microsoft.com/cli/azure/)
- [Azure CLI Install Guide](https://learn.microsoft.com/cli/azure/install-azure-cli)

### その他
- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework)
- [ソフトバンク技術ブログ - Azure Speech Service](https://www.softbank.jp/biz/blog/cloud-technology/articles/202410/azure-speech-service/)

---

**作成日**: 2025-11-13
**最終更新**: 2025-11-13
**バージョン**: 1.0
