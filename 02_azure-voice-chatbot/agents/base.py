"""
共通エージェント基底クラス

Azure OpenAI エージェントを作成するための共通機能を提供します。
"""

import os
from typing import Optional
from agent_framework import ChatAgent
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity.aio import AzureCliCredential


async def create_azure_agent(
    name: str,
    instructions: str,
    deployment_name: str,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None
) -> ChatAgent:
    """
    Azure OpenAI エージェントを作成

    Args:
        name: エージェント名
        instructions: システムプロンプト（エージェントの役割・指示）
        deployment_name: Azure OpenAIのデプロイメント名（gpt-5など）
        endpoint: Azure OpenAIエンドポイント（環境変数から取得可能）
        api_key: APIキー（省略時はAzure CLI認証を使用）

    Returns:
        ChatAgent: 設定済みエージェント
    """
    # 環境変数から取得
    endpoint = endpoint or os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = api_key or os.getenv("AZURE_OPENAI_API_KEY")

    if not endpoint:
        raise ValueError("AZURE_OPENAI_ENDPOINTが設定されていません")

    # クライアント作成
    if api_key:
        # APIキー認証
        client = AzureOpenAIChatClient(
            endpoint=endpoint,
            deployment_name=deployment_name,
            api_key=api_key
        )
    else:
        # Azure CLI認証（推奨）
        credential = AzureCliCredential()
        client = AzureOpenAIChatClient(
            endpoint=endpoint,
            deployment_name=deployment_name,
            credential=credential
        )

    # エージェント作成
    agent = ChatAgent(
        chat_client=client,
        name=name,
        instructions=instructions
    )

    return agent
