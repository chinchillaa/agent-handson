"""
Analysis Agent - 分析エージェント

データ分析・論理的推論を担当します。
"""

from agent_framework._tools import HostedCodeInterpreterTool
from .base import create_azure_agent
from ..config.settings import settings
from ..tools import (
    calculate_statistics,
    compare_data,
    extract_numbers_from_text,
    analyze_trend,
    categorize_data
)


ANALYZER_INSTRUCTIONS = """
あなたは優秀なアナリストです。
Researcherが収集した情報を分析し、深い洞察を導き出します。

**利用可能なツール:**
- コードインタープリター（複雑な計算・データ分析・グラフ作成）
- calculate_statistics: 基本統計量の計算
- compare_data: 2つのデータセットを比較
- extract_numbers_from_text: テキストから数値を抽出
- analyze_trend: データのトレンド分析
- categorize_data: 閾値に基づくデータ分類

**あなたの役割:**
1. 収集された情報を多角的に分析する（ツールを活用）
2. パターン、傾向、因果関係を特定する（analyze_trendを活用）
3. 論理的な推論を行い、意味のある洞察を抽出する
4. 異なる観点からの考察を提供する

**分析方針:**
- 批判的思考を用いて情報を評価する
- 複数の視点から分析する（compare_dataで比較）
- 仮説を立て、データで検証する（コードインタープリター活用）
- 潜在的な課題やリスクも指摘する

**出力形式:**
以下の構造で出力してください：

【分析の観点】
- 本分析で採用する主要な観点

【主要な発見】
## 発見1: [タイトル]
- 詳細な説明
- 根拠となるデータ
- 重要性の評価

## 発見2: [タイトル]
...

【パターンと傾向】
- 特定されたパターン
- 将来の傾向予測

【リスクと機会】
- 潜在的なリスク
- 可能性のある機会

【推論と洞察】
- データから導き出される深い洞察
- 論理的な推論プロセスの説明

**重要:**
- 論理的な根拠を明確に示す
- 推測と確実な分析を区別する
- Summarizerが最終回答を作成しやすいように構造化する
"""


async def create_analyzer_agent():
    """
    Analysis Agentを作成

    HostedCodeInterpreterToolとカスタムツールを組み込み

    Returns:
        ChatAgent: 設定済みAnalysis Agent（ツール付き）
    """
    # 利用可能なツール
    tools = [
        HostedCodeInterpreterTool(description="複雑な計算、データ分析、グラフ作成"),
        calculate_statistics,
        compare_data,
        extract_numbers_from_text,
        analyze_trend,
        categorize_data
    ]

    from agent_framework import ChatAgent
    from agent_framework.azure import AzureOpenAIChatClient
    from azure.identity.aio import AzureCliCredential
    import os

    # 環境変数から取得
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")

    if not endpoint:
        raise ValueError("AZURE_OPENAI_ENDPOINTが設定されていません")

    deployment_name = settings.get_deployment_name("gpt5")

    # クライアント作成
    if api_key:
        client = AzureOpenAIChatClient(
            endpoint=endpoint,
            deployment_name=deployment_name,
            api_key=api_key
        )
    else:
        credential = AzureCliCredential()
        client = AzureOpenAIChatClient(
            endpoint=endpoint,
            deployment_name=deployment_name,
            credential=credential
        )

    # ツール付きエージェント作成
    agent = ChatAgent(
        chat_client=client,
        name="Analyzer",
        instructions=ANALYZER_INSTRUCTIONS,
        tools=tools
    )

    return agent
