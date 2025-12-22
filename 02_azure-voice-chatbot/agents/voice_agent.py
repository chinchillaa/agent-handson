"""
音声対話エージェント

GPT-5を使用した音声対話専用エージェントを提供します。
"""

from typing import Optional
from agent_framework import ChatAgent
from .base import create_azure_agent


# システムプロンプト（音声対話用）
VOICE_AGENT_INSTRUCTIONS = """あなたは親しみやすく自然な音声対話アシスタントです。

## 役割
- ユーザーとの音声による自然な対話を行う
- 質問に対して簡潔で分かりやすい回答を提供する
- 必要に応じて追加の質問をして、ユーザーのニーズを理解する

## 対話スタイル
- 音声での読み上げに適した、自然で流れるような文章で回答する
- 長すぎる回答は避け、要点を簡潔に伝える
- 専門用語を使う場合は、必要に応じて簡単な説明を加える
- 親しみやすく、丁寧な口調を維持する

## 注意事項
- マークダウン記法やコードブロックは使用しない（音声には不向き）
- 箇条書きは「1つ目は...、2つ目は...」のように音声で分かりやすく表現する
- URLやファイルパスは読み上げやすい形で簡潔に説明する
- 数式や図表が必要な場合は、言葉で分かりやすく説明する

## 対話の進め方
1. ユーザーの質問や要求を正確に理解する
2. 簡潔で分かりやすい回答を提供する
3. 必要に応じて確認や追加質問を行う
4. 会話の文脈を理解し、自然な対話を継続する
"""


async def create_voice_agent(
    name: str = "VoiceAssistant",
    instructions: Optional[str] = None,
    deployment_name: str = "gpt-5",
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None
) -> ChatAgent:
    """
    音声対話エージェントを作成

    Args:
        name: エージェント名（デフォルト: VoiceAssistant）
        instructions: カスタムシステムプロンプト（省略時はデフォルトを使用）
        deployment_name: Azure OpenAIのデプロイメント名（デフォルト: gpt-5）
        endpoint: Azure OpenAIエンドポイント（環境変数から取得可能）
        api_key: APIキー（省略時はAzure CLI認証を使用）

    Returns:
        ChatAgent: 音声対話用に設定されたエージェント
    """
    # カスタム指示がない場合はデフォルトを使用
    agent_instructions = instructions or VOICE_AGENT_INSTRUCTIONS

    # ベースエージェント作成関数を使用
    agent = await create_azure_agent(
        name=name,
        instructions=agent_instructions,
        deployment_name=deployment_name,
        endpoint=endpoint,
        api_key=api_key
    )

    return agent


class VoiceAgentSession:
    """
    音声対話セッション管理クラス

    会話履歴の管理と、エージェントとの対話インターフェースを提供します。
    """

    def __init__(self, agent: ChatAgent):
        """
        セッションの初期化

        Args:
            agent: 使用するChatAgentインスタンス
        """
        self.agent = agent
        self.conversation_history: list[dict] = []

    async def send_message(self, user_input: str) -> str:
        """
        ユーザーメッセージを送信してエージェントから応答を取得

        Args:
            user_input: ユーザーからの入力テキスト

        Returns:
            エージェントからの応答テキスト
        """
        # ユーザーメッセージを履歴に追加
        self.conversation_history.append({
            "role": "user",
            "content": user_input
        })

        # エージェントに送信（Agent Framework 1.0.0b251209ではrun()を使用）
        response = await self.agent.run(user_input)

        # アシスタントの応答を履歴に追加
        assistant_message = response.text
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })

        return assistant_message

    def get_conversation_history(self) -> list[dict]:
        """
        会話履歴を取得

        Returns:
            会話履歴のリスト（各要素は{"role": str, "content": str}）
        """
        return self.conversation_history.copy()

    def clear_history(self):
        """会話履歴をクリア"""
        self.conversation_history = []
        print("💭 会話履歴をクリアしました")

    def get_turn_count(self) -> int:
        """
        現在の会話ターン数を取得

        Returns:
            ユーザー発話の回数
        """
        return sum(1 for msg in self.conversation_history if msg["role"] == "user")


async def create_voice_session(
    agent_name: str = "VoiceAssistant",
    deployment_name: str = "gpt-5"
) -> VoiceAgentSession:
    """
    音声対話セッションを作成（簡易ヘルパー関数）

    Args:
        agent_name: エージェント名
        deployment_name: Azure OpenAIデプロイメント名

    Returns:
        VoiceAgentSession: 設定済みの音声対話セッション
    """
    agent = await create_voice_agent(
        name=agent_name,
        deployment_name=deployment_name
    )

    session = VoiceAgentSession(agent)
    return session


if __name__ == "__main__":
    """テスト実行"""
    import asyncio

    async def test_voice_agent():
        print("=== 音声対話エージェント テスト ===\n")

        # エージェント作成
        print("エージェントを作成中...")
        agent = await create_voice_agent(name="TestVoiceAgent")
        session = VoiceAgentSession(agent)

        print("✅ エージェント作成完了\n")

        # テストメッセージ
        test_messages = [
            "こんにちは。今日の天気について教えてください。",
            "ありがとう。ところで、Pythonプログラミングのコツを教えてください。",
            "なるほど、参考になりました。",
        ]

        for i, message in enumerate(test_messages, 1):
            print(f"【ターン {i}】")
            print(f"ユーザー: {message}")

            response = await session.send_message(message)
            print(f"アシスタント: {response}\n")

        # 会話履歴表示
        print("=== 会話履歴 ===")
        print(f"総ターン数: {session.get_turn_count()}")

    # 非同期テスト実行
    asyncio.run(test_voice_agent())
