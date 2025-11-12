"""
コンテキスト管理ツール

会話の中で重要な情報を抽出・保持し、適切なタイミングで参照できるようにします。
"""

from typing import Optional
from datetime import datetime


class ContextManager:
    """
    コンテキスト管理クラス

    会話の文脈や重要な情報を管理します。
    """

    def __init__(self, max_context_items: int = 20):
        """
        コンテキストマネージャーの初期化

        Args:
            max_context_items: 保持する最大コンテキスト項目数
        """
        self.max_context_items = max_context_items
        self.context_items: list[dict] = []
        self.user_preferences: dict = {}

    def add_context(
        self,
        key: str,
        value: str,
        importance: str = "normal"
    ) -> None:
        """
        コンテキスト情報を追加

        Args:
            key: コンテキストのキー（例: "user_name", "topic", "preference"）
            value: コンテキストの値
            importance: 重要度（"high", "normal", "low"）
        """
        context_item = {
            "key": key,
            "value": value,
            "importance": importance,
            "timestamp": datetime.now().isoformat()
        }

        # 同じキーの既存項目を削除
        self.context_items = [
            item for item in self.context_items
            if item["key"] != key
        ]

        # 新しい項目を追加
        self.context_items.append(context_item)

        # 最大数を超えた場合、重要度の低いものから削除
        if len(self.context_items) > self.max_context_items:
            self._trim_context()

    def get_context(self, key: str) -> Optional[str]:
        """
        指定されたキーのコンテキストを取得

        Args:
            key: コンテキストのキー

        Returns:
            コンテキストの値（存在しない場合はNone）
        """
        for item in reversed(self.context_items):
            if item["key"] == key:
                return item["value"]
        return None

    def get_all_contexts(self) -> list[dict]:
        """
        すべてのコンテキスト情報を取得

        Returns:
            コンテキスト項目のリスト
        """
        return self.context_items.copy()

    def get_important_contexts(self) -> list[dict]:
        """
        重要度が高いコンテキストのみを取得

        Returns:
            重要なコンテキスト項目のリスト
        """
        return [
            item for item in self.context_items
            if item["importance"] == "high"
        ]

    def set_user_preference(self, key: str, value: str) -> None:
        """
        ユーザーの好みや設定を保存

        Args:
            key: 設定項目名（例: "preferred_voice", "speaking_speed"）
            value: 設定値
        """
        self.user_preferences[key] = value

    def get_user_preference(self, key: str) -> Optional[str]:
        """
        ユーザーの好みや設定を取得

        Args:
            key: 設定項目名

        Returns:
            設定値（存在しない場合はNone）
        """
        return self.user_preferences.get(key)

    def extract_from_conversation(
        self,
        conversation_history: list[dict]
    ) -> None:
        """
        会話履歴から自動的にコンテキストを抽出

        Args:
            conversation_history: 会話履歴
        """
        # ユーザーの最近の発話から話題を抽出
        recent_user_messages = [
            msg["content"] for msg in conversation_history[-10:]
            if msg["role"] == "user"
        ]

        if recent_user_messages:
            # 最後の話題を保存
            last_topic = self._extract_topic(recent_user_messages[-1])
            if last_topic:
                self.add_context("last_topic", last_topic, importance="normal")

        # 名前の検出
        for msg in conversation_history:
            if msg["role"] == "user":
                name = self._extract_name(msg["content"])
                if name:
                    self.add_context("user_name", name, importance="high")

    def _extract_topic(self, message: str) -> Optional[str]:
        """
        メッセージから話題を抽出

        Args:
            message: メッセージテキスト

        Returns:
            抽出された話題（存在しない場合はNone）
        """
        # 簡易的な話題抽出（キーワードベース）
        topic_patterns = {
            "天気": ["天気", "気温", "雨", "晴れ"],
            "プログラミング": ["Python", "コード", "プログラム", "関数", "変数"],
            "AI": ["AI", "機械学習", "LLM", "GPT", "エージェント"],
            "音楽": ["音楽", "曲", "歌", "アーティスト"],
            "料理": ["料理", "レシピ", "食事", "食べ物"],
        }

        for topic, keywords in topic_patterns.items():
            if any(keyword in message for keyword in keywords):
                return topic

        return None

    def _extract_name(self, message: str) -> Optional[str]:
        """
        メッセージから名前を抽出

        Args:
            message: メッセージテキスト

        Returns:
            抽出された名前（存在しない場合はNone）
        """
        # 簡易的な名前抽出（「私の名前は〜」パターン）
        patterns = [
            "私の名前は",
            "名前は",
            "〜と言います",
            "〜です"
        ]

        for pattern in patterns:
            if pattern in message:
                # パターンの後の単語を抽出（簡易版）
                idx = message.find(pattern) + len(pattern)
                remaining = message[idx:].strip()
                # 最初の単語を取得（簡易的）
                words = remaining.split()
                if words:
                    # 句読点を除去
                    name = words[0].rstrip("。、です")
                    if len(name) > 0 and len(name) <= 10:  # 妥当な長さの名前
                        return name

        return None

    def _trim_context(self) -> None:
        """
        コンテキスト項目数が上限を超えた場合、古い・重要度の低いものを削除
        """
        # 重要度でソート（high > normal > low）、同じ重要度なら古い順
        importance_order = {"high": 3, "normal": 2, "low": 1}

        sorted_items = sorted(
            self.context_items,
            key=lambda x: (importance_order.get(x["importance"], 0), x["timestamp"]),
            reverse=True
        )

        # 上限まで保持
        self.context_items = sorted_items[:self.max_context_items]

    def format_context_summary(self) -> str:
        """
        コンテキスト情報を読みやすく整形

        Returns:
            整形されたコンテキスト情報
        """
        if not self.context_items:
            return "保存されているコンテキスト情報はありません。"

        lines = ["保存されているコンテキスト:"]

        # 重要度別にグループ化
        high_items = [item for item in self.context_items if item["importance"] == "high"]
        normal_items = [item for item in self.context_items if item["importance"] == "normal"]
        low_items = [item for item in self.context_items if item["importance"] == "low"]

        if high_items:
            lines.append("\n【重要】")
            for item in high_items:
                lines.append(f"  {item['key']}: {item['value']}")

        if normal_items:
            lines.append("\n【通常】")
            for item in normal_items:
                lines.append(f"  {item['key']}: {item['value']}")

        if low_items:
            lines.append("\n【補足】")
            for item in low_items:
                lines.append(f"  {item['key']}: {item['value']}")

        # ユーザー設定
        if self.user_preferences:
            lines.append("\n【ユーザー設定】")
            for key, value in self.user_preferences.items():
                lines.append(f"  {key}: {value}")

        return "\n".join(lines)

    def clear_context(self) -> None:
        """すべてのコンテキスト情報をクリア"""
        self.context_items = []
        self.user_preferences = {}


if __name__ == "__main__":
    """テスト実行"""
    print("=== コンテキスト管理テスト ===\n")

    manager = ContextManager()

    # コンテキスト追加テスト
    print("【コンテキスト追加】")
    manager.add_context("user_name", "太郎", importance="high")
    manager.add_context("last_topic", "プログラミング", importance="normal")
    manager.add_context("mood", "元気", importance="low")

    # ユーザー設定テスト
    manager.set_user_preference("preferred_voice", "ja-JP-NanamiNeural")
    manager.set_user_preference("speaking_speed", "normal")

    print(manager.format_context_summary())

    # 会話履歴からの抽出テスト
    print("\n【会話履歴からの抽出】")
    test_history = [
        {"role": "user", "content": "私の名前は花子です。"},
        {"role": "assistant", "content": "花子さん、こんにちは。"},
        {"role": "user", "content": "Pythonプログラミングについて教えてください。"},
    ]

    manager.extract_from_conversation(test_history)
    print(manager.format_context_summary())
