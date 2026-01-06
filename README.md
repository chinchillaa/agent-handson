# 🚀 Azure AI Agent ハンズオン

**Azureで始める次世代AIエージェント開発 - すぐに実行できます！**

Microsoft Agent FrameworkとAzure OpenAI Service (GPT-5)を使って、実践的なAIエージェントシステムを体験するハンズオンプロジェクトです。

---

## 🎯 このハンズオンで学べること

### ✨ Azureの最新AI技術を体験
- **GPT-5**の驚異的な推論能力を実感
- **Azure Speech Service**による高精度音声認識（99%精度）
- **エンタープライズグレード**のセキュリティとスケーラビリティ

### 🛠️ 実践的なスキル習得
- **マルチエージェントシステム**の設計と実装
- **音声対話AI**の構築方法
- **Azure OpenAI Service**を使った本格的な開発体験

### 💡 すぐに使えるプロダクション品質のコード
- **環境準備済み** - すぐに実行可能
- 業務に応用できる実装パターン
- 17種類のカスタムツールを活用した拡張性の高い設計

---

## 🚀 クイックスタート

### ✅ 環境は準備済みです！

このVM環境には以下が既に設定されています：
- ✅ Python 3.11
- ✅ uv パッケージマネージャー
- ✅ 必要なライブラリ（すべてインストール済み）
- ✅ Azure API設定（.envファイル設定済み）
- ✅ プロジェクトコード

**すぐに実行できます！**

---

### 📋 STEP 1: ターミナルを開く

1. デスクトップの**ターミナル**アイコンをクリック
2. または、画面左上の「アクティビティ」→「ターミナル」を検索

### 🎤 STEP 2: マイクとスピーカーの設定（音声チャットボット用）

音声チャットボット（`02_azure-voice-chatbot`）を使用する場合は、ローカルPCのマイクをVMにリダイレクトする必要があります。

#### Windows リモートデスクトップの場合

1. **リモートデスクトップ接続を一旦切断**します
2. リモートデスクトップ接続を再度開きます
3. **「オプションの表示」**をクリック
4. **「ローカル リソース」**タブを選択
5. **「リモート オーディオ」**セクションの**「設定」**ボタンをクリック
6. 以下の2つを設定：
   - **リモート オーディオ再生**: 「**このコンピューターで再生する**」を選択
   - **リモート オーディオ録音**: 「**このコンピューターから録音する**」を選択
7. **「OK」**をクリック
8. **「接続」**をクリックしてVMに再接続

#### Mac/Linux の場合

Microsoft Remote Desktopアプリを使用している場合：
1. 接続設定を編集
2. 「Devices & Audio」セクション
3. 「Microphone」を「Redirect from this Mac/PC」に設定
4. 「Audio Output」を「Play on this Mac/PC」に設定

---

### 🤖 STEP 3: プロジェクトを実行

プロジェクトディレクトリに移動します：

```bash
cd /home/chinchilla/pjt/sbcs-work/agent-handson
```

#### 📊 プロジェクト1: マルチエージェント推論システム

4つのAIエージェントが協調して質問に回答します。

```bash
# プロジェクトディレクトリに移動
cd 01_multi-llm-reasoning

# 実行！（質問を指定）
uv run python main.py "量子コンピューターとは何ですか？"
```

**他にも試してみましょう：**

```bash
# 複雑な質問も可能
uv run python main.py "ブロックチェーン技術の仕組みと応用例を教えてください"

# インタラクティブモード（引数なしで対話的に質問）
uv run python main.py
```

**実行が完了したら、プロジェクトルートに戻ります：**

```bash
cd ..
```

---

#### 🎙️ プロジェクト2: 音声対話AIチャットボット

**重要**: STEP 2でマイクの設定を済ませていることを確認してください。

```bash
# プロジェクトディレクトリに移動
cd 02_azure-voice-chatbot

# 実行！
uv run python main.py
```

**使い方：**
1. プログラムが起動したら「何か話しかけてください...」と表示されます
2. マイクに向かって日本語で話しかけてください
   - 例: 「こんにちは」「今日の天気は？」「AIとは何ですか？」
