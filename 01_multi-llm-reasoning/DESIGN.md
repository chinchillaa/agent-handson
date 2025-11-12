# マルチLLM推論システム 設計計画書

## システム概要

Azure OpenAI Serviceを活用し、複数のAIエージェントが協調してユーザーの質問に対して高度な推論を行うシステムを構築します。Microsoft Agent Frameworkのグラフベースワークフロー機能を使用して、エージェント間の効率的な連携を実現します。

## アーキテクチャ設計

### エージェント構成

本システムは4つの専門エージェントで構成されます：

1. **Coordinator Agent (コーディネーター)**
   - 役割: ユーザーの質問を受け取り、タスクを分析・分配
   - 機能: 質問の意図理解、タスク分解、エージェント間の調整
   - 使用モデル: Azure OpenAI **gpt-5**

2. **Research Agent (リサーチャー)**
   - 役割: 情報収集・調査を担当
   - 機能: 必要な情報の特定、データ収集、事実確認
   - 使用モデル: Azure OpenAI **gpt-5-mini**

3. **Analysis Agent (アナライザー)**
   - 役割: データ分析・論理的推論を担当
   - 機能: データ解析、論理的思考、仮説検証
   - 使用モデル: Azure OpenAI **gpt-5**

4. **Summary Agent (サマライザー)**
   - 役割: 各エージェントの結果を統合・要約
   - 機能: 情報統合、最終回答生成、品質チェック
   - 使用モデル: Azure OpenAI **gpt-5**

### 使用するLLMモデル（Azure OpenAI Service - GPT-5ファミリー）

**主要モデル:**
- **gpt-5**: ロジック重視・マルチステップタスク用
  - Coordinator、Analysis、Summaryエージェントで使用
  - 複雑な推論と高度な論理処理に最適
- **gpt-5-mini**: コスト効率重視の軽量版
  - Researchエージェントで使用
  - 情報収集タスクに最適化

**特徴:**
- Azureの高セキュリティ環境で稼働（Azure AI Foundry）
- エンタープライズグレードのSLA
- Azure Identity統合による安全な認証
- OpenTelemetryによる詳細な観測可能性
- 利用可能リージョン: East US 2, Sweden Central

**GPT-5の主な改善点:**
- より高度な推論能力とマルチステップタスク処理
- 長いコンテキストウィンドウ
- 改善された精度と一貫性
- マルチモーダル対応の強化

### Agent Frameworkの活用機能

1. **グラフベースワークフロー**
   - エージェント間の依存関係を明示的に定義
   - ストリーミング対応
   - チェックポイント機能（状態保存・復元）
   - タイムトラベル機能（実行履歴の再現）

2. **DevUI**
   - インタラクティブな開発・テストインターフェース
   - エージェントの動作確認
   - デバッグ支援

3. **観測可能性（Observability）**
   - OpenTelemetry統合
   - 分散トレーシング
   - パフォーマンス監視
   - ログ集約

4. **Human-in-the-Loop**
   - 人間による確認・承認フロー
   - インタラクティブな意思決定支援

## ディレクトリ構造

agent-frameworkの推奨パターンに従った実践的な構造：

```
01_multi-llm-reasoning/
├── README.md                 # ハンズオン説明
├── DESIGN.md                 # 本設計書
├── .env.example              # 環境変数テンプレート
├── .env                      # 実際の環境変数（gitignore）
├── requirements.txt          # 依存パッケージ
│
├── agents/                   # エージェント定義
│   ├── __init__.py
│   ├── base.py              # 共通エージェント基底クラス
│   ├── coordinator.py       # コーディネーターエージェント
│   ├── researcher.py        # リサーチエージェント
│   ├── analyzer.py          # 分析エージェント
│   └── summarizer.py        # サマリーエージェント
│
├── workflow.py               # マルチエージェントワークフロー
├── main.py                   # メインエントリーポイント
│
├── tools/                    # カスタムツール定義（オプション）
│   ├── __init__.py
│   └── custom_tools.py
│
├── config/                   # 設定管理
│   ├── __init__.py
│   └── settings.py          # 環境変数読み込み
│
└── examples/                 # 実行例
    ├── simple_query.py      # シンプルな質問例
    └── complex_reasoning.py # 複雑な推論例
```

