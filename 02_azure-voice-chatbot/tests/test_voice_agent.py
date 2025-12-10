"""
音声対話エージェントモジュール (agents/voice_agent.py) のユニットテスト

VoiceAgentSessionクラスの会話管理機能をテストします。
Agent Frameworkの呼び出しはモックで代替します。
"""

import sys
from pathlib import Path
from unittest.mock import Mock, AsyncMock, patch
import pytest

# プロジェクトディレクトリをパスに追加
PROJECT_DIR = Path(__file__).resolve().parents[1]
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from agents.voice_agent import VoiceAgentSession


@pytest.fixture
def mock_agent():
    """ChatAgentのモック"""
    agent = Mock()
    agent.send_message = AsyncMock()
    return agent


def test_voice_agent_session_initialization(mock_agent):
    """VoiceAgentSessionの初期化テスト"""
    session = VoiceAgentSession(mock_agent)

    # 初期状態の確認
    assert session.agent == mock_agent
    assert session.conversation_history == []


@pytest.mark.asyncio
async def test_send_message_success(mock_agent):
    """メッセージ送信成功のテスト"""
    session = VoiceAgentSession(mock_agent)

    # モックの応答設定
    mock_response = Mock()
    mock_response.get_content.return_value = "こんにちは。お元気ですか？"
    mock_agent.send_message.return_value = mock_response

    # メッセージ送信
    user_input = "こんにちは"
    response = await session.send_message(user_input)

    # 応答の確認
    assert response == "こんにちは。お元気ですか？"

    # エージェントが呼ばれたか確認
    mock_agent.send_message.assert_called_once_with(user_input)

    # 会話履歴に追加されたか確認
    assert len(session.conversation_history) == 2
    assert session.conversation_history[0] == {"role": "user", "content": user_input}
    assert session.conversation_history[1] == {"role": "assistant", "content": response}


@pytest.mark.asyncio
async def test_send_message_multiple_turns(mock_agent):
    """複数ターンの会話テスト"""
    session = VoiceAgentSession(mock_agent)

    # 1回目
    mock_response1 = Mock()
    mock_response1.get_content.return_value = "こんにちは。"
    mock_agent.send_message.return_value = mock_response1

    await session.send_message("こんにちは")

    # 2回目
    mock_response2 = Mock()
    mock_response2.get_content.return_value = "晴れです。"
    mock_agent.send_message.return_value = mock_response2

    await session.send_message("今日の天気は？")

    # 3回目
    mock_response3 = Mock()
    mock_response3.get_content.return_value = "どういたしまして。"
    mock_agent.send_message.return_value = mock_response3

    await session.send_message("ありがとう")

    # 会話履歴の確認（3ターン = 6メッセージ）
    assert len(session.conversation_history) == 6
    assert session.get_turn_count() == 3


def test_get_conversation_history(mock_agent):
    """会話履歴取得のテスト"""
    session = VoiceAgentSession(mock_agent)

    # 空の状態
    assert session.get_conversation_history() == []

    # 手動で履歴を追加
    session.conversation_history.append({"role": "user", "content": "test1"})
    session.conversation_history.append({"role": "assistant", "content": "response1"})

    history = session.get_conversation_history()

    # コピーが返されるか確認
    assert len(history) == 2
    assert history[0] == {"role": "user", "content": "test1"}
    assert history[1] == {"role": "assistant", "content": "response1"}

    # 元の履歴が変更されないか確認
    history.append({"role": "user", "content": "test2"})
    assert len(session.conversation_history) == 2


def test_clear_history(mock_agent, capsys):
    """会話履歴クリアのテスト"""
    session = VoiceAgentSession(mock_agent)

    # 履歴を追加
    session.conversation_history.append({"role": "user", "content": "test1"})
    session.conversation_history.append({"role": "assistant", "content": "response1"})
    assert len(session.conversation_history) == 2

    # クリア
    session.clear_history()

    # 履歴が空になったか確認
    assert session.conversation_history == []

    # メッセージが出力されたか確認
    captured = capsys.readouterr()
    assert "会話履歴をクリアしました" in captured.out


def test_get_turn_count_empty(mock_agent):
    """空の会話履歴でのターン数取得テスト"""
    session = VoiceAgentSession(mock_agent)

    assert session.get_turn_count() == 0


def test_get_turn_count_with_messages(mock_agent):
    """メッセージありの会話履歴でのターン数取得テスト"""
    session = VoiceAgentSession(mock_agent)

    # ユーザーとアシスタントのメッセージを追加
    session.conversation_history.append({"role": "user", "content": "msg1"})
    session.conversation_history.append({"role": "assistant", "content": "resp1"})
    session.conversation_history.append({"role": "user", "content": "msg2"})
    session.conversation_history.append({"role": "assistant", "content": "resp2"})
    session.conversation_history.append({"role": "user", "content": "msg3"})

    # ユーザー発話のみカウント
    assert session.get_turn_count() == 3


def test_get_turn_count_assistant_only(mock_agent):
    """アシスタントのみのメッセージでのターン数テスト"""
    session = VoiceAgentSession(mock_agent)

    # アシスタントメッセージのみ追加
    session.conversation_history.append({"role": "assistant", "content": "resp1"})
    session.conversation_history.append({"role": "assistant", "content": "resp2"})

    # ユーザー発話がないのでターン数は0
    assert session.get_turn_count() == 0


@pytest.mark.asyncio
async def test_send_message_preserves_order(mock_agent):
    """メッセージの順序が保持されるテスト"""
    session = VoiceAgentSession(mock_agent)

    # 複数回メッセージ送信
    messages = [
        ("message1", "response1"),
        ("message2", "response2"),
        ("message3", "response3"),
    ]

    for user_msg, assistant_msg in messages:
        mock_response = Mock()
        mock_response.get_content.return_value = assistant_msg
        mock_agent.send_message.return_value = mock_response

        await session.send_message(user_msg)

    # 順序が保持されているか確認
    history = session.get_conversation_history()
    assert len(history) == 6

    for i, (user_msg, assistant_msg) in enumerate(messages):
        assert history[i * 2] == {"role": "user", "content": user_msg}
        assert history[i * 2 + 1] == {"role": "assistant", "content": assistant_msg}


@pytest.mark.asyncio
async def test_send_message_with_empty_string(mock_agent):
    """空文字列のメッセージ送信テスト"""
    session = VoiceAgentSession(mock_agent)

    # 空の応答
    mock_response = Mock()
    mock_response.get_content.return_value = ""
    mock_agent.send_message.return_value = mock_response

    response = await session.send_message("")

    # 空文字列でも履歴に追加される
    assert response == ""
    assert len(session.conversation_history) == 2
    assert session.conversation_history[0]["content"] == ""
