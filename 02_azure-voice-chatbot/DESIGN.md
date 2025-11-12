# Azure Voice Chatbot 設計計画書

## システム概要

Azure Speech ServicesとMicrosoft Agent Frameworkを組み合わせ、**音声で対話できるAIチャットボット**を構築します。Speech-to-Text（音声認識）とText-to-Speech（音声合成）を使い、GPT-5とのマルチターン対話を音声で実現します。

## アーキテクチャ設計

### システムフロー

```
🎤 ユーザー音声入力
    ↓
🔊 Speech-to-Text (Azure Speech Service)
    ↓
📝 テキストに変換
    ↓
🤖 VoiceAgent処理 (agent-framework + Azure OpenAI GPT-5)
    ↓
💬 応答テキスト生成
    ↓
🔉 Text-to-Speech (Azure Speech Service)
    ↓
🔊 音声出力・再生
```

### 対話ループ

```python
while True:
    # 1. 音声入力を待機
    user_speech = recognize_speech()

    # 2. Speech-to-Text
    user_text = speech_to_text(user_speech)

    # 3. エージェントで応答生成（会話履歴を保持）
    agent_response = await voice_agent.run(user_text)

    # 4. Text-to-Speech
    response_audio = text_to_speech(agent_response.text)

    # 5. 音声出力
    play_audio(response_audio)
```

### エージェント構成

**Phase 1: シンプル構成（単一エージェント）**

- **VoiceAgent**: 音声対話を担当する単一エージェント
  - 役割: ユーザーとの対話全般
  - 使用モデル: Azure OpenAI **GPT-5**
  - 機能: マルチターン対話、会話履歴管理

**Phase 2以降: 拡張構成（複数エージェント）**

- **ListenerAgent**: 音声認識と意図理解
- **ProcessorAgent**: 対話処理と応答生成
- **SpeakerAgent**: 音声合成と出力

## 使用するAzureサービス

### 1. Azure Speech Service

**主要機能:**
- **Speech-to-Text（音声認識）**
  - リアルタイム音声認識
  - 日本語対応（`ja-JP`）
  - 高精度（文字誤り率 0-5%）

- **Text-to-Speech（音声合成）**
  - 自然な日本語音声
  - 複数の音声スタイル（Neural Voice）
  - 推奨: `ja-JP-NanamiNeural`、`ja-JP-KeitaNeural`

**料金:**
- Speech-to-Text: 約 ¥120/時間
- Text-to-Speech (Neural): 約 ¥2,000/100万文字

### 2. Azure OpenAI Service

**使用モデル:**
- **GPT-5**: 高度な対話処理
  - マルチターン会話に最適
  - コンテキスト理解が優れている
  - 自然な応答生成

## ディレクトリ構造

```
02_azure-voice-chatbot/
├── README.md                 # プロジェクト説明
├── DESIGN.md                 # 本設計書
├── main.py                   # メインエントリーポイント
├── voice_chat.py             # 音声対話ループ
│
├── agents/                   # エージェント定義
│   ├── __init__.py
│   ├── base.py              # ベースエージェント（01から流用）
│   └── voice_agent.py       # 音声対話エージェント
│
├── speech/                   # 音声処理モジュール
│   ├── __init__.py
│   ├── recognizer.py        # Speech-to-Text
│   └── synthesizer.py       # Text-to-Speech
│
├── config/                   # 設定管理
│   ├── __init__.py
│   └── settings.py          # Azure設定（Speech + OpenAI）
│
├── tools/                    # カスタムツール（オプション）
│   ├── __init__.py
│   └── conversation_tools.py # 会話支援ツール
│
├── examples/                 # 実行サンプル
│   ├── __init__.py
│   ├── test_speech.py       # 音声入出力テスト
│   └── simple_chat.py       # シンプルな音声対話例
│
└── tests/                    # テスト（Phase 4）
    ├── __init__.py
    ├── test_recognizer.py
    └── test_synthesizer.py
```

## 実装ステップ

### Phase 1: 基本音声入出力（現在のフェーズ）

**目標**: Azure Speech Serviceの基本機能を実装