## 実装ステップ

### Phase 1: 環境セットアップ

1. **プロジェクト初期化**
   ```bash
   mkdir -p agents config tools examples
   touch .env.example requirements.txt
   ```

2. **依存パッケージインストール**
   ```bash
   uv add agent-framework --pre
   uv add python-dotenv azure-identity
   ```

3. **環境変数設定**
   - `.env.example` を `.env` にコピー
   - Azure OpenAI の設定を記入
   - Azure CLI認証: `az login`

### Phase 2: エージェント実装

4. **共通基底クラス作成** (`agents/base.py`)
   ```python
   from agent_framework import ChatAgent
   from agent_framework.azure import AzureOpenAIChatClient
   from azure.identity.aio import AzureCliCredential

   async def create_azure_agent(name: str, instructions: str, model: str):
       """Azure OpenAI エージェントを作成"""
       credential = AzureCliCredential()
       client = AzureOpenAIChatClient(
           credential=credential,
           deployment_name=model
       )
       return ChatAgent(
           chat_client=client,
           name=name,
           instructions=instructions
       )
   ```

5. **各エージェントの実装**
   - `coordinator.py`: タスク分析・調整
   - `researcher.py`: 情報収集
   - `analyzer.py`: 論理分析
   - `summarizer.py`: 統合・要約

6. **システムプロンプト設計**
   - 各エージェントの役割を明確に定義
   - 出力フォーマットの指定
   - エージェント間の連携方法を記述

### Phase 3: ワークフロー構築

7. **シーケンシャルワークフロー実装** (`workflow.py`)
   ```python
   import asyncio
   from agents import coordinator, researcher, analyzer, summarizer

   async def run_reasoning_workflow(user_query: str):
       # 1. Coordinator: タスク分析
       coord_result = await coordinator.run(user_query)

       # 2. Researcher: 情報収集
       research_result = await researcher.run(coord_result.text)

       # 3. Analyzer: 論理分析
       analysis_result = await analyzer.run(research_result.text)

       # 4. Summary: 統合
       final_result = await summarizer.run(analysis_result.text)

       return final_result
   ```

8. **並列処理の追加（オプション）**
   ```python
   # 複数の調査を並列実行
   results = await asyncio.gather(
       researcher1.run(task1),
       researcher2.run(task2)
   )
   ```

### Phase 4: 統合とテスト

9. **メインアプリケーション実装** (`main.py`)
   - コマンドライン引数処理
   - ワークフロー実行
   - 結果の表示

10. **実行例の作成** (`examples/`)
    - シンプルなクエリ例
    - 複雑な推論タスク例

11. **動作確認**
    ```bash
    python main.py "量子コンピュータの将来性について分析してください"
    ```

12. **DevUI統合（オプション）**
    - ワークフローの可視化
    - ステップごとのデバッグ

## 機能仕様

### 基本フロー

**非同期実行パターン（asyncio使用）:**

```python
import asyncio
from agents import create_coordinator, create_researcher, create_analyzer, create_summarizer

async def main():
    # 1. 入力受付
    user_query = "量子コンピュータが金融業界に与える影響を分析してください"

    # 2. エージェント初期化
    coordinator = await create_coordinator()
    researcher = await create_researcher()
    analyzer = await create_analyzer()
    summarizer = await create_summarizer()

    # 3. シーケンシャル実行
    print("📋 Coordinator: タスク分析中...")
    coord_result = await coordinator.run(user_query)

    print("🔍 Researcher: 情報収集中...")
    research_result = await researcher.run(coord_result.text)

    print("📊 Analyzer: 論理分析中...")
    analysis_result = await analyzer.run(research_result.text)

    print("✍️ Summarizer: 結果統合中...")
    final_result = await summarizer.run(analysis_result.text)

    # 4. 出力
    print("\n=== 最終結果 ===")
    print(final_result.text)

if __name__ == "__main__":
    asyncio.run(main())
```

