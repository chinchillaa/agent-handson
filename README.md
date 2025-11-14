# 🚀 Azure AI Agent ハンズオン

**Azureで始める次世代AIエージェント開発 - 5分でスタート！**

Microsoft Agent FrameworkとAzure OpenAI Service (GPT-5)を使って、実践的なAIエージェントシステムを構築するハンズオンプロジェクトです。

---

## 🎯 このハンズオンで学べること

### ✨ Azureの最新AI技術を体験
- **GPT-5**の驚異的な推論能力を実感
- **Azure Speech Service**による高精度音声認識（99%精度）
- **エンタープライズグレード**のセキュリティとスケーラビリティ

### 🛠️ 実践的なスキル習得
- **マルチエージェントシステム**の設計と実装
- **音声対話AI**の構築方法
- **Azure AI Foundry**を使った本格的な開発体験

### 💡 すぐに使えるプロダクション品質のコード
- git cloneして**5分で動く**サンプル
- 業務に応用できる実装パターン
- 17種類のカスタムツールを活用した拡張性の高い設計

---

## 🎓 ハンズオン参加者の方へ

**まずはこちら！ 最短5分でセットアップ完了** 👇

### 📘 [HANDSON_QUICKSTART.md](./HANDSON_QUICKSTART.md)

主催者から配布されたAPI Keyがあれば、すぐに始められます：

```bash
# 1. クローン
git clone https://github.com/chinchillaa/agent-handson.git
cd agent-handson

# 2. 環境設定
cp .env.example .env
# .envに配布されたAPI Keyを設定

# 3. インストール
uv sync

# 4. 実行！
cd 01_multi-llm-reasoning
uv run python main.py "量子コンピューターとは何ですか？"
```

**詳細は [HANDSON_QUICKSTART.md](./HANDSON_QUICKSTART.md) をご覧ください**

---

## 📋 プロジェクト概要

### ✅ 01_multi-llm-reasoning（Phase 1-4 完了）
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

### ✅ 02_azure-voice-chatbot（Phase 1-3 完了）
**Azure Speech Servicesで実現する音声対話AIチャットボット**

Azure Speech ServicesとAgent Frameworkを組み合わせた、**音声で対話できる**次世代AIアシスタントです。

#### 🌟 主な機能
- 🎤 **高精度音声認識**: Azure Speech Serviceによる99%の認識精度
- 🤖 **GPT-5との対話**: 自然で高度な会話を音声で実現
- 🔊 **自然な音声合成**: 5種類の日本語Neural Voiceから選択可能
- 🎙️ **音声コマンド対応**: 「要約して」「音声を変更して」などの直感的な操作

#### 💡 Phase 3 完了機能
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

## 🚀 クイックスタート

### 🎓 ハンズオン参加者向け（推奨）

**所要時間: 5分**

詳細は **[HANDSON_QUICKSTART.md](./HANDSON_QUICKSTART.md)** をご覧ください

```bash
git clone https://github.com/chinchillaa/agent-handson.git
cd agent-handson
cp .env.example .env
# .envに配布されたAPI Keyを設定
uv sync
cd 01_multi-llm-reasoning
uv run python main.py "量子コンピューターとは何ですか？"
```

---

### 💻 自分のAzureアカウントで試したい方向け

**所要時間: 15-30分（Azure設定を含む）**

#### 1. Azureリソースの準備

以下のAzureリソースが必要です：
- **Azure OpenAI Service** (GPT-5 / GPT-5-mini デプロイ)
- **Azure Speech Service** (音声認識・合成用)

詳細な作成手順: [.azure/azure_settings.md](./.azure/azure_settings.md)

#### 2. リポジトリのセットアップ

```bash
# 1. リポジトリをクローン
git clone https://github.com/chinchillaa/agent-handson.git
cd agent-handson

# 2. 環境変数を設定
cp .env.example .env
# .envファイルを編集してAzure認証情報を設定

# 3. Azure認証（Azure CLI使用の場合）
az login

# 4. 依存パッケージをインストール
uv sync

# 5. 実行
uv run python 01_multi-llm-reasoning/main.py "量子コンピューターについて教えてください"
```

