# Azure側の設定手順および設定項目

このドキュメントでは、`agent-handson`プロジェクトで使用するAzureリソースの設定手順をまとめています。

## 📋 目次

- [🎓 ハンズオン参加者向けクイックスタート](#-ハンズオン参加者向けクイックスタート)
- [共通設定](#共通設定)
- [01_multi-llm-reasoning用 Azure設定](#01_multi-llm-reasoning用-azure設定)
- [02_azure-voice-chatbot用 Azure設定](#02_azure-voice-chatbot用-azure設定)
- [コスト管理](#コスト管理)
- [トラブルシューティング](#トラブルシューティング)
- [主催者向けリソース準備ガイド](#主催者向けリソース準備ガイド)

---

## 🎓 ハンズオン参加者向けクイックスタート

**このセクションはハンズオン参加者向けです。主催者から提供されたAPI Keyを使って、5分でセットアップを完了できます。**

### 前提条件

- ✅ Python 3.11以上がインストール済み
- ✅ uvパッケージマネージャーがインストール済み（[インストール方法](https://github.com/astral-sh/uv)）
- ✅ 主催者から配布されたAPI Keyを受領済み

**重要**: Azureアカウントの作成やAzure CLIのインストールは**不要**です！

---

### ⚡ 5分セットアップ手順

#### ステップ1: リポジトリをクローン（1分）

```bash
git clone https://github.com/chinchillaa/agent-handson.git
cd agent-handson
```

#### ステップ2: 環境ファイルを作成（1分）

```bash
# .env.exampleをコピーして.envを作成
cp .env.example .env
```

#### ステップ3: API Keyを設定（2分）

`.env`ファイルをエディタで開き、主催者から配布された値を設定：

```bash
# エディタで開く（お好みのエディタを使用）
nano .env
# または
vim .env
# または
code .env  # VS Code
```

**設定内容**（配布された値に置き換えてください）:

```bash
# ========================================
# Azure OpenAI Service 設定
# ========================================
AZURE_OPENAI_ENDPOINT=https://ハンズオン用エンドポイント/
AZURE_OPENAI_API_KEY=配布されたOpenAI_API_Key
AZURE_OPENAI_DEPLOYMENT_GPT5=gpt-5
AZURE_OPENAI_DEPLOYMENT_GPT5_MINI=gpt-5-mini

# ========================================
# Azure Speech Service 設定
# ========================================
AZURE_SPEECH_API_KEY=配布されたSpeech_API_Key
AZURE_SPEECH_REGION=japaneast
AZURE_SPEECH_LANGUAGE=ja-JP
AZURE_SPEECH_VOICE_NAME=ja-JP-NanamiNeural
```

#### ステップ4: 依存パッケージをインストール（1分）

```bash
# uvで一括インストール
uv sync
```

#### ステップ5: 動作確認（30秒）

**01_multi-llm-reasoningの動作確認**:

```bash
cd 01_multi-llm-reasoning
uv run python main.py "量子コンピューターとは何ですか？"
```

**02_azure-voice-chatbotの動作確認**:

```bash
cd ../02_azure-voice-chatbot
uv run python main.py
# 音声入力が始まったら「こんにちは」と話しかけてみてください
```

---

### 🔐 セキュリティ注意事項

#### API Keyの取り扱い

⚠️ **重要**: 配布されたAPI Keyは機密情報です！

- ❌ GitHub等の公開リポジトリにpushしない
- ❌ SNSやチャットで共有しない
- ❌ スクリーンショットに含めない
- ✅ ハンズオン終了後は`.env`ファイルを削除

#### .gitignoreの確認

このリポジトリには既に`.gitignore`が設定されており、`.env`ファイルは自動的にGit管理から除外されます。

```bash
# .gitignoreで除外されているか確認
cat .gitignore | grep .env
# 出力: .env が含まれていればOK
```

---

### ❓ トラブルシューティング（ハンズオン参加者向け）

#### Q1: 環境変数エラーが出る

```
❌ エラー: AZURE_OPENAI_ENDPOINTが設定されていません
```

**解決方法**:
1. `.env`ファイルが`agent-handson/`ディレクトリにあるか確認
2. API Keyが正しく記載されているか確認（スペースや改行に注意）

```bash
# 現在のディレクトリを確認
pwd
# 出力: /path/to/agent-handson

# .envファイルの存在確認
ls -la .env

# .envファイルの内容確認（API Keyは表示されます）
cat .env
```

#### Q2: Python/uvが見つからない

```
❌ command not found: python
❌ command not found: uv
```

**解決方法**: 主催者または近くの参加者にサポートを依頼してください。

#### Q3: マイクが認識されない（02_azure-voice-chatbot）

**解決方法**:
- マイクが接続されているか確認
- ブラウザ/OSのマイク権限を確認
- 他のアプリがマイクを使用していないか確認

#### その他のトラブル

主催者に質問してください。詳細なエラーメッセージをコピーしておくとスムーズです。

---

### 📚 参考: 本格的な学習をしたい方へ

ハンズオン終了後、自分のAzureアカウントで継続学習したい場合：

1. **Azureアカウントを作成**: https://azure.microsoft.com/free/
2. **Azure CLIをインストール**: [共通設定](#共通設定)を参照
3. **自分のリソースを作成**: [01用設定](#01_multi-llm-reasoning用-azure設定)、[02用設定](#02_azure-voice-chatbot用-azure設定)を参照

Azure CLI認証を使えば、APIキーなしで安全に開発できます。

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
- 入力トークン: 約 ¥189.91 / 1Mトークン（※最新料金はAzure Portalで確認）
- 出力トークン: 約 ¥1,519.25 / 1Mトークン

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

## 主催者向けリソース準備ガイド

**このセクションはハンズオン主催者向けです。参加者に提供する共有Azureリソースの準備方法を説明します。**

### 📝 準備の流れ

```
1. Azureリソースの作成
   ↓
2. API Keyの取得
   ↓
3. 参加者への配布準備
   ↓
4. ハンズオン実施
   ↓
5. 後処理（API Key無効化）
```

---

### ステップ1: Azureリソースの作成

#### 1-1. Azure OpenAI Serviceの作成

**リソース作成**:
- [01_multi-llm-reasoning用 Azure設定](#01_multi-llm-reasoning用-azure設定)の手順に従ってリソース作成
- GPT-5とGPT-5-miniの両方をデプロイ

**推奨設定**:
- **価格レベル**: Standard S0（本格利用の場合）
- **リージョン**: Japan East（日本で実施する場合）
- **使用量制限**: Azure Portalで設定可能（コスト管理）

#### 1-2. Azure Speech Serviceの作成

**リソース作成**:
- [02_azure-voice-chatbot用 Azure設定](#02_azure-voice-chatbot用-azure設定)の手順に従ってリソース作成

**推奨設定**:
- **価格レベル**: Standard S0（Free F0は制限が厳しい）
- **リージョン**: Japan East（OpenAIと同じリージョン推奨）

---

### ステップ2: API Keyとエンドポイントの取得

#### 2-1. Azure OpenAI Service

Azure Portalで以下を取得：

```
リソース → キーとエンドポイント

必要な情報:
- エンドポイント: https://your-resource.openai.azure.com/
- キー1（API Key）: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
- デプロイメント名: gpt-5, gpt-5-mini
```

#### 2-2. Azure Speech Service

Azure Portalで以下を取得：

```
リソース → キーとエンドポイント

必要な情報:
- キー1（API Key）: yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy
- リージョン: japaneast
```

---

### ステップ3: 参加者への配布資料準備

#### 3-1. .env設定サンプルの作成

参加者に配布する`.env`設定値を準備：

```bash
# ========================================
# ハンズオン用Azure設定（参加者配布用）
# ========================================

# Azure OpenAI Service
AZURE_OPENAI_ENDPOINT=https://your-actual-endpoint.openai.azure.com/
AZURE_OPENAI_API_KEY=実際のOpenAI_API_Key
AZURE_OPENAI_DEPLOYMENT_GPT5=gpt-5
AZURE_OPENAI_DEPLOYMENT_GPT5_MINI=gpt-5-mini

# Azure Speech Service
AZURE_SPEECH_API_KEY=実際のSpeech_API_Key
AZURE_SPEECH_REGION=japaneast
AZURE_SPEECH_LANGUAGE=ja-JP
AZURE_SPEECH_VOICE_NAME=ja-JP-NanamiNeural
```

#### 3-2. 配布方法

**推奨**: ハンズオン当日にSlack/チャットで共有

```markdown
# ハンズオン参加者の皆様へ

以下の設定値を.envファイルに記載してください：

（上記の設定値をコピー）

⚠️ 注意:
- このAPI Keyはハンズオン専用です
- ハンズオン終了後、このKeyは無効化されます
- 外部への共有は厳禁です
```

**セキュリティのベストプラクティス**:
- ✅ 当日配布（事前配布は避ける）
- ✅ Slack DM、限定チャンネルで共有
- ✅ 公開チャンネル・メールは避ける
- ✅ ハンズオン終了後に無効化を明記

---

### ステップ4: コスト管理

#### 4-1. 使用量制限の設定（推奨）

Azure Portalで使用量制限を設定：

```
Azure OpenAI Service
→ クォータ
→ 使用量制限を設定

例: 1日あたり100,000トークンまで
```

#### 4-2. 予算アラートの設定

Azure Cost Managementで予算を設定：

```
Cost Management
→ 予算
→ 新しい予算を作成

例: 月5,000円の予算、80%で警告
```

#### 4-3. 想定コスト（参考）

**10人規模のハンズオン（3時間）の場合**:

| サービス | 使用量 | 単価 | 合計 |
|---------|--------|------|------|
| Azure OpenAI (GPT-5) | ~500K tokens | ~$X/1M tokens | ~$Y |
| Azure OpenAI (GPT-5-mini) | ~1M tokens | ~$Z/1M tokens | ~$W |
| Azure Speech (STT) | ~5時間 | ~¥120/時間 | ~¥600 |
| Azure Speech (TTS) | ~100K文字 | ~¥2,000/1M文字 | ~¥200 |
| **合計** | - | - | **~¥1,000〜3,000** |

*実際の料金は使用状況により変動します。最新料金はAzure Portalで確認してください。

---

### ステップ5: ハンズオン当日の運営

#### 5-1. 開始前

- [ ] API Keyが有効であることを確認
- [ ] 自分の環境で動作確認
- [ ] Slackに配布資料を投稿準備

#### 5-2. ハンズオン中

- [ ] API Key使用状況をモニタリング（Azure Portal）
- [ ] 使用量が予想を超えた場合は制限を調整
- [ ] トラブル時は[トラブルシューティング](#トラブルシューティング)を参照

#### 5-3. よくある質問への対応

**Q: API Keyが認識されない**
→ `.env`ファイルの場所、スペース・改行の確認

**Q: マイクが動かない**
→ OSのマイク権限設定を確認

**Q: 応答が遅い**
→ Azure リージョンの距離、ネットワーク状況を確認

---

### ステップ6: ハンズオン終了後の処理

#### 6-1. API Keyの無効化（必須）

**Azure OpenAI Service**:
```
Azure Portal
→ Azure OpenAI リソース
→ キーとエンドポイント
→ キー1を再生成

これにより配布したAPI Keyは即座に無効化されます
```

**Azure Speech Service**:
```
同様の手順でSpeech ServiceのAPI Keyも再生成
```

#### 6-2. 使用量・コストの確認

```
Cost Management
→ コスト分析
→ 期間を選択してコストを確認
```

#### 6-3. 参加者へのフォローアップ（オプション）

```markdown
# ハンズオンご参加ありがとうございました

本日使用したAPI Keyは無効化されました。
継続学習したい方は、以下を参照してご自身のAzureアカウントでお試しください：

📚 .azure/azure_settings.md
- 「共通設定」セクション
- 「01_multi-llm-reasoning用 Azure設定」
- 「02_azure-voice-chatbot用 Azure設定」

ご質問があればお気軽にどうぞ！
```

---

### 📊 チェックリスト

#### ハンズオン1週間前

- [ ] Azureリソース作成完了
- [ ] API Key取得完了
- [ ] 配布資料準備完了
- [ ] 自分の環境で動作確認完了
- [ ] 使用量制限・予算アラート設定完了

#### ハンズオン当日

- [ ] API Key配布準備完了
- [ ] モニタリング画面を開いておく
- [ ] トラブルシューティング資料を手元に用意

#### ハンズオン終了後

- [ ] API Key無効化完了
- [ ] 使用量・コスト確認完了
- [ ] 参加者フォローアップ送信（オプション）

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