### ChatAgentの基本機能

**1. 標準実行**
```python
result = await agent.run("質問内容")
print(result.text)
```

**2. ストリーミング実行**
```python
async for chunk in agent.run_stream("質問内容"):
    print(chunk, end="", flush=True)
```

**3. 会話履歴の管理**
```python
# エージェントは自動的に会話履歴を保持
result1 = await agent.run("最初の質問")
result2 = await agent.run("前の回答についてもっと詳しく教えて")
```

### カスタムツールの定義（オプション）

```python
def search_database(query: str) -> str:
    """データベースを検索する"""
    # 実装
    return f"検索結果: {query}"

def calculate(expression: str) -> float:
    """数式を計算する"""
    return eval(expression)

# ツールを持つエージェント
agent = ChatAgent(
    chat_client=client,
    name="Researcher",
    instructions="あなたは調査エージェントです",
    tools=[search_database, calculate]
)
```

### 並列処理パターン

```python
# 複数のリサーチを並列実行
async def parallel_research(topics: list[str]):
    tasks = [
        researcher.run(f"{topic}について調査してください")
        for topic in topics
    ]
    results = await asyncio.gather(*tasks)
    return results
```

### 拡張機能（オプション）

**1. Human-in-the-Loop**
```python
# 重要な判断時に人間の承認を要求
if needs_approval:
    approval = input("この分析を続行しますか？ (y/n): ")
    if approval.lower() != 'y':
        return "処理を中断しました"
```

**2. エラーハンドリング**
```python
try:
    result = await agent.run(query)
except Exception as e:
    print(f"エラー: {e}")
    # リトライロジック
```

**3. ログ記録**
```python
import logging
logging.basicConfig(level=logging.INFO)

# agent-frameworkが自動的にログを出力
```

**4. タイムアウト設定**
```python
import asyncio

try:
    result = await asyncio.wait_for(
        agent.run(query),
        timeout=60.0  # 60秒
    )
except asyncio.TimeoutError:
    print("タイムアウトしました")
```

## 技術スタック

### コア技術
- **フレームワーク**: Microsoft Agent Framework 1.0.0b251104
- **言語**: Python 3.11+
- **LLMプロバイダー**: Azure AI Foundry (Azure OpenAI Service)
  - **gpt-5** (Coordinator, Analysis, Summary)
  - **gpt-5-mini** (Research)

### Azure サービス
- **Azure AI Foundry**: 次世代AIプラットフォーム
- **Azure OpenAI Service**: GPT-5モデルホスティング
- **Azure Identity**: 認証・認可
- **Azure Monitor**: 監視・ログ（オプション）

### Python パッケージ

**requirements.txt:**
```txt
# Agent Framework（プレリリース版）
agent-framework==1.0.0b251104

# Azure認証
azure-identity>=1.25.0

# 環境変数管理
python-dotenv>=1.2.0

# オプション: 追加機能
# pydantic>=2.0.0  # データバリデーション
# opentelemetry-api>=1.20.0  # トレーシング
```

**インストールコマンド:**
```bash
uv pip install -r requirements.txt
# または
uv pip install agent-framework --pre
```

## 認証方法

### 方法1: Azure CLI認証（推奨）

**ステップ1: Azure CLIでログイン**
```bash
az login
az account show  # サブスクリプション確認
```

**ステップ2: Pythonコードで使用**
```python
from azure.identity.aio import AzureCliCredential
from agent_framework.azure import AzureOpenAIChatClient
from agent_framework import ChatAgent

async def create_agent():
    # AzureCliCredentialを使用（非同期版）
    credential = AzureCliCredential()

    # Azure OpenAI チャットクライアント
    client = AzureOpenAIChatClient(
        credential=credential,
        endpoint="https://your-resource.openai.azure.com/",
        deployment_name="gpt-5"
    )

    # エージェント作成
    agent = ChatAgent(
        chat_client=client,
        name="MyAgent",
        instructions="あなたは親切なアシスタントです"
    )

    return agent
```