---

## 環境要件

### 必須環境

- **Python**: 3.11以上
- **uv**: パッケージマネージャー（[インストール方法](https://github.com/astral-sh/uv)）
- **Azure環境**:
  - Azure サブスクリプション
  - Azure OpenAI Service リソース
  - GPT-5 / GPT-5-mini モデルのデプロイメント
  - Azure Speech Service リソース（音声チャットボット用）
- **Git**: リポジトリのクローン用

### 推奨環境

- **Azure CLI**: 認証に使用（`az login`）
- **Visual Studio Code**: 開発・デバッグ用
- **マイクとスピーカー**: 音声チャットボット用

---

## 使用方法

### 📊 01_multi-llm-reasoning の実行

#### 基本的な使い方

```bash
# コマンドライン引数で質問を指定
uv run python 01_multi-llm-reasoning/main.py "量子コンピューターについて詳しく教えてください"

# インタラクティブモード（引数なし）
uv run python 01_multi-llm-reasoning/main.py

# 詳細出力（各エージェントの出力を表示）
uv run python 01_multi-llm-reasoning/main.py "質問内容" --verbose

# 結果をMarkdownファイルに保存
uv run python 01_multi-llm-reasoning/main.py "質問内容" --save-output
```

#### サンプルスクリプトの実行

```bash
# シンプルな質問の例
uv run python 01_multi-llm-reasoning/examples/simple_query.py

# 複雑な推論が必要な質問の例
uv run python 01_multi-llm-reasoning/examples/complex_reasoning.py
```

詳細は [01_multi-llm-reasoning/README.md](./01_multi-llm-reasoning/README.md) を参照してください。

---

### 🎙️ 02_azure-voice-chatbot の実行

#### 基本的な使い方

```bash
# 音声対話を開始
cd 02_azure-voice-chatbot
uv run python main.py
```

マイクに向かって話しかけると、AIが音声で応答します。

#### Phase 3: 高度な機能デモ

```bash
# 音声コマンド機能を体験
uv run python examples/advanced_chat.py
```

**使える音声コマンド**:
- 「要約して」 - 会話の要約を表示
- 「音声を変更して」 - 音声プロファイルを切り替え
- 「速く話して」 - 話速を上げる
- 「ゆっくり話して」 - 話速を下げる
- 「音声をリセット」 - デフォルト設定に戻す

詳細は [02_azure-voice-chatbot/README.md](./02_azure-voice-chatbot/README.md) を参照してください。

---

## プロジェクト構造

```
agent-handson/
├── .env.example              # 環境変数のサンプル（詳細なコメント付き）
├── .env                      # 環境変数（.gitignoreに含まれる）
├── pyproject.toml            # uv設定ファイル・依存関係
├── uv.lock                   # 依存パッケージのロックファイル
├── .venv/                    # 仮想環境（uv syncで自動作成）
├── README.md                 # このファイル
├── HANDSON_QUICKSTART.md     # 🎓 ハンズオン参加者向けクイックスタート
├── PROJECT_HISTORY.md        # 開発履歴
├── CLAUDE.md                 # 開発・主催者向けガイド
│
├── .azure/                   # Azure設定ドキュメント
│   └── azure_settings.md     # Azure OpenAI/Speechの詳細設定手順
│
├── 01_multi-llm-reasoning/   # ✅ マルチエージェント推論システム（Phase 1-4完了）
│   ├── README.md             # 詳細ドキュメント
│   ├── DESIGN.md             # 設計ドキュメント
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
└── 02_azure-voice-chatbot/   # ✅ 音声チャットボット（Phase 1-3完了）
    ├── README.md             # 詳細ドキュメント
    ├── DESIGN.md             # 設計ドキュメント
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
        └── advanced_chat.py  # Phase 3機能デモ
```

---

## 💪 なぜAzureなのか？

### 🌐 エンタープライズグレードのインフラ
- **99.9%のSLA保証**: ミッションクリティカルなシステムにも対応
- **グローバル展開**: 世界60以上のリージョンで利用可能
- **セキュリティとコンプライアンス**: SOC、ISO、HIPAAなど各種認証取得

### 🚀 最先端のAI技術
- **GPT-5**: OpenAIの最新モデルをいち早く利用可能
- **Azure AI Foundry**: 包括的なAI開発プラットフォーム
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

## 技術スタック

- **言語**: Python 3.11+
- **パッケージマネージャー**: uv
- **エージェントフレームワーク**: Microsoft Agent Framework 1.0.0b251104
- **LLMプラットフォーム**: Azure AI Foundry (Azure OpenAI Service)
  - GPT-5
  - GPT-5-mini
- **音声サービス**: Azure Speech Service
  - Speech-to-Text (音声認識)
  - Text-to-Speech (音声合成)
- **認証**: Azure Identity (Azure CLI or API Key)
- **環境変数**: python-dotenv

---

## トラブルシューティング

### 🎓 ハンズオン参加者向け

詳細は **[HANDSON_QUICKSTART.md - トラブルシューティング](./HANDSON_QUICKSTART.md#-トラブルシューティング)** をご覧ください

よくある質問：
- Q: 環境変数エラーが出る → `.env`ファイルがプロジェクトルートにあるか確認
- Q: マイクが認識されない → マイク接続・権限設定を確認
- Q: その他のエラー → 主催者にご質問ください

### 💻 自分のAzureアカウント使用時

#### Azure認証エラーの場合

```bash
# Azure CLIで再ログイン
az login

# サブスクリプション一覧を確認
az account show
```

#### パッケージのインストールエラー

```bash
# uvのキャッシュをクリア
uv cache clean

# 再インストール
uv sync
```

#### 環境変数が読み込まれない

- `.env`ファイルがプロジェクトルート（agent-handson/）に配置されているか確認
- `.env`ファイルの各行が正しくKEY=VALUE形式になっているか確認

詳細な設定手順: [.azure/azure_settings.md - トラブルシューティング](./.azure/azure_settings.md#トラブルシューティング)

---

## 📚 関連ドキュメント

### ハンズオン参加者向け
- **[HANDSON_QUICKSTART.md](./HANDSON_QUICKSTART.md)** - 5分でスタート！
- **[01_multi-llm-reasoning/README.md](./01_multi-llm-reasoning/README.md)** - マルチエージェント推論システム詳細
- **[02_azure-voice-chatbot/README.md](./02_azure-voice-chatbot/README.md)** - 音声チャットボット詳細

### 開発者・主催者向け
- **[CLAUDE.md](./CLAUDE.md)** - 開発・主催者向けガイド
- **[.azure/azure_settings.md](./.azure/azure_settings.md)** - Azure詳細設定手順
- **[PROJECT_HISTORY.md](./PROJECT_HISTORY.md)** - 開発履歴

---

## 🎓 ハンズオン後の学習

### 継続学習したい方へ

ハンズオン終了後、自分のAzureアカウントで継続学習できます：

1. **Azureアカウントを作成**: https://azure.microsoft.com/free/
   - 初回12ヶ月無料サービス + 200ドル分のクレジット
2. **Azure CLIをインストール**: [.azure/azure_settings.md](./.azure/azure_settings.md)の「共通設定」参照
3. **自分のリソースを作成**: [.azure/azure_settings.md](./.azure/azure_settings.md)の各プロジェクト設定を参照

### おすすめの次のステップ

- **Azure AI Foundry**: https://ai.azure.com/
- **Microsoft Agent Framework**: https://github.com/microsoft/agent-framework
- **Azure OpenAI Service ドキュメント**: https://learn.microsoft.com/azure/ai-services/openai/
- **Azure Speech Service ドキュメント**: https://learn.microsoft.com/azure/ai-services/speech-service/

---

## 参考資料

- [Microsoft Agent Framework GitHub](https://github.com/microsoft/agent-framework)
- [Azure AI Foundry Documentation](https://learn.microsoft.com/azure/ai-foundry/)
- [Azure OpenAI Service Documentation](https://learn.microsoft.com/azure/ai-services/openai/)
- [GPT-5 in Azure AI Foundry](https://azure.microsoft.com/en-us/blog/gpt-5-in-azure-ai-foundry-the-future-of-ai-apps-and-agents-starts-here/)
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
