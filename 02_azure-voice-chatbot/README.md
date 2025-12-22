# 🎙️ Azure Voice Chatbot

**5分で音声AIアシスタントを体験！ - Azure Speech Servicesの実力を実感しよう**

Azure Speech ServicesとMicrosoft Agent Frameworkを組み合わせた**音声対話型AIチャットボット**で、次世代の音声インターフェースを体験できます。

---

## 🎯 このプロジェクトで学べること

### ✨ Azure Speech Serviceの魅力を体験
- **99%の音声認識精度**: ビジネスでも使える高精度
- **40言語以上対応**: 日本語から英語まで幅広くサポート
- **Neural Voice**: 人間に近い自然な音声合成
- **低レイテンシ**: リアルタイム対話に最適（応答時間2-5秒）

### 🛠️ 実践的なスキル習得
- **Speech-to-Text**: 音声認識の実装方法
- **Text-to-Speech**: 音声合成の実装方法
- **マルチターン対話**: GPT-5との自然な会話の実現
- **音声コマンド**: 音声による直感的な操作

### 💡 業務に応用できる技術
- **コールセンター自動化**: 音声による問い合わせ対応
- **音声アシスタント**: ハンズフリーな業務支援
- **アクセシビリティ**: 視覚障害者向けインターフェース
- **多言語対応**: グローバルなサービス展開

---

## 📋 目次

