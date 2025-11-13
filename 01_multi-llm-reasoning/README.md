# Multi-LLM Reasoning System

Microsoft Agent FrameworkとAzure OpenAI Service (GPT-5)を使った
**4つのAIエージェントによる協調推論システム**

## 📋 目次

- [概要](#概要)
- [システムアーキテクチャ](#システムアーキテクチャ)
- [環境要件](#環境要件)
- [セットアップ手順](#セットアップ手順)
- [使用方法](#使用方法)
- [プロジェクト構造](#プロジェクト構造)
- [各エージェントの詳細](#各エージェントの詳細)
- [カスタムツール](#カスタムツール)
- [トラブルシューティング](#トラブルシューティング)

## 概要

このプロジェクトは、**4つの専門AIエージェント**が連携して複雑な質問に答えるマルチエージェント推論システムです。

### 特徴

- ✅ **4段階の推論プロセス**: Coordinator → Researcher → Analyzer → Summarizer
- ✅ **agent-framework活用**: Agent開発のフレームワークを使い、Web検索、データ分析など17種類のカスタムツールを使いこなすエージェントを実装
- ✅ **Azure OpenAI GPT-5**: 最新のGPT-5/GPT-5-miniモデルを活用
- ✅ **コマンドライン対応**: シンプルなCLIインターフェース
- ✅ **実行例付き**: すぐに試せるサンプルスクリプト

### 動作イメージ

```
ユーザー質問
    ↓
🎯 Coordinator (調査計画を立案)
    ↓
🔍 Researcher (Web検索で情報収集)
    ↓
📊 Analyzer (データ分析・洞察導出)
    ↓
📝 Summarizer (最終回答を生成)
    ↓
構造化された回答
```

## システムアーキテクチャ

### 4つのAIエージェント

| エージェント | 役割 | 使用モデル | 主な機能 |
|------------|------|-----------|---------|
| **Coordinator** | 調査計画の立案 | GPT-5 | 質問を分析し、調査項目を抽出 |
| **Researcher** | 情報収集 | GPT-5-mini | Web検索、情報整理 |
| **Analyzer** | データ分析 | GPT-5 | 統計分析、トレンド解析、洞察導出 |
| **Summarizer** | 最終統合 | GPT-5 | Markdown整形、結論生成 |

### 技術スタック

- **Microsoft Agent Framework** 1.0.0b251104
- **Azure OpenAI Service** (GPT-5 / GPT-5-mini)
- **Python** 3.11+
- **uv** パッケージマネージャー

## 環境要件

### 必須環境

- **Python**: 3.11以上
- **uv**: パッケージマネージャー（[インストール](https://github.com/astral-sh/uv)）
- **Azure環境**:
  - Azure サブスクリプション
  - Azure OpenAI Service リソース
  - GPT-5 / GPT-5-mini モデルのデプロイメント

### 推奨環境

- **Azure CLI**: 認証に使用（`az login`）
- **Git**: リポジトリのクローン

## セットアップ手順

### 🎓 ハンズオン参加者向けクイックスタート

**主催者から配布されたAPI Keyがある場合、こちらの簡単な手順で5分でセットアップ完了！**

1. **リポジトリをクローン**
   ```bash
   git clone https://github.com/chinchillaa/agent-handson.git
   cd agent-handson
   ```

2. **環境ファイルを作成**
   ```bash
   cp .env.example .env
   nano .env  # または vim/code .env
   ```

3. **配布されたAPI Keyを.envに設定**
   ```bash
   AZURE_OPENAI_ENDPOINT=配布されたエンドポイント
   AZURE_OPENAI_API_KEY=配布されたAPI_Key
   AZURE_OPENAI_DEPLOYMENT_GPT5=gpt-5
   AZURE_OPENAI_DEPLOYMENT_GPT5_MINI=gpt-5-mini
   ```

4. **依存パッケージをインストール**
   ```bash
   uv sync
   ```

5. **動作確認**
   ```bash
   cd 01_multi-llm-reasoning
   uv run python main.py "量子コンピューターとは？"
   ```

**詳細**: [ハンズオン参加者向けガイド](../.azure/azure_settings.md#-ハンズオン参加者向けクイックスタート)

---

### 💻 自分のAzureアカウントでセットアップする場合

**本格的に学習したい方・継続利用したい方向けの手順**

#### 1. リポジトリのクローン

```bash
git clone https://github.com/chinchillaa/agent-handson.git
cd agent-handson/01_multi-llm-reasoning
```

#### 2. 仮想環境のセットアップ

```bash
# uvで依存パッケージを一括インストール（仮想環境も自動作成）
uv sync
```

これにより、以下が自動的に実行されます：
- `.venv/` ディレクトリに仮想環境を作成
- `pyproject.toml` と `uv.lock` に基づいて依存パッケージをインストール

#### 3. Azure設定

Azure OpenAI Serviceの設定が必要です。

**詳細な設定手順は以下を参照してください**:
- **[Azure設定ガイド](../.azure/azure_settings.md)** - Azure OpenAI Serviceの作成手順、モデルデプロイメント、環境変数設定、認証方法など

## 使用方法

### 基本的な使い方

```bash
# コマンドライン引数で質問を指定
uv run python main.py "量子コンピューターについて詳しく教えてください"
```

### インタラクティブモード

```bash
# 引数なしで実行すると質問を入力できます
uv run python main.py
> 量子コンピューターについて詳しく教えてください
```

### オプション

```bash
# 各エージェントの詳細出力を表示
uv run python main.py "質問内容" --verbose

# 結果をMarkdownファイルに保存
uv run python main.py "質問内容" --save-output

# 出力先ディレクトリを指定
uv run python main.py "質問内容" --save-output --output-dir results/

# バナーを非表示
uv run python main.py "質問内容" --no-banner
```

### サンプルスクリプトの実行

```bash
# シンプルな質問の例
uv run python examples/simple_query.py

# 複雑な推論が必要な質問の例
uv run python examples/complex_reasoning.py
```

## プロジェクト構造

```
01_multi-llm-reasoning/
├── agents/                    # エージェント定義
│   ├── __init__.py
│   ├── base.py               # ベースエージェント
│   ├── coordinator.py        # 調査計画エージェント
│   ├── researcher.py         # 情報収集エージェント
│   ├── analyzer.py           # データ分析エージェント
│   └── summarizer.py         # 最終統合エージェント
│
├── config/                    # 設定ファイル
│   ├── __init__.py
│   └── settings.py           # Azure設定管理
│
├── tools/                     # カスタムツール
│   ├── __init__.py
│   ├── web_tools.py          # Web検索支援ツール
│   ├── analysis_tools.py     # データ分析ツール
│   └── formatting_tools.py   # テキスト整形ツール
│
├── examples/                  # 実行サンプル
│   ├── __init__.py
│   ├── simple_query.py       # シンプルな例
│   └── complex_reasoning.py  # 複雑な推論の例
│
├── workflow.py               # マルチエージェント連携
├── main.py                   # メインエントリーポイント
├── DESIGN.md                 # 設計ドキュメント
└── README.md                 # このファイル
```

## 各エージェントの詳細

### 🎯 Coordinator Agent

**役割**: ユーザーの質問を分析し、調査計画を立案

**使用モデル**: GPT-5

**出力例**:
```markdown
【調査項目】
1. 量子コンピューターの基本原理
2. 従来のコンピューターとの違い
3. 実用化の現状
4. 将来の応用分野
```

### 🔍 Researcher Agent

**役割**: Web検索などを使って情報を収集・整理

**使用モデル**: GPT-5-mini（高速・コスト効率）

**搭載ツール**:
- `HostedWebSearchTool` - Web検索（agent-framework組み込み）
- `extract_key_information` - キーワード抽出
- `summarize_search_results` - 検索結果要約
- `organize_information` - カテゴリ別整理
- `validate_sources` - 情報源の妥当性チェック

### 📊 Analyzer Agent

**役割**: 収集した情報を分析し、洞察を導出

**使用モデル**: GPT-5

**搭載ツール**:
- `HostedCodeInterpreterTool` - コード実行・グラフ作成
- `calculate_statistics` - 基本統計量計算
- `compare_data` - データセット比較
- `extract_numbers_from_text` - 数値抽出
- `analyze_trend` - トレンド分析
- `categorize_data` - データ分類

### 📝 Summarizer Agent

**役割**: 全エージェントの出力を統合し、最終回答を生成

**使用モデル**: GPT-5

**搭載ツール**:
- `format_as_markdown` - Markdown整形
- `create_bullet_list` - 箇条書き作成
- `structure_as_json` - JSON構造化
- `create_summary_table` - テーブル作成
- `highlight_key_points` - キーワード強調
- `format_conclusion` - 結論セクション整形
- `clean_text` - テキストクリーンアップ
- `add_metadata` - メタデータ追加

## カスタムツール

このシステムには**17種類のカスタムツール**が実装されています。

### Web検索支援ツール（4個）

- `extract_key_information` - テキストからキーワード抽出
- `summarize_search_results` - 検索結果の要約
- `organize_information` - 情報のカテゴリ分類
- `validate_sources` - 情報源の妥当性チェック

### データ分析ツール（5個）

- `calculate_statistics` - 平均、中央値、標準偏差などの計算
- `compare_data` - 2つのデータセットの比較
- `extract_numbers_from_text` - テキストから数値を抽出
- `analyze_trend` - データの増加・減少傾向を分析
- `categorize_data` - 閾値に基づくデータ分類

### テキスト整形ツール（8個）

- `format_as_markdown` - 辞書データをMarkdown形式に整形
- `create_bullet_list` - 箇条書きリストの作成
- `structure_as_json` - JSON形式での構造化
- `create_summary_table` - Markdownテーブルの作成
- `highlight_key_points` - キーワードの強調表示
- `format_conclusion` - 結論セクションの整形
- `clean_text` - 余分な空白・改行の削除
- `add_metadata` - メタデータの追加

## トラブルシューティング

Azure関連のトラブルシューティングは **[Azure設定ガイド - トラブルシューティング](../.azure/azure_settings.md#トラブルシューティング)** を参照してください。

### パッケージインストールエラー

```bash
# 依存関係を再インストール
uv sync --refresh
```

### その他の問題

詳細なログを確認するには、`--verbose` オプションを使用してください：

```bash
uv run python main.py "質問内容" --verbose
```

## 関連ドキュメント

- **プロジェクトルート**: [../README.md](../README.md)
- **設計ドキュメント**: [DESIGN.md](./DESIGN.md)
- **開発履歴**: [../PROJECT_HISTORY.md](../PROJECT_HISTORY.md)
- **開発ガイド**: [../CLAUDE.md](../CLAUDE.md)

## ライセンス

このプロジェクトはハンズオン・学習目的で作成されています。

---

**Azure AI Agent ハンズオンプロジェクト**
