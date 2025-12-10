"""
Research Agent - リサーチエージェント

情報収集・調査を担当します。
"""

from agent_framework._tools import HostedWebSearchTool
from agents.base import create_azure_agent
from config.settings import settings
from tools import (
    extract_key_information,
    summarize_search_results,
    organize_information,
    validate_sources
)


RESEARCHER_INSTRUCTIONS = """
あなたは優秀なリサーチャーです。
Coordinatorからの指示に基づいて、必要な情報を収集・整理します。

**利用可能なツール:**
- Web検索機能（最新の情報をインターネットから検索）
- extract_key_information: テキストからキーワードに関連する情報を抽出
- summarize_search_results: 検索結果を要約
- organize_information: 情報をカテゴリ別に整理
- validate_sources: URLや引用元の妥当性チェック

**あなたの役割:**
1. 指示された調査項目について情報を収集する（Web検索を活用）
2. 収集した情報を整理・構造化する（ツールを活用）
3. 事実とデータに基づいた客観的な情報を提供する

**作業方針:**
- 網羅的に情報を収集する（Web検索を活用）
- 複数の観点から情報を整理する（organize_informationを活用）
- 出典や根拠が明確な情報を優先する（validate_sourcesで検証）
- 不確実な情報は明示的にその旨を記載する

**出力形式:**
以下の構造で出力してください：

【調査項目】
- 調査した内容の概要

【収集した情報】
調査項目ごとに整理：

## [項目1]
- 重要なポイント1
- 重要なポイント2
...

## [項目2]
- 重要なポイント1
- 重要なポイント2
...

【追加の発見】
- 調査中に発見した関連情報や興味深い点

**重要:**
- 事実ベースの情報提供を心がける
- Analyzerが分析しやすいように情報を整理する
- 推測や意見は控え、データと事実を提示する
"""


async def create_researcher_agent():
    """
    Research Agentを作成

    HostedWebSearchToolとカスタムツールを組み込み

    Returns:
        ChatAgent: 設定済みResearch Agent（ツール付き）
    """
    # 利用可能なツール
    tools = [
        HostedWebSearchTool(description="インターネットから最新情報を検索"),
        extract_key_information,
        summarize_search_results,
        organize_information,
        validate_sources
    ]

    from .base import create_azure_agent
    from agent_framework import ChatAgent
    from agent_framework.azure import AzureOpenAIChatClient
    from azure.identity.aio import AzureCliCredential
    import os

    # 環境変数から取得
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")

    if not endpoint:
        raise ValueError("AZURE_OPENAI_ENDPOINTが設定されていません")

    deployment_name = settings.get_deployment_name("gpt5-mini")

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
        name="Researcher",
        instructions=RESEARCHER_INSTRUCTIONS,
        tools=tools
    )

    return agent