1. **環境セットアップ**
   - Azure Speech Serviceリソース作成
   - `azure-cognitiveservices-speech` パッケージ追加
   - 環境変数設定

2. **設定モジュール実装**
   - `config/settings.py`: Speech Service認証情報管理

3. **音声認識モジュール実装**
   - `speech/recognizer.py`: Speech-to-Text機能
   - 日本語音声認識
   - エラーハンドリング

4. **音声合成モジュール実装**
   - `speech/synthesizer.py`: Text-to-Speech機能
   - 日本語音声合成
   - 音声スタイル設定

5. **動作確認**
   - `examples/test_speech.py`: 基本機能テスト

### Phase 2: エージェント統合

**目標**: agent-frameworkと音声機能を統合

1. **VoiceAgent実装**
   - GPT-5ベースのエージェント
   - マルチターン対話対応
   - 会話履歴管理

2. **音声対話ループ実装**
   - 音声入力 → エージェント → 音声出力のループ
   - セッション管理

3. **メインアプリケーション**
   - コマンドラインインターフェース
   - 対話開始・終了処理

### Phase 3: 機能拡張

**目標**: 実用的な機能を追加

1. **会話支援ツール**
   - 会話履歴の要約
   - コンテキスト管理

2. **エラーハンドリング強化**
   - 音声認識失敗時の再試行
   - タイムアウト処理

3. **設定カスタマイズ**
   - 音声スタイル選択
   - 発話速度調整

### Phase 4: テストとドキュメント

**目標**: 品質保証と使いやすさ向上

1. **テスト実装**
   - ユニットテスト
   - 統合テスト

2. **ドキュメント整備**
   - README更新
   - 使用例追加

## 技術スタック

### コア技術
- **フレームワーク**: Microsoft Agent Framework 1.0.0b251104
- **言語**: Python 3.11+
- **LLMプロバイダー**: Azure AI Foundry (Azure OpenAI Service)
  - **GPT-5** (対話処理)

### Azureサービス
- **Azure Speech Service**: 音声認識・音声合成
- **Azure OpenAI Service**: GPT-5モデルホスティング
- **Azure Identity**: 認証・認可

### Pythonパッケージ

```txt
# Agent Framework
agent-framework==1.0.0b251104

# Azure Speech SDK
azure-cognitiveservices-speech>=1.40.0

# Azure認証
azure-identity>=1.25.0

# 環境変数管理
python-dotenv>=1.2.0
```

## Azure Speech Serviceのセットアップ

### ステップ1: Azureポータルでリソース作成

1. **Azure Portalにアクセス**
   - https://portal.azure.com

2. **Speech Serviceを作成**
   ```
   リソースの作成
   → AI + Machine Learning
   → Speech Services
   ```

3. **設定項目**
   - **サブスクリプション**: 使用するサブスクリプション
   - **リソースグループ**: 新規作成 or 既存のグループ
   - **リージョン**: Japan East（または East US）
   - **名前**: 任意の名前（例: `voice-chatbot-speech`）
   - **価格レベル**: Free F0（テスト用）または Standard S0

4. **確認と作成**
   - 設定を確認して「作成」をクリック

### ステップ2: APIキーとエンドポイントを取得

1. **作成したリソースを開く**

2. **「キーとエンドポイント」を選択**

3. **以下の情報をコピー**
   - **キー1** (API Key)
   - **リージョン** (例: `japaneast`)
   - **エンドポイント** (例: `https://japaneast.api.cognitive.microsoft.com/`)

### ステップ3: 環境変数を設定

`.env` ファイルに以下を追加：

```bash
# Azure Speech Service 設定
AZURE_SPEECH_API_KEY=your_api_key_here
AZURE_SPEECH_REGION=japaneast
AZURE_SPEECH_LANGUAGE=ja-JP
AZURE_SPEECH_VOICE_NAME=ja-JP-NanamiNeural
```

## 認証方法

### 方法1: APIキー認証（推奨・シンプル）

```python
import azure.cognitiveservices.speech as speechsdk

speech_config = speechsdk.SpeechConfig(
    subscription=os.getenv("AZURE_SPEECH_API_KEY"),
    region=os.getenv("AZURE_SPEECH_REGION")
)
```

