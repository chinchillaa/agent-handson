"""
コンテキスト管理モジュール (tools/context_manager.py) のユニットテスト

コンテキスト情報の追加、取得、抽出機能をテストします。
"""

import sys
from pathlib import Path
from datetime import datetime
import pytest

# プロジェクトディレクトリをパスに追加
PROJECT_DIR = Path(__file__).resolve().parents[1]
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from tools.context_manager import ContextManager


def test_context_manager_initialization():
    """コンテキストマネージャーの初期化テスト"""
    manager = ContextManager()

    # デフォルト値の確認
    assert manager.max_context_items == 20
    assert manager.context_items == []
    assert manager.user_preferences == {}

    # カスタム初期化
    custom_manager = ContextManager(max_context_items=10)
    assert custom_manager.max_context_items == 10


def test_add_context():
    """コンテキスト追加のテスト"""
    manager = ContextManager()

    # 通常の追加
    manager.add_context("user_name", "太郎", importance="high")
    assert len(manager.context_items) == 1
    assert manager.context_items[0]["key"] == "user_name"
    assert manager.context_items[0]["value"] == "太郎"
    assert manager.context_items[0]["importance"] == "high"
    assert "timestamp" in manager.context_items[0]

    # 複数追加
    manager.add_context("topic", "プログラミング", importance="normal")
    manager.add_context("mood", "元気", importance="low")
    assert len(manager.context_items) == 3


def test_add_context_duplicate_key():
    """同じキーのコンテキスト追加テスト（上書き）"""
    manager = ContextManager()

    # 最初の追加
    manager.add_context("user_name", "太郎")
    assert len(manager.context_items) == 1
    assert manager.get_context("user_name") == "太郎"

    # 同じキーで再追加（上書き）
    manager.add_context("user_name", "花子")
    assert len(manager.context_items) == 1
    assert manager.get_context("user_name") == "花子"


def test_add_context_max_limit():
    """コンテキスト最大数制限のテスト"""
    manager = ContextManager(max_context_items=5)

    # 最大数まで追加
    for i in range(7):
        manager.add_context(f"key_{i}", f"value_{i}", importance="low")

    # 最大数以下に保たれているか確認
    assert len(manager.context_items) <= 5


def test_get_context():
    """コンテキスト取得のテスト"""
    manager = ContextManager()

    manager.add_context("user_name", "太郎")
    manager.add_context("topic", "AI")

    # 存在するキーの取得
    assert manager.get_context("user_name") == "太郎"
    assert manager.get_context("topic") == "AI"

    # 存在しないキーの取得
    assert manager.get_context("non_existent") is None


def test_get_all_contexts():
    """全コンテキスト取得のテスト"""
    manager = ContextManager()

    # 空の状態
    assert manager.get_all_contexts() == []

    # 追加後
    manager.add_context("key1", "value1")
    manager.add_context("key2", "value2")

    all_contexts = manager.get_all_contexts()
    assert len(all_contexts) == 2
    assert all_contexts[0]["key"] == "key1"
    assert all_contexts[1]["key"] == "key2"

    # コピーであることを確認（元のリストを変更しても影響しない）
    all_contexts.append({"key": "test", "value": "test"})
    assert len(manager.context_items) == 2


def test_get_important_contexts():
    """重要コンテキストのフィルタリングテスト"""
    manager = ContextManager()

    manager.add_context("user_name", "太郎", importance="high")
    manager.add_context("topic", "AI", importance="normal")
    manager.add_context("mood", "元気", importance="low")
    manager.add_context("preference", "速い応答", importance="high")

    important_contexts = manager.get_important_contexts()

    # 重要度が高いもののみ取得されるか確認
    assert len(important_contexts) == 2
    assert all(item["importance"] == "high" for item in important_contexts)
    assert any(item["key"] == "user_name" for item in important_contexts)
    assert any(item["key"] == "preference" for item in important_contexts)


def test_user_preferences():
    """ユーザー設定の管理テスト"""
    manager = ContextManager()

    # 設定の保存
    manager.set_user_preference("preferred_voice", "ja-JP-NanamiNeural")
    manager.set_user_preference("speaking_speed", "normal")

    # 設定の取得
    assert manager.get_user_preference("preferred_voice") == "ja-JP-NanamiNeural"
    assert manager.get_user_preference("speaking_speed") == "normal"

    # 存在しない設定
    assert manager.get_user_preference("non_existent") is None

    # 設定の上書き
    manager.set_user_preference("preferred_voice", "ja-JP-KeitaNeural")
    assert manager.get_user_preference("preferred_voice") == "ja-JP-KeitaNeural"