### 方法2: APIキー認証（開発・テスト用）

**ステップ1: 環境変数設定**
```bash
export AZURE_OPENAI_API_KEY="your_api_key"
export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"
```

**ステップ2: Pythonコードで使用**
```python
import os
from agent_framework.azure import AzureOpenAIChatClient

client = AzureOpenAIChatClient(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    deployment_name="gpt-5"
)
```

## 環境変数設定

### .env ファイル例

```bash
# Azure AI Foundry / OpenAI 設定
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-08-01-preview
AZURE_REGION=eastus2  # または swedencentral

# GPT-5 デプロイメント名
AZURE_OPENAI_DEPLOYMENT_GPT5=gpt-5
AZURE_OPENAI_DEPLOYMENT_GPT5_MINI=gpt-5-mini

# 認証方式の選択
# 方式1: Azure CLI認証（推奨 - AZURE_OPENAI_API_KEYを設定しない）
# 方式2: APIキー認証（以下を設定）
# AZURE_OPENAI_API_KEY=your_api_key_here

# Agent 設定
MAX_RETRIES=3
TIMEOUT_SECONDS=60
ENABLE_STREAMING=true
ENABLE_CHECKPOINTS=true

# 観測可能性設定
ENABLE_TELEMETRY=true
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318

# GPT-5 特有の設定
GPT5_MAX_TOKENS=4096
GPT5_TEMPERATURE=0.7
```

## 期待される成果

### 技術的成果
- **最新GPT-5モデル**を活用したエージェントシステムの構築スキル
- **Azure AI Foundry**プラットフォームの実践的な理解
- Microsoft Agent Frameworkの実践的な使用方法の習得
- グラフベースワークフローの設計・実装能力
- マルチエージェントシステムのアーキテクチャ理解
- GPT-5の高度な推論能力を活用したアプリケーション開発

### ビジネス的成果
- エンタープライズグレードのAIシステム構築手法の理解
- Azure統合によるセキュアなAI活用方法の習得
- 観測可能性とデバッグ技術の向上
- スケーラブルなAIアプリケーション設計能力
- 最新のAI技術トレンドへのキャッチアップ

## 学習リソース

### Agent Framework公式ドキュメント
- [Microsoft Agent Framework GitHub](https://github.com/microsoft/agent-framework)
- [Agent Framework Overview](https://learn.microsoft.com/agent-framework/overview/agent-framework-overview)
- [Quick Start Guide](https://learn.microsoft.com/agent-framework/tutorials/quick-start)
- [Create and Run an Agent](https://learn.microsoft.com/agent-framework/tutorials/agents/run-agent)
- [Agent Framework Blog](https://devblogs.microsoft.com/foundry/introducing-microsoft-agent-framework-the-open-source-engine-for-agentic-ai-apps/)

### Azure & GPT-5リソース
- [Azure AI Foundry Documentation](https://learn.microsoft.com/azure/ai-foundry/)
- [GPT-5 in Azure AI Foundry](https://azure.microsoft.com/en-us/blog/gpt-5-in-azure-ai-foundry-the-future-of-ai-apps-and-agents-starts-here/)
- [Azure OpenAI Service Documentation](https://learn.microsoft.com/azure/ai-services/openai/)
- [OpenAI GPT-5 Introduction](https://openai.com/index/introducing-gpt-5/)

### 認証・その他
- [Azure Identity Documentation](https://learn.microsoft.com/python/api/azure-identity/)
- [Python asyncio Documentation](https://docs.python.org/3/library/asyncio.html)
- [OpenTelemetry Python](https://opentelemetry.io/docs/languages/python/)

---

**作成日**: 2025-11-05
**最終更新**: 2025-11-05
**バージョン**: 4.0
**ステータス**: Optimized - agent-framework実装パターン最適化版