- [概要](#概要)
- [システムアーキテクチャ](#システムアーキテクチャ)
- [環境要件](#環境要件)
- [セットアップ手順](#セットアップ手順)
- [使用方法](#使用方法)
- [音声コマンド機能](#音声コマンド機能)
- [プロジェクト構造](#プロジェクト構造)
- [トラブルシューティング](#トラブルシューティング)
- [実用例とユースケース](#実用例とユースケース)
- [Azureの強みとコスト](#azureの強みとコスト)

---

## 概要

このプロジェクトは、**Azure Speech Service**と**Microsoft Agent Framework**を組み合わせて、GPT-5と音声で対話できるAIチャットボットを構築するハンズオンです。

### 特徴

#### ✅ 基本機能
- **Speech-to-Text**: 日本語音声をリアルタイムでテキスト化
- **GPT-5との対話**: マルチターン会話に対応
- **Text-to-Speech**: 自然な日本語音声で応答
- **安全機構**: 無限ループ防止、エラーハンドリング

#### ✅ 音声コマンド機能
- **会話要約**: 「要約して」「まとめて」でこれまでの対話を自動要約
- **音声プロファイル切り替え**: 「音声を変更して」で5種類の音声から選択可能
- **話速調整**: 「速く話して」「ゆっくり話して」でリアルタイム調整（0.5x ~ 1.5x）
- **設定リセット**: 「音声をリセット」でデフォルトに戻す

#### ✅ コンテキスト管理
- **会話の文脈を自動抽出・保持**: ユーザー名、話題などを自動認識
- **自然な対話**: 前の会話内容を踏まえた応答
- **統計情報**: 会話ターン数、メッセージ数などを管理

### 動作イメージ

```
🎤 ユーザー音声入力
    ↓
🔊 Speech-to-Text (Azure Speech Service)
    ↓ 99%の認識精度
📝 テキスト化
    ↓
🤖 VoiceAgent処理 (GPT-5)
    ↓ マルチターン対話
💬 応答テキスト生成
    ↓
🔉 Text-to-Speech (Azure Speech Service)
    ↓ Neural Voice（自然な音声）
🔊 音声出力・再生
```

---

## システムアーキテクチャ

### 対話フロー

1. **音声入力**: ユーザーがマイクで質問
2. **音声認識**: Azure Speech Serviceでテキスト化（99%精度）
3. **エージェント処理**: GPT-5が応答を生成（会話履歴を保持）
4. **音声合成**: 応答テキストを自然な音声に変換（Neural Voice）
5. **音声出力**: スピーカーで再生

### 技術スタック

- **Microsoft Agent Framework** 1.0.0b251104
- **Azure Speech Service** (Speech-to-Text / Text-to-Speech)
- **Azure OpenAI Service** (GPT-5)
- **Python** 3.11+
- **uv** パッケージマネージャー

---

## 環境要件

### 必須環境

- **Python**: 3.11以上
- **uv**: パッケージマネージャー
- **Azureサブスクリプション**
- **Azure Speech Service**: 音声認識・合成用
- **Azure OpenAI Service**: GPT-5モデル
- **マイクとスピーカー**: 音声入出力用

### 推奨環境

- **Azure CLI**: 認証に使用
- **静かな環境**: 音声認識の精度向上のため

---

## セットアップ手順

### 🎓 ハンズオン参加者向けクイックスタート

**主催者から配布されたAPI Keyがある場合、こちらの簡単な手順で5分でセットアップ完了！**

#### ステップ1: リポジトリをクローン（01_multi-llm-reasoningで完了済）
```bash
git clone https://github.com/chinchillaa/agent-handson.git
cd agent-handson
```

#### ステップ2: 環境ファイルを作成（01_multi-llm-reasoningで完了済）
```bash
cp .env.example .env
nano .env  # または vim/code .env
```

#### ステップ3: 配布されたAPI Keyを.envに設定
```bash
# Azure OpenAI Service
AZURE_OPENAI_ENDPOINT=配布されたエンドポイント
AZURE_OPENAI_API_KEY=配布されたOpenAI_API_Key
AZURE_OPENAI_DEPLOYMENT_GPT5=gpt-5

# Azure Speech Service
AZURE_SPEECH_API_KEY=配布されたSpeech_API_Key
AZURE_SPEECH_REGION=japaneast
AZURE_SPEECH_LANGUAGE=ja-JP
AZURE_SPEECH_VOICE_NAME=ja-JP-NanamiNeural
```

#### ステップ4: 依存パッケージをインストール（01_multi-llm-reasoningで完了済）
```bash
uv sync
```

#### ステップ5: 動作確認
```bash
cd 02_azure-voice-chatbot
uv run python main.py
# マイクに向かって「こんにちは」と話しかけてみてください
```

**詳細**: [ハンズオン参加者向けガイド](../HANDSON_QUICKSTART.md)

---

### 💻 自分のAzureアカウントでセットアップする場合

**本格的に学習したい方・継続利用したい方向けの手順**

#### 1. リポジトリのクローン（既に実施済みの場合はスキップ）

```bash
git clone https://github.com/chinchillaa/agent-handson.git
cd agent-handson/02_azure-voice-chatbot
```

#### 2. 依存パッケージのインストール

```bash
# プロジェクトルートで実行（uvが依存関係を同期）
cd ..  # agent-handson/ へ移動
uv sync
```

これにより、以下が自動的にインストールされます：
- `agent-framework`
- `azure-cognitiveservices-speech`
- `azure-identity`
- `python-dotenv`

#### 3. Azure設定

Azure Speech ServiceとAzure OpenAI Serviceの設定が必要です。

**詳細な設定手順は以下を参照してください**:
- **[Azure設定ガイド](../.azure/azure_settings.md)** - Azure Speech Service・Azure OpenAI Serviceの作成手順、環境変数設定、認証方法など

**推奨認証方式**:
- ✅ **Azure CLI認証**（OpenAI用 - セキュリティ高）
- ✅ **API Key認証**（Speech用 - 現状必須）

---

## 使用方法

### 基本的な使い方

```bash
# 音声対話を開始
uv run python 02_azure-voice-chatbot/main.py
```

マイクに向かって話しかけると、AIが音声で応答します。

**終了方法**: 「終了」「バイバイ」「さようなら」などと話しかけるか、Ctrl+C

### 音声コマンド機能を体験

```bash
# 音声コマンド、コンテキスト管理、会話要約などの高度な機能を試す
uv run python 02_azure-voice-chatbot/examples/advanced_chat.py
```

### 音声入出力のテスト

```bash
# 音声認識・合成の基本動作を確認
uv run python 02_azure-voice-chatbot/examples/test_speech.py
```

---

## 音声コマンド機能

音声対話中に以下のコマンドを使用できます：

### 📝 会話要約
```
「要約して」「まとめて」「サマリーを見せて」
```
これまでの会話内容を自動で要約します。

### 🎙️  音声プロファイル変更
```
「音声を変更して」「声を変えて」
```
以下の音声から順番に切り替わります：
- **デフォルト**（明るく親しみやすい女性 - Nanami）
- **優しい**（落ち着いた女性 - Shiori）
- **元気**（明るく元気な女性 - Aoi）
- **落ち着いた男性**（Keita）
- **親しみやすい男性**（Naoki）

### ⏩ 話速調整
```
「速く話して」「早く話して」  # 0.25倍速アップ
「ゆっくり話して」「遅く話して」  # 0.25倍速ダウン
```
話速を0.5倍 ~ 1.5倍の範囲で調整できます。

### 🔄 設定リセット
```
「音声をリセット」「音声を初期化」
```
音声設定をデフォルトに戻します。

---

## プロジェクト構造

```
02_azure-voice-chatbot/
├── agents/                    # エージェント定義
│   ├── __init__.py
│   ├── base.py               # ベースエージェント
│   └── voice_agent.py        # 音声対話エージェント
│
├── speech/                    # 音声処理モジュール
│   ├── __init__.py
│   ├── recognizer.py         # Speech-to-Text
│   └── synthesizer.py        # Text-to-Speech
│
├── config/                    # 設定管理
│   ├── __init__.py
│   └── settings.py           # Azure設定
│
├── tools/                     # カスタムツール
│   ├── __init__.py
│   ├── context_manager.py    # コンテキスト管理
│   ├── conversation_summarizer.py # 会話要約
│   └── voice_profiles.py     # 音声プロファイル定義
│
├── tests/                     # テストコード
│   ├── __init__.py
│   ├── test_config.py        # 設定テスト
│   ├── test_recognizer.py    # 音声認識テスト
│   ├── test_synthesizer.py   # 音声合成テスト
│   ├── test_context_manager.py # コンテキスト管理テスト
│   ├── test_conversation_summarizer.py # 会話要約テスト
│   ├── test_voice_agent.py   # エージェントテスト
│   ├── test_voice_chat.py    # 対話ループテスト
│   └── test_integration.py   # 統合テスト
│
├── examples/                  # 実行サンプル
│   ├── __init__.py
│   ├── test_speech.py        # 音声入出力テスト
│   ├── simple_chat.py        # 基本音声対話
│   └── advanced_chat.py      # 音声コマンド機能デモ
│
├── main.py                    # メインエントリーポイント
├── voice_chat.py              # 音声対話ループ
├── DESIGN.md                  # 設計ドキュメント（開発者向け）
├── COST_ESTIMATES.md          # コスト見積もり
└── README.md                  # このファイル
```

---

## トラブルシューティング

Azure関連のトラブルシューティングは **[Azure設定ガイド - トラブルシューティング](../.azure/azure_settings.md#トラブルシューティング)** を参照してください。

### マイクが認識されない

**解決方法**:
- マイクが正しく接続されているか確認
- OSのマイク権限設定を確認
- 他のアプリケーションがマイクを使用していないか確認

### 音声認識の精度が低い

**解決方法**:
- 静かな環境で使用
- マイクを口に近づける（15-30cm程度）
- バックグラウンドノイズを最小化
- マイクの品質を確認（USB接続のマイク推奨）

### パッケージインストールエラー

```bash
# 依存関係を再インストール
uv sync --refresh
```

### 音声が出力されない

**解決方法**:
- スピーカー/ヘッドフォンが正しく接続されているか確認
- システムの音量設定を確認
- 他のアプリケーションが音声デバイスを使用していないか確認

---

## 実用例とユースケース

### 💼 ビジネス活用例

#### 1. コールセンター自動化
- **24時間365日対応**: 音声による自動問い合わせ対応
- **多言語対応**: 40言語以上に対応可能
- **コスト削減**: オペレーター人件費の削減

#### 2. 社内ヘルプデスク
- **ハンズフリー操作**: 作業中でも音声で問い合わせ可能
- **情報検索**: 社内ドキュメントの音声検索
- **FAQ自動応答**: よくある質問への自動回答

#### 3. アクセシビリティ向上
- **視覚障害者支援**: 音声による情報アクセス
- **高齢者向けインターフェース**: 直感的な音声操作
- **多言語サポート**: 外国人利用者への対応

### 🏢 導入のメリット

#### コスト効率
- **初期費用不要**: 従量課金制で小さく始められる
- **インフラ不要**: クラウドベースで保守不要
- **スケーラブル**: 利用量に応じて柔軟にスケール

#### 高品質
- **99%の認識精度**: ビジネスに耐える高精度
- **低レイテンシ**: 2-5秒の応答時間
- **自然な音声**: Neural Voiceによる人間らしい音声

#### 開発効率
- **簡単な実装**: Microsoft Agent Frameworkで数時間で構築
- **豊富なドキュメント**: 日本語含む充実した資料
- **継続的なアップデート**: 最新のAI技術を常に利用可能

---

## Azureの強みとコスト

### 💪 Azure Speech Serviceの強み

#### 🎯 高精度・高品質
- **99%の音声認識精度**: 業界トップクラスの精度
- **Neural Voice**: 人間に近い自然な音声合成
- **40言語以上対応**: グローバル展開も容易
- **方言対応**: 日本語の方言にも対応

#### ⚡ 高性能
- **低レイテンシ**: リアルタイム対話に最適
- **高可用性**: 99.9%のSLA保証
- **グローバル展開**: 世界60以上のリージョン

#### 🔒 セキュリティ
- **エンタープライズグレード**: SOC、ISO、HIPAAなど各種認証
- **データ保護**: Azure独自のセキュリティ基盤
- **コンプライアンス**: 各国の規制に対応

### 💰 コスト

#### Speech-to-Text（音声認識）
- **Standard**: 約 ¥120/時間
- **無料枠**: 5時間/月（Standard）

#### Text-to-Speech（音声合成）
- **Neural Voice**: 約 ¥2,000/100万文字
- **無料枠**: 50万文字/月（Neural）

#### Azure OpenAI Service（GPT-5）
- **従量課金制**: トークン数に応じた課金
- **GPT-5-mini**: 高速・低コストなオプション

**詳細**: [Azure Pricing Calculator](https://azure.microsoft.com/pricing/calculator/)

### 📊 コスト試算例

**月間1000回の音声対話（1回5分）の場合**:
- Speech-to-Text: 5分 × 1000回 = 83時間 ≈ ¥10,000
- Text-to-Speech: 約200文字 × 1000回 ≈ ¥400
- Azure OpenAI: トークン数に応じて変動

**合計**: 約 ¥10,400/月 + OpenAI費用

※無料枠を活用することで、開発・テスト段階ではコストを大幅に削減可能

---

## 関連ドキュメント

- **コスト見積もり**: [COST_ESTIMATES.md](./COST_ESTIMATES.md)
- **プロジェクトルート**: [../README.md](../README.md)
- **ハンズオンクイックスタート**: [../HANDSON_QUICKSTART.md](../HANDSON_QUICKSTART.md)
- **設計ドキュメント（開発者向け）**: [DESIGN.md](./DESIGN.md)
- **開発履歴（開発者向け）**: [../PROJECT_HISTORY.md](../PROJECT_HISTORY.md)
- **開発ガイド（開発者向け）**: [../CLAUDE.md](../CLAUDE.md)

---

## 参考資料

### Azure Speech Service
- [Azure Speech Service Documentation](https://learn.microsoft.com/azure/ai-services/speech-service/)
- [Speech SDK for Python](https://learn.microsoft.com/azure/ai-services/speech-service/quickstarts/setup-platform?pivots=programming-language-python)
- [Speech-to-Text Quickstart](https://learn.microsoft.com/azure/ai-services/speech-service/get-started-speech-to-text)
- [Text-to-Speech Quickstart](https://learn.microsoft.com/azure/ai-services/speech-service/get-started-text-to-speech)

### Microsoft Agent Framework
- [Microsoft Agent Framework GitHub](https://github.com/microsoft/agent-framework)
- [Agent Framework Overview](https://learn.microsoft.com/agent-framework/overview/agent-framework-overview)

### その他
- [Azure Cognitive Services Speech SDK](https://github.com/Azure-Samples/cognitive-services-speech-sdk)
- [ソフトバンク技術ブログ - Azure Speech Service](https://www.softbank.jp/biz/blog/cloud-technology/articles/202410/azure-speech-service/)

---

## 🎓 次のステップ

### ハンズオン後の学習

1. **自分のAzureアカウントで継続**: [Azure無料アカウント作成](https://azure.microsoft.com/free/)
2. **他の音声機能を試す**: 音声翻訳、話者認識など
3. **カスタム音声モデル**: 自社ブランドの音声を作成
4. **他のAzure AIサービスと統合**: Computer Vision、Language Serviceなど

### おすすめリソース

- **Azure OpenAI Service**: https://learn.microsoft.com/azure/ai-services/openai/
- **Azure Speech Studio**: https://speech.microsoft.com/
- **Microsoft Learn**: https://learn.microsoft.com/training/

---

**Azureで次世代の音声AIを体験しよう！** 🚀

質問があれば主催者または近くの参加者に気軽に声をかけてください。
