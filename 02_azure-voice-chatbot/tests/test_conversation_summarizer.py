"""
会話要約モジュール (tools/conversation_summarizer.py) のユニットテスト

会話履歴の要約、統計情報の取得機能をテストします。
"""

import sys
from pathlib import Path
import pytest

# プロジェクトディレクトリをパスに追加
PROJECT_DIR = Path(__file__).resolve().parents[1]
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from tools.conversation_summarizer import ConversationSummarizer, summarize_quick


def test_summarizer_initialization():
    """会話要約ツールの初期化テスト"""
    summarizer = ConversationSummarizer()

    # デフォルト値の確認
    assert summarizer.max_summary_length == 500

    # カスタム初期化
    custom_summarizer = ConversationSummarizer(max_summary_length=1000)
    assert custom_summarizer.max_summary_length == 1000


def test_summarize_empty_conversation():
    """空の会話履歴の要約テスト"""
    summarizer = ConversationSummarizer()

    summary = summarizer.summarize_conversation([])

    assert "まだ会話履歴がありません" in summary


def test_summarize_conversation_basic():
    """基本的な会話要約テスト"""
    summarizer = ConversationSummarizer()

    conversation_history = [
        {"role": "user", "content": "こんにちは"},
        {"role": "assistant", "content": "こんにちは。お元気ですか？"},
        {"role": "user", "content": "元気です。ありがとう。"},
    ]

    summary = summarizer.summarize_conversation(conversation_history)

    # 統計情報が含まれているか確認
    assert "会話ターン数: 2" in summary
    assert "ユーザー発話:" in summary
    assert "アシスタント応答:" in summary


def test_summarize_conversation_with_topics():
    """話題を含む会話の要約テスト"""
    summarizer = ConversationSummarizer()

    conversation_history = [
        {"role": "user", "content": "今日の天気はどうですか？"},
        {"role": "assistant", "content": "今日は晴れです。"},
        {"role": "user", "content": "Pythonプログラミングについて教えてください。"},
        {"role": "assistant", "content": "Pythonは使いやすいプログラミング言語です。"},
    ]

    summary = summarizer.summarize_conversation(conversation_history)

    # 話題が抽出されているか確認
    assert "主な話題:" in summary
    assert ("天気" in summary or "プログラミング" in summary)


def test_summarize_conversation_recent_focus():
    """最近の会話に焦点を当てた要約テスト"""
    summarizer = ConversationSummarizer()

    conversation_history = [
        {"role": "user", "content": "最初の質問です。"},
        {"role": "assistant", "content": "最初の回答です。"},
        {"role": "user", "content": "次の質問です。"},
        {"role": "assistant", "content": "次の回答です。"},
        {"role": "user", "content": "最後の質問です。"},
        {"role": "assistant", "content": "最後の回答です。"},
    ]

    # 最近の会話に焦点
    summary = summarizer.summarize_conversation(conversation_history, focus_on_recent=True)
    assert "最近の話題:" in summary

    # 最近の会話に焦点を当てない
    summary_no_focus = summarizer.summarize_conversation(conversation_history, focus_on_recent=False)
    assert "最近の話題:" not in summary_no_focus


def test_summarize_conversation_max_length():
    """要約の最大長制限テスト"""
    summarizer = ConversationSummarizer(max_summary_length=50)

    # 長い会話履歴
    conversation_history = []
    for i in range(20):
        conversation_history.append({
            "role": "user",
            "content": f"これは{i}番目の非常に長いユーザーメッセージです。" * 10
        })
        conversation_history.append({
            "role": "assistant",
            "content": f"これは{i}番目の非常に長いアシスタントメッセージです。" * 10
        })

    summary = summarizer.summarize_conversation(conversation_history)

    # 最大長以下に収まっているか確認
    assert len(summary) <= 50 + 3  # "..."を考慮


def test_get_conversation_stats():
    """会話統計情報の取得テスト"""
    summarizer = ConversationSummarizer()

    conversation_history = [
        {"role": "user", "content": "短いメッセージ"},
        {"role": "assistant", "content": "これは少し長めのアシスタントの応答です。"},
        {"role": "user", "content": "次の質問"},
        {"role": "assistant", "content": "次の回答"},
    ]

    stats = summarizer.get_conversation_stats(conversation_history)

    # 統計情報の確認
    assert stats["total_turns"] == 2
    assert stats["total_messages"] == 4
    assert stats["user_messages"] == 2
    assert stats["assistant_messages"] == 2
    assert stats["avg_user_length"] > 0
    assert stats["avg_assistant_length"] > 0