3. AIが音声で応答します
4. 終了する場合は「終了」「さようなら」「バイバイ」などと言ってください

**音声コマンドも試してみましょう：**
- 「要約して」 - 会話の要約を表示
- 「音声を変更して」 - 音声を変更
- 「速く話して」 - 話速を上げる
- 「ゆっくり話して」 - 話速を下げる

**実行が完了したら、プロジェクトルートに戻ります：**

```bash
cd ..
```

---

## 📋 プロジェクト概要

### ✅ 01_multi-llm-reasoning
**4つのAIエージェントによる協調推論システム**

複数のAIエージェントが連携して、複雑な質問を分析・調査・統合する本格的なマルチエージェントシステムです。

#### 🌟 主な機能
- 🎯 **Coordinator**: 質問を分析し最適な調査計画を立案（GPT-5）
- 🔍 **Researcher**: Web検索で最新情報を収集（GPT-5-mini）
- 📊 **Analyzer**: データ分析とコードインタープリター（GPT-5）
- 📝 **Summarizer**: Markdown形式で読みやすい最終回答を生成（GPT-5）

#### 🛠️ カスタムツール 17種類搭載
- Web検索支援ツール（4個）
- データ分析ツール（5個）
- テキスト整形ツール（8個）

#### 💪 Azureの強み
- **GPT-5の高度な推論能力**で複雑な質問にも対応
- **GPT-5-miniの高速処理**でコスト効率良く情報収集
- **エンタープライズセキュリティ**で安心して利用可能

[📖 詳細ドキュメント](./01_multi-llm-reasoning/README.md)

---

### ✅ 02_azure-voice-chatbot
**Azure Speech Servicesで実現する音声対話AIチャットボット**

Azure Speech ServicesとAgent Frameworkを組み合わせた、**音声で対話できる**次世代AIアシスタントです。

#### 🌟 主な機能
- 🎤 **高精度音声認識**: Azure Speech Serviceによる99%の認識精度
- 🤖 **GPT-5との対話**: 自然で高度な会話を音声で実現
- 🔊 **自然な音声合成**: 5種類の日本語Neural Voiceから選択可能
- 🎙️ **音声コマンド対応**: 「要約して」「音声を変更して」などの直感的な操作

#### 💡 高度な機能
- 会話コンテキスト管理
- リアルタイム会話要約
- 音声プロファイル切り替え（5種類）
- 話速調整（0.5x ~ 1.5x）

#### 💪 Azureの強み
- **99%の音声認識精度**: ビジネス利用に耐える高品質
- **40言語以上対応**: グローバル展開も容易
- **Neural Voice**: 人間に近い自然な音声合成
- **低レイテンシ**: リアルタイム対話に最適

[📖 詳細ドキュメント](./02_azure-voice-chatbot/README.md)

---

## 🔧 トラブルシューティング

### よくある問題と解決方法

#### ❓ マイクが認識されない（音声チャットボット）

**原因**: ローカルマイクがVMにリダイレクトされていない

**解決方法**:
1. リモートデスクトップ接続を切断
2. 上記「STEP 2: マイクとスピーカーの設定」の手順を確認
3. 設定後、再接続してください

**確認方法**:
```bash
# マイクのテストスクリプトを実行
cd 02_azure-voice-chatbot
uv run python examples/test_speech.py
```

---

#### ❓ 音声が聞こえない

**原因**: スピーカー設定の問題

**解決方法**:
1. VM側の音量設定を確認（画面右上のスピーカーアイコン）
2. ローカルPCの音量設定を確認
3. リモートデスクトップのオーディオ設定を確認（STEP 2参照）

---

#### ❓ 「環境変数エラー」が出る

**原因**: .envファイルが見つからない（通常は発生しません）

**解決方法**:
```bash
# プロジェクトルートにいることを確認
cd /home/chinchilla/pjt/sbcs-work/agent-handson

# .envファイルの存在確認
ls -la .env

# ファイルが存在しない場合は主催者にお知らせください
```

---

#### ❓ プログラムが途中で止まる

**原因**: API呼び出しに時間がかかっている場合があります

**解決方法**:
- 少し待ってみてください（最大1-2分）
- それでも動かない場合は `Ctrl+C` で終了し、再実行してください

