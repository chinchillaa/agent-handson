# Azure AI Agent ハンズオン

Microsoft Agent FrameworkとAzure OpenAI Service (GPT-5)を使ったAIエージェントハンズオン

## 📋 プロジェクト概要

このリポジトリには2つのAIエージェントハンズオンプロジェクトが含まれています。

### ✅ 01_multi-llm-reasoning（実装完了）
**4つのAIエージェントによる協調推論システム**

- **概要**: Coordinator、Researcher、Analyzer、Summarizerの4エージェントが連携して複雑な推論タスクを実行
- **実装状況**: ✅ **完全実装済み**（Phase 1-4完了）
- **主な機能**:
  - 🎯 Coordinator: 質問を分析し調査計画を立案
  - 🔍 Researcher: Web検索で最新情報を収集（GPT-5-mini）
  - 📊 Analyzer: データ分析とコードインタープリター
  - 📝 Summarizer: Markdown形式で最終回答を生成
  - 🛠️ **17種類のカスタムツール**搭載（Web検索支援、データ分析、テキスト整形）
- **使用技術**: Microsoft Agent Framework、Azure OpenAI Service (GPT-5/GPT-5-mini)
- **詳細**: [01_multi-llm-reasoning/README.md](./01_multi-llm-reasoning/README.md)

### 🚧 02_azure-voice-chatbot（未実装）
**Azure音声サービスを使ったマルチエージェント音声チャットボット**

- **概要**: Azure Speech Servicesとagent-frameworkを使った音声対話システム
- **実装状況**: 🚧 未実装
- **使用技術**: Azure Speech Services、Microsoft Agent Framework

## 🚀 クイックスタート

```bash
# 1. リポジトリをクローン
git clone https://github.com/chinchillaa/agent-handson.git
cd agent-handson

# 2. 依存パッケージをインストール（仮想環境も自動作成）
uv sync

# 3. 環境変数を設定
cp .env.example .env
# .envファイルを編集してAzure OpenAI認証情報を設定

# 4. Azure認証（Azure CLI使用の場合）
az login

# 5. 実行！
uv run python 01_multi-llm-reasoning/main.py "量子コンピューターについて教えてください"
```

詳細なセットアップ手順は [セットアップ手順](#セットアップ手順) を参照してください。

## 環境要件

### 必須環境

- **Python**: 3.11以上
- **uv**: パッケージマネージャー（[インストール方法](https://github.com/astral-sh/uv)）
- **Azure環境**:
  - Azure サブスクリプション
  - Azure OpenAI Service リソース
  - GPT-5 / GPT-5-mini モデルのデプロイメント
- **Git**: リポジトリのクローン用

### 推奨環境

- **Azure CLI**: 認証に使用（`az login`）
- **Visual Studio Code**: 開発・デバッグ用

## セットアップ手順

### 1. リポジトリのクローン

```bash
git clone https://github.com/chinchillaa/agent-handson.git
cd agent-handson
```

### 2. 環境変数の設定

```bash
# .env.exampleをコピー
cp .env.example .env

# .envファイルを編集してAzure OpenAIの認証情報を設定
# 必須項目（.envファイルに記載）:
# - AZURE_OPENAI_ENDPOINT
# - AZURE_OPENAI_DEPLOYMENT_GPT5
# - AZURE_OPENAI_DEPLOYMENT_GPT5_MINI
# - その他の認証情報
```

### 3. Azureへのログイン（推奨）

```bash
# Azure CLIでログイン
az login

# サブスクリプションの確認
az account show
```

または、API Keyを使用する場合は`.env`ファイルに`AZURE_OPENAI_API_KEY`を設定してください。

### 4. 依存パッケージのインストール

```bash
# uvで依存パッケージを一括インストール
# 仮想環境が自動的に作成されます（既に存在する場合は使用されます）
uv sync
```

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

### 🚧 02_azure-voice-chatbot の実行

```bash
# 音声チャットボットを起動（未実装）
uv run python 02_azure-voice-chatbot/main.py
```

**注意**: このプロジェクトは現在未実装です。

## プロジェクト構造

```
agent-handson/
├── .env.example              # 環境変数のサンプル（詳細なコメント付き）
├── .env                      # 環境変数（.gitignoreに含まれる）
├── pyproject.toml            # uv設定ファイル・依存関係
├── uv.lock                   # 依存パッケージのロックファイル
├── .venv/                    # 仮想環境（uv syncで自動作成）
├── README.md                 # このファイル
├── PROJECT_HISTORY.md        # 開発履歴
├── CLAUDE.md                 # 開発ガイド
│
├── 01_multi-llm-reasoning/   # ✅ マルチエージェント推論システム（実装完了）
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
└── 02_azure-voice-chatbot/   # 🚧 音声チャットボット（未実装）
    └── README.md
```

## 技術スタック

- **言語**: Python 3.11+
- **パッケージマネージャー**: uv
- **エージェントフレームワーク**: Microsoft Agent Framework 1.0.0b251104
- **LLMプラットフォーム**: Azure AI Foundry (Azure OpenAI Service)
  - GPT-5
  - GPT-5-mini
- **認証**: Azure Identity (Azure CLI or API Key)
- **環境変数**: python-dotenv

## トラブルシューティング

### Azure認証エラーの場合

```bash
# Azure CLIで再ログイン
az login

# サブスクリプション一覧を確認
az account show
```

### パッケージのインストールエラー

```bash
# uvのキャッシュをクリア
uv cache clean

# 再インストール
uv sync
```

### 環境変数が読み込まれない

- `.env`ファイルがプロジェクトルート（agent-handson/）に配置されているか確認
- `.env`ファイルの各行が正しくKEY=VALUE形式になっているか確認

## 貢献

このプロジェクトはハンズオン用のサンプルプロジェクトです。

## 参考資料

- [Microsoft Agent Framework GitHub](https://github.com/microsoft/agent-framework)
- [Azure AI Foundry Documentation](https://learn.microsoft.com/azure/ai-foundry/)
- [Azure OpenAI Service Documentation](https://learn.microsoft.com/azure/ai-services/openai/)
- [GPT-5 in Azure AI Foundry](https://azure.microsoft.com/en-us/blog/gpt-5-in-azure-ai-foundry-the-future-of-ai-apps-and-agents-starts-here/)
