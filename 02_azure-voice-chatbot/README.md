# Azure Voice Chatbot

Azure Speech ServicesとMicrosoft Agent Frameworkを組み合わせた**音声対話型AIチャットボット**

## 📋 目次

- [概要](#概要)
- [システムアーキテクチャ](#システムアーキテクチャ)
- [環境要件](#環境要件)
- [セットアップ手順](#セットアップ手順)
- [使用方法](#使用方法)
- [プロジェクト構造](#プロジェクト構造)
- [トラブルシューティング](#トラブルシューティング)

## 概要

このプロジェクトは、**Azure Speech Service**と**Microsoft Agent Framework**を組み合わせて、GPT-5と音声で対話できるAIチャットボットを構築するハンズオンです。

### 特徴

#### Phase 1-2: 基本機能
- ✅ **Speech-to-Text**: 日本語音声をリアルタイムでテキスト化
- ✅ **GPT-5との対話**: マルチターン会話に対応
- ✅ **Text-to-Speech**: 自然な日本語音声で応答
- ✅ **安全機構**: 無限ループ防止、エラーハンドリング

#### Phase 3: 高度な機能（✨ NEW）
- ✅ **音声コマンド**: 「要約して」「音声を変更して」などの音声操作
- ✅ **コンテキスト管理**: 会話の文脈を自動抽出・保持
- ✅ **会話要約**: これまでの対話を自動要約
- ✅ **音声プロファイル切り替え**: 5種類の音声から選択可能
- ✅ **話速調整**: リアルタイムで話速を変更（0.5x ~ 1.5x）

### 動作イメージ

```
🎤 ユーザー音声入力
    ↓
🔊 Speech-to-Text (Azure Speech Service)
    ↓
🤖 VoiceAgent処理 (GPT-5)
    ↓
🔉 Text-to-Speech (Azure Speech Service)
    ↓
🔊 音声出力
```

## システムアーキテクチャ

### 対話フロー

1. **音声入力**: ユーザーがマイクで質問
2. **音声認識**: Azure Speech Serviceでテキスト化
3. **エージェント処理**: GPT-5が応答を生成（会話履歴を保持）
4. **音声合成**: 応答テキストを自然な音声に変換
5. **音声出力**: スピーカーで再生

### 技術スタック

- **Microsoft Agent Framework** 1.0.0b251104
- **Azure Speech Service** (Speech-to-Text / Text-to-Speech)
- **Azure OpenAI Service** (GPT-5)
- **Python** 3.11+
- **uv** パッケージマネージャー

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

## セットアップ手順

### 1. リポジトリのクローン（既に実施済みの場合はスキップ）

```bash
git clone https://github.com/chinchillaa/agent-handson.git
cd agent-handson/02_azure-voice-chatbot
```

### 2. 依存パッケージのインストール

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

### 3. Azure設定

Azure Speech ServiceとAzure OpenAI Serviceの設定が必要です。

**詳細な設定手順は以下を参照してください**:
- **[Azure設定ガイド](../.azure/azure_settings.md)** - Azure Speech Service・Azure OpenAI Serviceの作成手順、環境変数設定、認証方法など

## 使用方法

### 基本的な使い方

```bash
# 音声対話を開始（Phase 2完了）
uv run python 02_azure-voice-chatbot/main.py
```

### 高度な機能デモ（Phase 3完了）

```bash
# Phase 3機能を体験（音声コマンド、コンテキスト管理、会話要約）
uv run python 02_azure-voice-chatbot/examples/advanced_chat.py
```

### 音声入出力のテスト（Phase 1）

```bash
# 音声認識・合成のテスト
uv run python 02_azure-voice-chatbot/examples/test_speech.py
```

## Phase 3: 音声コマンド機能

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
- デフォルト（明るく親しみやすい女性）
- 優しい（落ち着いた女性）
- 元気（明るく元気な女性）
- 落ち着いた男性
- 親しみやすい男性

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

## プロジェクト構造

```
02_azure-voice-chatbot/
├── agents/                    # エージェント定義
│   ├── __init__.py
│   ├── base.py               # ベースエージェント
│   └── voice_agent.py        # 音声対話エージェント（Phase 2）
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
├── examples/                  # 実行サンプル
│   ├── __init__.py
│   ├── test_speech.py        # 音声入出力テスト
│   └── simple_chat.py        # 音声対話例（Phase 2）
│
├── main.py                    # メインエントリーポイント（Phase 2）
├── voice_chat.py              # 音声対話ループ（Phase 2）
├── DESIGN.md                  # 設計ドキュメント
└── README.md                  # このファイル
```

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
- マイクを口に近づける
- バックグラウンドノイズを最小化
- マイクの品質を確認

### パッケージインストールエラー

```bash
# 依存関係を再インストール
uv sync --refresh
```

## 関連ドキュメント

- **設計ドキュメント**: [DESIGN.md](./DESIGN.md)
- **プロジェクトルート**: [../README.md](../README.md)
- **開発履歴**: [../PROJECT_HISTORY.md](../PROJECT_HISTORY.md)
- **開発ガイド**: [../CLAUDE.md](../CLAUDE.md)

## 参考資料

- [Azure Speech Service Documentation](https://learn.microsoft.com/azure/ai-services/speech-service/)
- [Speech SDK for Python](https://learn.microsoft.com/azure/ai-services/speech-service/quickstarts/setup-platform?pivots=programming-language-python)
- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework)
- [ソフトバンク技術ブログ - Azure Speech Service](https://www.softbank.jp/biz/blog/cloud-technology/articles/202410/azure-speech-service/)

---

**Azure AI Agent ハンズオンプロジェクト**