---

#### ❓ その他のエラー

わからないことがあれば、**気軽に主催者に質問してください！**

---

## 💪 なぜAzureなのか？

### 🌐 エンタープライズグレードのインフラ
- **99.9%のSLA保証**: ミッションクリティカルなシステムにも対応
- **グローバル展開**: 世界60以上のリージョンで利用可能
- **セキュリティとコンプライアンス**: SOC、ISO、HIPAAなど各種認証取得

### 🚀 最先端のAI技術
- **GPT-5**: OpenAIの最新モデルをいち早く利用可能
- **Azure OpenAI Service**: エンタープライズ向けAIプラットフォーム
- **継続的なアップデート**: 最新のAI技術を常に利用可能

### 💰 柔軟なコスト管理
- **従量課金制**: 使った分だけ支払い
- **GPT-5-mini**: 高速・低コストなオプション
- **無料枠**: 開発・テスト用のFreeティアあり

### 🔧 開発者フレンドリー
- **Microsoft Agent Framework**: 簡単にエージェントシステムを構築
- **豊富なSDK**: Python, .NET, Java, JavaScriptなど多言語対応
- **充実したドキュメント**: 日本語ドキュメントも豊富

---

## プロジェクト構造

```
agent-handson/
├── .env.example              # 環境変数のサンプル（詳細なコメント付き）
├── .env                      # 環境変数（設定済み）
├── pyproject.toml            # uv設定ファイル・依存関係
├── uv.lock                   # 依存パッケージのロックファイル
├── .venv/                    # 仮想環境（セットアップ済み）
├── README.md                 # このファイル
│
├── docs/                     # 📚 ドキュメント（整理済み）
│   ├── project/              # プロジェクト全体のドキュメント
│   │   ├── AGENTS.md         # エージェント設計概要
│   │   ├── CLAUDE.md         # 開発・主催者向けガイド
│   │   ├── PROJECT_HISTORY.md # 開発履歴
│   │   └── HANDSON_QUICKSTART.md # ハンズオン参加者向けガイド
│   ├── design/               # 設計ドキュメント
│   │   ├── 01_multi-llm-reasoning/
│   │   │   ├── DESIGN.md
│   │   │   ├── COST_ESTIMATES.md
│   │   │   └── PRICING_SOURCES.todo.md
│   │   └── 02_azure-voice-chatbot/
│   │       ├── DESIGN.md
│   │       └── COST_ESTIMATES.md
│   └── azure/                # Azure設定ドキュメント
│       ├── azure_settings.md
│       └── temp.md
│
├── 01_multi-llm-reasoning/   # ✅ マルチエージェント推論システム
│   ├── README.md             # 詳細ドキュメント
│   ├── main.py               # メインエントリーポイント
│   ├── workflow.py           # 4エージェント連携ワークフロー
│   │
│   ├── agents/               # エージェント実装
│   │   ├── base.py           # ベースエージェント
│   │   ├── coordinator.py    # 調査計画エージェント（GPT-5）
│   │   ├── researcher.py     # 情報収集エージェント（GPT-5-mini + Web検索）
│   │   ├── analyzer.py       # データ分析エージェント（GPT-5 + コードインタープリター）
│   │   └── summarizer.py     # 最終統合エージェント（GPT-5 + 整形ツール）
│   │
│   ├── config/               # 設定管理
│   │   └── settings.py       # Azure設定・デプロイメント名管理
│   │
│   ├── tools/                # カスタムツール（17種類）
│   │   ├── web_tools.py      # Web検索支援ツール（4個）
│   │   ├── analysis_tools.py # データ分析ツール（5個）
│   │   └── formatting_tools.py # テキスト整形ツール（8個）
│   │
│   └── examples/             # 実行サンプル
│       ├── simple_query.py   # シンプルな質問の例
│       └── complex_reasoning.py # 複雑な推論の例
│
└── 02_azure-voice-chatbot/   # ✅ 音声チャットボット
    ├── README.md             # 詳細ドキュメント
    ├── main.py               # メインエントリーポイント
    ├── voice_chat.py         # 音声対話ループ
    │
    ├── agents/               # エージェント定義
    │   ├── base.py           # ベースエージェント
    │   └── voice_agent.py    # 音声対話エージェント（GPT-5）
    │
    ├── speech/               # 音声処理モジュール
    │   ├── recognizer.py     # Speech-to-Text
    │   └── synthesizer.py    # Text-to-Speech
    │
    ├── config/               # 設定管理
    │   └── settings.py       # Azure設定
    │
    ├── tools/                # カスタムツール
    │   └── conversation_tools.py # 会話支援ツール
    │
    └── examples/             # 実行サンプル
        ├── test_speech.py    # 音声入出力テスト
        ├── simple_chat.py    # 基本音声対話
        └── advanced_chat.py  # 高度な機能デモ
```

