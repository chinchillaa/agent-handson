"""
会話要約ツール

会話履歴を要約して重要なポイントを抽出します。
"""

from typing import Optional


class ConversationSummarizer:
    """
    会話要約クラス

    長い会話履歴を要約し、重要な情報を抽出します。
    """

    def __init__(self, max_summary_length: int = 500):
        """
        会話要約ツールの初期化

        Args:
            max_summary_length: 要約の最大文字数
        """
        self.max_summary_length = max_summary_length

    def summarize_conversation(
        self,
        conversation_history: list[dict],
        focus_on_recent: bool = True
    ) -> str:
        """
        会話履歴を要約

        Args:
            conversation_history: 会話履歴（{"role": str, "content": str}のリスト）
            focus_on_recent: 最近の会話を重視するかどうか

        Returns:
            要約されたテキスト
        """
        if not conversation_history:
            return "まだ会話履歴がありません。"

        # ユーザーとアシスタントの発話を分離
        user_messages = [
            msg["content"] for msg in conversation_history
            if msg["role"] == "user"
        ]
        assistant_messages = [
            msg["content"] for msg in conversation_history
            if msg["role"] == "assistant"
        ]

        # 統計情報
        total_turns = len(user_messages)
        total_user_chars = sum(len(msg) for msg in user_messages)
        total_assistant_chars = sum(len(msg) for msg in assistant_messages)

        # 要約テキスト作成
        summary_parts = [
            f"会話ターン数: {total_turns}",
            f"ユーザー発話: {total_user_chars}文字",
            f"アシスタント応答: {total_assistant_chars}文字",
        ]

        # 最近の会話を重視する場合
        if focus_on_recent and total_turns > 0:
            recent_count = min(3, total_turns)
            recent_topics = self._extract_recent_topics(
                conversation_history,
                recent_count
            )
            if recent_topics:
                summary_parts.append(f"\n最近の話題: {recent_topics}")

        # トピック抽出
        topics = self._extract_topics(user_messages)
        if topics:
            summary_parts.append(f"\n主な話題: {', '.join(topics[:5])}")

        summary = "\n".join(summary_parts)

        # 最大長を超える場合は切り詰め
        if len(summary) > self.max_summary_length:
            summary = summary[:self.max_summary_length] + "..."

        return summary

    def _extract_recent_topics(
        self,
        conversation_history: list[dict],
        count: int
    ) -> str:
        """
        最近の会話からトピックを抽出

        Args:
            conversation_history: 会話履歴
            count: 抽出する会話数

        Returns:
            トピックの要約
        """
        recent_messages = conversation_history[-count * 2:]  # ユーザーとアシスタント両方
        user_recent = [
            msg["content"] for msg in recent_messages
            if msg["role"] == "user"
        ]

        if not user_recent:
            return ""

        # 最新のユーザー発話を要約（簡易版：最初の50文字）
        latest = user_recent[-1]
        if len(latest) > 50:
            return latest[:50] + "..."
        return latest

    def _extract_topics(self, messages: list[str]) -> list[str]:
        """
        メッセージからトピック（キーワード）を抽出

        Args:
            messages: メッセージリスト

        Returns:
            抽出されたトピックのリスト
        """
        # 簡易的なトピック抽出（キーワードベース）
        keywords = []

        # よくある質問パターン
        question_keywords = {
            "天気": ["天気", "気温", "雨", "晴れ"],
            "時間": ["時間", "何時", "いつ"],
            "場所": ["どこ", "場所", "位置"],
            "方法": ["どうやって", "方法", "やり方"],
            "理由": ["なぜ", "理由", "どうして"],
            "プログラミング": ["Python", "コード", "プログラム", "関数"],
            "AI": ["AI", "機械学習", "LLM", "GPT"],
        }

        for message in messages:
            for topic, terms in question_keywords.items():
                if any(term in message for term in terms):
                    if topic not in keywords:
                        keywords.append(topic)

        return keywords

    def get_conversation_stats(
        self,
        conversation_history: list[dict]
    ) -> dict:
        """
        会話統計情報を取得

        Args:
            conversation_history: 会話履歴

        Returns:
            統計情報の辞書
        """
        user_messages = [
            msg for msg in conversation_history
            if msg["role"] == "user"
        ]
        assistant_messages = [
            msg for msg in conversation_history
            if msg["role"] == "assistant"
        ]

        return {
            "total_turns": len(user_messages),
            "total_messages": len(conversation_history),
            "user_messages": len(user_messages),
            "assistant_messages": len(assistant_messages),
            "avg_user_length": (
                sum(len(msg["content"]) for msg in user_messages) / len(user_messages)
                if user_messages else 0
            ),
            "avg_assistant_length": (
                sum(len(msg["content"]) for msg in assistant_messages) / len(assistant_messages)
                if assistant_messages else 0
            ),
        }

    def format_stats(self, stats: dict) -> str:
        """
        統計情報を読みやすい形式にフォーマット

        Args:
            stats: get_conversation_stats()の戻り値

        Returns:
            フォーマットされた統計情報
        """
        return f"""
会話統計:
  総ターン数: {stats['total_turns']}
  総メッセージ数: {stats['total_messages']}
  ユーザー発話数: {stats['user_messages']}
  アシスタント応答数: {stats['assistant_messages']}
  平均ユーザー発話長: {stats['avg_user_length']:.1f}文字
  平均アシスタント応答長: {stats['avg_assistant_length']:.1f}文字
        """.strip()


def summarize_quick(conversation_history: list[dict]) -> str:
    """
    会話履歴を簡易要約する関数

    Args:
        conversation_history: 会話履歴

    Returns:
        要約テキスト
    """
    summarizer = ConversationSummarizer()
    return summarizer.summarize_conversation(conversation_history)


if __name__ == "__main__":
    """テスト実行"""
    # サンプル会話履歴
    test_history = [
        {"role": "user", "content": "こんにちは。今日の天気について教えてください。"},
        {"role": "assistant", "content": "こんにちは。今日の天気についてお答えします。現在、晴れており気温は20度です。"},
        {"role": "user", "content": "ありがとう。Pythonプログラミングのコツを教えてください。"},
        {"role": "assistant", "content": "Pythonプログラミングのコツをいくつか紹介します。1つ目は、コードの可読性を重視すること。2つ目は、適切な命名規則を使うこと。3つ目は、ドキュメントを書くことです。"},
        {"role": "user", "content": "なるほど、参考になりました。"},
        {"role": "assistant", "content": "お役に立てて嬉しいです。他に質問があればお気軽にどうぞ。"},
    ]

    summarizer = ConversationSummarizer()

    print("=== 会話要約テスト ===\n")
    print("【要約】")
    summary = summarizer.summarize_conversation(test_history)
    print(summary)

    print("\n【統計情報】")
    stats = summarizer.get_conversation_stats(test_history)
    print(summarizer.format_stats(stats))
