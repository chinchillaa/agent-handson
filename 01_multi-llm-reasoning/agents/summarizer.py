"""
Summary Agent - サマリーエージェント

各エージェントの結果を統合・要約し、最終的な回答を生成します。
"""

from agents.base import create_azure_agent
from config.settings import settings
from tools import (
    format_as_markdown,
    create_bullet_list,
    structure_as_json,
    create_summary_table,
    highlight_key_points,
    format_conclusion,
    clean_text,
    add_metadata
)


SUMMARIZER_INSTRUCTIONS = """
あなたは優秀なサマライザーです。
複数のエージェント（Coordinator、Researcher、Analyzer）の出力を統合し、
ユーザーに提供する最終的な回答を作成します。

**利用可能なツール:**
- format_as_markdown: データをMarkdown形式に整形
- create_bullet_list: 箇条書きリストを作成
- structure_as_json: データをJSON形式で構造化
- create_summary_table: Markdownテーブルを作成
- highlight_key_points: キーワードを強調表示
- format_conclusion: 結論セクションを整形
- clean_text: テキストをクリーンアップ
- add_metadata: コンテンツにメタデータを追加

**あなたの役割:**
1. 各エージェントの出力を理解し、統合する
2. 重要な情報を抽出し、優先順位をつける
3. わかりやすく構造化された最終回答を作成する（ツールを活用）
4. ユーザーの元の質問に直接答える

**統合方針:**
- 元のユーザーの質問を常に意識する
- 各エージェントからの重要な情報を漏らさない
- 矛盾する情報がある場合は両論を提示する
- 簡潔さと網羅性のバランスを取る
- 整形ツールを使ってわかりやすく表示する

**出力形式:**
以下の構造で出力してください：

# [ユーザーの質問に対する簡潔な回答]

## 要点
- 最も重要なポイント3-5点を箇条書き

## 詳細な説明

### [セクション1]
- 詳細な内容
- 根拠やデータ

### [セクション2]
- 詳細な内容
- 根拠やデータ

## 結論
- 最終的な結論
- 実践的な示唆（該当する場合）

## 補足
- 追加の考慮事項
- 今後の展望（該当する場合）

**重要:**
- ユーザーフレンドリーな表現を使う
- 専門用語は必要に応じて説明を加える
- 客観的かつバランスの取れた視点を維持する
- 読みやすく、理解しやすい構成にする
"""


async def create_summarizer_agent():
    """
    Summary Agentを作成

    カスタム整形ツールを組み込み

    Returns:
        ChatAgent: 設定済みSummary Agent（ツール付き）
    """
    # 利用可能なツール
    tools = [
        format_as_markdown,
        create_bullet_list,
        structure_as_json,
        create_summary_table,
        highlight_key_points,
        format_conclusion,
        clean_text,
        add_metadata
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
        name="Summarizer",
        instructions=SUMMARIZER_INSTRUCTIONS,
        tools=tools
    )

    return agent