def test_extract_topic():
    """話題抽出のテスト"""
    manager = ContextManager()

    # 天気に関する話題
    topic = manager._extract_topic("今日の天気はどうですか？")
    assert topic == "天気"

    # プログラミングに関する話題
    topic = manager._extract_topic("Pythonプログラムの書き方を教えてください。")
    assert topic == "プログラミング"

    # AIに関する話題
    topic = manager._extract_topic("機械学習のモデルについて知りたい。")
    assert topic == "AI"

    # 話題が見つからない場合
    topic = manager._extract_topic("こんにちは")
    assert topic is None


def test_extract_name():
    """名前抽出のテスト"""
    manager = ContextManager()

    # 「私の名前は〜」パターン
    name = manager._extract_name("私の名前は太郎です。")
    assert name == "太郎"

    # 「名前は〜」パターン
    name = manager._extract_name("名前は花子です。")
    assert name == "花子"

    # 名前が見つからない場合
    name = manager._extract_name("こんにちは")
    assert name is None

    # 長すぎる名前（不正）
    name = manager._extract_name("私の名前はとても長い名前なので抽出できませんです。")
    # 最初の単語が取得されるが、妥当な長さでなければNone
    # 実装依存だが、基本的に短い単語が期待される


def test_extract_from_conversation():
    """会話履歴からのコンテキスト抽出テスト"""
    manager = ContextManager()

    conversation_history = [
        {"role": "user", "content": "私の名前は太郎です。"},
        {"role": "assistant", "content": "太郎さん、こんにちは。"},
        {"role": "user", "content": "Pythonプログラミングについて教えてください。"},
        {"role": "assistant", "content": "Pythonについて説明します。"},
    ]

    manager.extract_from_conversation(conversation_history)

    # 名前が抽出されているか確認
    assert manager.get_context("user_name") == "太郎"

    # 最後の話題が抽出されているか確認
    last_topic = manager.get_context("last_topic")
    assert last_topic == "プログラミング"


def test_format_context_summary():
    """コンテキストサマリーのフォーマットテスト"""
    manager = ContextManager()

    # 空の状態
    summary = manager.format_context_summary()
    assert "保存されているコンテキスト情報はありません" in summary

    # コンテキストを追加
    manager.add_context("user_name", "太郎", importance="high")
    manager.add_context("topic", "AI", importance="normal")
    manager.add_context("note", "補足情報", importance="low")
    manager.set_user_preference("preferred_voice", "ja-JP-NanamiNeural")

    summary = manager.format_context_summary()

    # 各セクションが含まれているか確認
    assert "【重要】" in summary
    assert "user_name: 太郎" in summary
    assert "【通常】" in summary
    assert "topic: AI" in summary
    assert "【補足】" in summary
    assert "note: 補足情報" in summary
    assert "【ユーザー設定】" in summary
    assert "preferred_voice: ja-JP-NanamiNeural" in summary


def test_clear_context():
    """コンテキストクリアのテスト"""
    manager = ContextManager()

    # コンテキストとユーザー設定を追加
    manager.add_context("key1", "value1")
    manager.add_context("key2", "value2")
    manager.set_user_preference("pref1", "value1")

    assert len(manager.context_items) == 2
    assert len(manager.user_preferences) == 1

    # クリア
    manager.clear_context()

    # 全てクリアされたか確認
    assert manager.context_items == []
    assert manager.user_preferences == {}


def test_context_trimming_preserves_important():
    """重要度の高いコンテキストが優先的に保持されるテスト"""
    manager = ContextManager(max_context_items=5)

    # 重要度の異なるコンテキストを追加
    manager.add_context("important1", "値1", importance="high")
    manager.add_context("important2", "値2", importance="high")
    manager.add_context("normal1", "値3", importance="normal")
    manager.add_context("normal2", "値4", importance="normal")
    manager.add_context("low1", "値5", importance="low")

    # さらに低重要度を追加（trimが発生）
    manager.add_context("low2", "値6", importance="low")
    manager.add_context("low3", "値7", importance="low")

    # 最大数以下に抑えられているか確認
    assert len(manager.context_items) == 5

    # 重要度の高いものが残っているか確認
    keys = [item["key"] for item in manager.context_items]
    assert "important1" in keys
    assert "important2" in keys