---

## 技術スタック

- **言語**: Python 3.11+
- **パッケージマネージャー**: uv
- **エージェントフレームワーク**: Microsoft Agent Framework 1.0.0b251104
- **LLMプラットフォーム**: Azure OpenAI Service
  - GPT-5
  - GPT-5-mini
- **音声サービス**: Azure Speech Service
  - Speech-to-Text (音声認識)
  - Text-to-Speech (音声合成)
- **認証**: Azure Identity (API Key設定済み)
- **環境変数**: python-dotenv

---

## 📚 関連ドキュメント

### ハンズオン参加者向け
- **[01_multi-llm-reasoning/README.md](./01_multi-llm-reasoning/README.md)** - マルチエージェント推論システム詳細
- **[02_azure-voice-chatbot/README.md](./02_azure-voice-chatbot/README.md)** - 音声チャットボット詳細

### より詳しく知りたい方へ
- **[docs/project/HANDSON_QUICKSTART.md](./docs/project/HANDSON_QUICKSTART.md)** - ハンズオンガイド
- **[docs/project/AGENTS.md](./docs/project/AGENTS.md)** - エージェント設計概要
- **[docs/azure/azure_settings.md](./docs/azure/azure_settings.md)** - Azure詳細設定手順
- **[docs/project/PROJECT_HISTORY.md](./docs/project/PROJECT_HISTORY.md)** - 開発履歴

---

## 🎓 ハンズオン後の学習

### 継続学習したい方へ

ハンズオン終了後、自分のAzureアカウントで継続学習できます：

#### 1. Azureアカウントを作成
- https://azure.microsoft.com/free/
- 初回12ヶ月無料サービス + 200ドル分のクレジット

#### 2. 自分の環境でセットアップ

自分のPC/Macで開発する場合：

```bash
# 1. リポジトリをクローン
git clone https://github.com/chinchillaa/agent-handson.git
cd agent-handson

# 2. 環境変数を設定
cp .env.example .env
# .envファイルを編集して自分のAzure認証情報を設定

# 3. 依存パッケージをインストール
uv sync

# 4. 実行
cd 01_multi-llm-reasoning
uv run python main.py "量子コンピューターについて教えてください"
```

詳細な設定手順: [docs/azure/azure_settings.md](./docs/azure/azure_settings.md)

### おすすめの次のステップ

- **Azure OpenAI Service**: https://learn.microsoft.com/azure/ai-services/openai/
- **Microsoft Agent Framework**: https://github.com/microsoft/agent-framework
- **Azure Speech Service**: https://learn.microsoft.com/azure/ai-services/speech-service/

---

## 参考資料

- [Microsoft Agent Framework GitHub](https://github.com/microsoft/agent-framework)
- [Azure OpenAI Service Documentation](https://learn.microsoft.com/azure/ai-services/openai/)
- [Azure OpenAI Service Overview](https://azure.microsoft.com/products/ai-services/openai-service/)
- [Azure Speech Service Documentation](https://learn.microsoft.com/azure/ai-services/speech-service/)

---

## 🤝 貢献

このプロジェクトはAzure AIハンズオン用のサンプルプロジェクトです。
フィードバックや改善提案は Issue または Pull Request でお寄せください。

---

## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。

---

**Azureで次世代AIエージェント開発を体験しよう！** 🚀

質問があれば主催者または近くの参加者に気軽に声をかけてください。