def test_get_conversation_stats_empty():
    """空の会話履歴の統計情報テスト"""
    summarizer = ConversationSummarizer()

    stats = summarizer.get_conversation_stats([])

    assert stats["total_turns"] == 0
    assert stats["total_messages"] == 0
    assert stats["user_messages"] == 0
    assert stats["assistant_messages"] == 0
    assert stats["avg_user_length"] == 0
    assert stats["avg_assistant_length"] == 0


def test_format_stats():
    """統計情報のフォーマットテスト"""
    summarizer = ConversationSummarizer()

    stats = {
        "total_turns": 5,
        "total_messages": 10,
        "user_messages": 5,
        "assistant_messages": 5,
        "avg_user_length": 25.5,
        "avg_assistant_length": 50.3,
    }

    formatted = summarizer.format_stats(stats)

    # フォーマットされた情報が含まれているか確認
    assert "会話統計:" in formatted
    assert "総ターン数: 5" in formatted
    assert "総メッセージ数: 10" in formatted
    assert "ユーザー発話数: 5" in formatted
    assert "アシスタント応答数: 5" in formatted
    assert "平均ユーザー発話長: 25.5" in formatted
    assert "平均アシスタント応答長: 50.3" in formatted


def test_extract_topics():
    """トピック抽出のテスト"""
    summarizer = ConversationSummarizer()

    messages = [
        "今日の天気はどうですか？",
        "Pythonプログラミングについて教えてください。",
        "機械学習のモデルを作りたい。",
    ]

    topics = summarizer._extract_topics(messages)

    # 抽出されたトピックの確認
    assert "天気" in topics
    assert "プログラミング" in topics
    assert "AI" in topics


def test_extract_topics_empty():
    """空のメッセージリストからのトピック抽出テスト"""
    summarizer = ConversationSummarizer()

    topics = summarizer._extract_topics([])

    assert topics == []


def test_extract_recent_topics():
    """最近のトピック抽出テスト"""
    summarizer = ConversationSummarizer()

    conversation_history = [
        {"role": "user", "content": "最初の質問です。"},
        {"role": "assistant", "content": "最初の回答です。"},
        {"role": "user", "content": "Pythonについて教えてください。"},
        {"role": "assistant", "content": "Pythonについて説明します。"},
    ]

    recent_topic = summarizer._extract_recent_topics(conversation_history, count=1)

    # 最後のユーザー発話が含まれているか確認
    assert "Python" in recent_topic or "について" in recent_topic


def test_extract_recent_topics_long_message():
    """長いメッセージの最近のトピック抽出テスト"""
    summarizer = ConversationSummarizer()

    long_message = "これは非常に長いユーザーメッセージです。" * 20
    conversation_history = [
        {"role": "user", "content": long_message},
        {"role": "assistant", "content": "回答です。"},
    ]

    recent_topic = summarizer._extract_recent_topics(conversation_history, count=1)

    # 50文字に切り詰められ、"..."が付いているか確認
    assert len(recent_topic) <= 53  # 50 + "..."
    assert "..." in recent_topic


def test_summarize_quick_function():
    """summarize_quick関数のテスト"""
    conversation_history = [
        {"role": "user", "content": "こんにちは"},
        {"role": "assistant", "content": "こんにちは。お元気ですか？"},
    ]

    summary = summarize_quick(conversation_history)

    # summarize_conversationと同じ結果が得られるか確認
    assert "会話ターン数:" in summary
    assert isinstance(summary, str)


def test_summarize_conversation_user_only():
    """ユーザーのみの会話履歴の要約テスト"""
    summarizer = ConversationSummarizer()

    conversation_history = [
        {"role": "user", "content": "最初のメッセージ"},
        {"role": "user", "content": "次のメッセージ"},
        {"role": "user", "content": "最後のメッセージ"},
    ]

    summary = summarizer.summarize_conversation(conversation_history)

    # ユーザー発話のみの統計
    assert "会話ターン数: 3" in summary
    assert "アシスタント応答: 0文字" in summary


def test_summarize_conversation_assistant_only():
    """アシスタントのみの会話履歴の要約テスト"""
    summarizer = ConversationSummarizer()

    conversation_history = [
        {"role": "assistant", "content": "最初の応答"},
        {"role": "assistant", "content": "次の応答"},
    ]

    summary = summarizer.summarize_conversation(conversation_history)

    # アシスタント応答のみの統計
    assert "会話ターン数: 0" in summary
    assert "ユーザー発話: 0文字" in summary