### 方法2: Azure CLI認証

```python
from azure.identity import AzureCliCredential

# Azure CLIでログイン済みの場合
credential = AzureCliCredential()
# Speech SDKはDefaultAzureCredentialに対応していないため、
# APIキー認証を推奨
```

## 環境変数設定

### .env ファイル例

```bash
# ========================================
# Azure OpenAI Service 設定
# ========================================
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_GPT5=gpt-5

# 認証（Azure CLI推奨）
# az login でログイン済みの場合、以下は不要
# AZURE_OPENAI_API_KEY=your_openai_api_key

# ========================================
# Azure Speech Service 設定
# ========================================
AZURE_SPEECH_API_KEY=your_speech_api_key
AZURE_SPEECH_REGION=japaneast

# 音声設定
AZURE_SPEECH_LANGUAGE=ja-JP
AZURE_SPEECH_VOICE_NAME=ja-JP-NanamiNeural

# その他の音声オプション（例）
# ja-JP-KeitaNeural (男性)
# ja-JP-AoiNeural (女性)
```

## 期待される成果

### 技術的成果
- Azure Speech Serviceの実践的な使用方法習得
- 音声入出力とAIエージェントの統合スキル
- リアルタイム音声処理の実装経験
- GPT-5とのマルチターン音声対話システム構築

### 成果物
- 動作する音声対話AIシステム
- 再利用可能な音声処理モジュール
- 詳細なドキュメントとサンプルコード

## 実装上の注意点

### 1. 音声品質
- マイク品質による認識精度の影響
- 静かな環境での動作確認推奨
- バックグラウンドノイズの影響を最小化

### 2. レイテンシ
- Speech-to-Text: 約0.5-1秒
- Agent処理（GPT-5）: 1-3秒
- Text-to-Speech: 約0.5-1秒
- **合計**: 2-5秒程度の応答時間

### 3. コスト管理
- **Speech Service**: 従量課金（音声処理時間）
  - テスト時はFree F0プランを活用
- **Azure OpenAI**: トークン課金
  - 01_multi-llm-reasoningと同様

### 4. エラーハンドリング
- ネットワーク障害
- 音声認識失敗（無音、雑音など）
- APIレート制限
- タイムアウト処理

## 利用可能な日本語音声（Neural Voice）

| 音声名 | 性別 | 特徴 |
|-------|------|------|
| ja-JP-NanamiNeural | 女性 | 標準的で自然な音声 |
| ja-JP-KeitaNeural | 男性 | 落ち着いた音声 |
| ja-JP-AoiNeural | 女性 | 若々しい音声 |
| ja-JP-DaichiNeural | 男性 | ビジネス向け |
| ja-JP-MayuNeural | 女性 | 親しみやすい音声 |
| ja-JP-NaokiNeural | 男性 | 明瞭な音声 |
| ja-JP-ShioriNeural | 女性 | 柔らかい音声 |

## 学習リソース

### Azure Speech Service
- [Azure Speech Service Documentation](https://learn.microsoft.com/azure/ai-services/speech-service/)
- [Speech SDK for Python](https://learn.microsoft.com/azure/ai-services/speech-service/quickstarts/setup-platform?pivots=programming-language-python)
- [Speech-to-Text Quickstart](https://learn.microsoft.com/azure/ai-services/speech-service/get-started-speech-to-text)
- [Text-to-Speech Quickstart](https://learn.microsoft.com/azure/ai-services/speech-service/get-started-text-to-speech)

### Agent Framework
- [Microsoft Agent Framework GitHub](https://github.com/microsoft/agent-framework)
- [Agent Framework Overview](https://learn.microsoft.com/agent-framework/overview/agent-framework-overview)

### その他
- [Azure Cognitive Services Speech SDK](https://github.com/Azure-Samples/cognitive-services-speech-sdk)
- [ソフトバンク技術ブログ - Azure Speech Service](https://www.softbank.jp/biz/blog/cloud-technology/articles/202410/azure-speech-service/)

---

**作成日**: 2025-11-12
**最終更新**: 2025-11-12
**バージョン**: 1.0
**ステータス**: Phase 1 - 基本音声入出力実装中
