"""
音声対話ループモジュール (voice_chat.py) のユニットテスト

VoiceChatクラスの安全機構と音声コマンド処理をテストします。
Azure Speech SDKとAgent Frameworkの呼び出しはモックで代替します。
"""

import sys
from pathlib import Path
from unittest.mock import Mock, AsyncMock, patch, MagicMock
import pytest
import time

# プロジェクトディレクトリをパスに追加
PROJECT_DIR = Path(__file__).resolve().parents[1]
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from voice_chat import VoiceChat


@pytest.fixture
def mock_session():
    """VoiceAgentSessionのモック"""
    session = Mock()
    session.send_message = AsyncMock(return_value="テスト応答")
    session.get_conversation_history = Mock(return_value=[])
    return session


@pytest.fixture
def mock_recognizer():
    """SpeechRecognizerのモック"""
    recognizer = Mock()
    recognizer.recognize_once = Mock(return_value=(True, "テスト入力"))
    return recognizer


@pytest.fixture
def mock_synthesizer():
    """SpeechSynthesizerのモック"""
    synthesizer = Mock()
    synthesizer.speak = Mock(return_value=(True, "完了"))
    synthesizer.speak_with_options = Mock(return_value=(True, "完了"))
    synthesizer.set_voice = Mock()
    return synthesizer


@pytest.fixture
def mock_settings():
    """設定のモック"""
    with patch('voice_chat.settings') as mock_set:
        mock_set.MAX_CONVERSATION_TURNS = 10
        mock_set.MAX_CONSECUTIVE_ERRORS = 3
        mock_set.MAX_SESSION_DURATION = 300  # 5分
        mock_set.EXIT_KEYWORDS = ["終了", "さようなら", "exit"]
        mock_set.is_exit_keyword = Mock(return_value=False)
        yield mock_set


def test_voice_chat_initialization(mock_session, mock_recognizer, mock_synthesizer):
    """VoiceChatの初期化テスト"""
    chat = VoiceChat(
        session=mock_session,
        recognizer=mock_recognizer,
        synthesizer=mock_synthesizer
    )

    # 初期状態の確認
    assert chat.session == mock_session
    assert chat.recognizer == mock_recognizer
    assert chat.synthesizer == mock_synthesizer
    assert chat.turn_count == 0
    assert chat.consecutive_errors == 0
    assert chat.session_start_time is None
    assert chat.current_voice_profile == "default"
    assert chat.current_speaking_rate == 1.0


def test_voice_chat_initialization_with_defaults(mock_session):
    """デフォルト引数での初期化テスト"""
    with patch('voice_chat.SpeechRecognizer'), \
         patch('voice_chat.SpeechSynthesizer'):
        chat = VoiceChat(session=mock_session)

        # recognizerとsynthesizerが自動作成されているか確認
        assert chat.recognizer is not None
        assert chat.synthesizer is not None


def test_check_safety_limits_initial(mock_session, mock_recognizer, mock_synthesizer, mock_settings):
    """安全制限チェック - 初期状態のテスト"""
    chat = VoiceChat(mock_session, mock_recognizer, mock_synthesizer)

    can_continue, stop_reason = chat._check_safety_limits()

    # 初期状態では継続可能
    assert can_continue is True
    assert stop_reason is None


def test_check_safety_limits_max_turns(mock_session, mock_recognizer, mock_synthesizer, mock_settings):
    """安全制限チェック - 最大ターン数到達のテスト"""
    chat = VoiceChat(mock_session, mock_recognizer, mock_synthesizer)

    # 最大ターン数に到達
    chat.turn_count = mock_settings.MAX_CONVERSATION_TURNS

    can_continue, stop_reason = chat._check_safety_limits()

    # 継続不可
    assert can_continue is False
    assert "最大ターン数" in stop_reason


def test_check_safety_limits_max_errors(mock_session, mock_recognizer, mock_synthesizer, mock_settings):
    """安全制限チェック - 連続エラー上限のテスト"""
    chat = VoiceChat(mock_session, mock_recognizer, mock_synthesizer)

    # 連続エラー上限に到達
    chat.consecutive_errors = mock_settings.MAX_CONSECUTIVE_ERRORS

    can_continue, stop_reason = chat._check_safety_limits()

    # 継続不可
    assert can_continue is False
    assert "連続エラー" in stop_reason


def test_check_safety_limits_max_duration(mock_session, mock_recognizer, mock_synthesizer, mock_settings):
    """安全制限チェック - 最大セッション時間超過のテスト"""
    chat = VoiceChat(mock_session, mock_recognizer, mock_synthesizer)

    # セッション開始時刻を設定（過去の時刻）
    chat.session_start_time = time.time() - (mock_settings.MAX_SESSION_DURATION + 10)

    can_continue, stop_reason = chat._check_safety_limits()

    # 継続不可
    assert can_continue is False
    assert "最大セッション時間" in stop_reason


def test_is_exit_command(mock_session, mock_recognizer, mock_synthesizer, mock_settings):
    """終了コマンド判定のテスト"""
    chat = VoiceChat(mock_session, mock_recognizer, mock_synthesizer)

    # 終了キーワードのモック
    mock_settings.is_exit_keyword.side_effect = lambda x: x in ["終了", "exit"]

    # 終了コマンド
    assert chat._is_exit_command("終了") is True
    assert chat._is_exit_command("exit") is True

    # 通常のメッセージ
    assert chat._is_exit_command("こんにちは") is False


def test_is_voice_command_summary(mock_session, mock_recognizer, mock_synthesizer, mock_settings):
    """音声コマンド判定 - 要約コマンドのテスト"""
    chat = VoiceChat(mock_session, mock_recognizer, mock_synthesizer)

    is_command, command_type = chat._is_voice_command("会話を要約して")
    assert is_command is True
    assert command_type == "summary"

    is_command, command_type = chat._is_voice_command("まとめてください")
    assert is_command is True
    assert command_type == "summary"


def test_is_voice_command_voice_change(mock_session, mock_recognizer, mock_synthesizer, mock_settings):
    """音声コマンド判定 - 音声変更コマンドのテスト"""
    chat = VoiceChat(mock_session, mock_recognizer, mock_synthesizer)

    is_command, command_type = chat._is_voice_command("音声を変更して")
    assert is_command is True
    assert command_type == "voice_change"

    is_command, command_type = chat._is_voice_command("声を切り替えて")
    assert is_command is True
    assert command_type == "voice_change"


def test_is_voice_command_speed(mock_session, mock_recognizer, mock_synthesizer, mock_settings):
    """音声コマンド判定 - 話速変更コマンドのテスト"""
    chat = VoiceChat(mock_session, mock_recognizer, mock_synthesizer)

    # 速く
    is_command, command_type = chat._is_voice_command("もっと速く話して")
    assert is_command is True
    assert command_type == "speed_up"

    # ゆっくり
    is_command, command_type = chat._is_voice_command("ゆっくり話して")
    assert is_command is True
    assert command_type == "speed_down"


def test_is_voice_command_reset(mock_session, mock_recognizer, mock_synthesizer, mock_settings):
    """音声コマンド判定 - リセットコマンドのテスト"""
    chat = VoiceChat(mock_session, mock_recognizer, mock_synthesizer)

    is_command, command_type = chat._is_voice_command("音声をリセットして")
    assert is_command is True
    assert command_type == "reset_voice"


def test_is_voice_command_none(mock_session, mock_recognizer, mock_synthesizer, mock_settings):
    """音声コマンド判定 - 通常メッセージのテスト"""
    chat = VoiceChat(mock_session, mock_recognizer, mock_synthesizer)

    is_command, command_type = chat._is_voice_command("こんにちは")
    assert is_command is False
    assert command_type is None


def test_generate_summary_empty(mock_session, mock_recognizer, mock_synthesizer, mock_settings):
    """会話要約生成 - 空の履歴のテスト"""
    chat = VoiceChat(mock_session, mock_recognizer, mock_synthesizer)

    # 空の履歴
    mock_session.get_conversation_history.return_value = []

    summary = chat._generate_summary()
    assert "まだ会話履歴がありません" in summary


def test_generate_summary_with_history(mock_session, mock_recognizer, mock_synthesizer, mock_settings):
    """会話要約生成 - 履歴ありのテスト"""
    chat = VoiceChat(mock_session, mock_recognizer, mock_synthesizer)

    # 履歴を設定
    mock_session.get_conversation_history.return_value = [
        {"role": "user", "content": "こんにちは"},
        {"role": "assistant", "content": "こんにちは。"},
    ]

    summary = chat._generate_summary()
    assert "会話の要約です" in summary


@patch('voice_chat.get_voice_profile')
def test_change_voice_profile(mock_get_profile, mock_session, mock_recognizer, mock_synthesizer, mock_settings):
    """音声プロファイル変更のテスト"""
    chat = VoiceChat(mock_session, mock_recognizer, mock_synthesizer)

    # プロファイルのモック
    mock_profile = Mock()
    mock_profile.name = "優しい声"
    mock_profile.description = "優しく穏やかな声です。"
    mock_profile.voice_name = "ja-JP-NanamiNeural"
    mock_profile.speaking_rate = 1.0
    mock_get_profile.return_value = mock_profile

    # 初期状態
    assert chat.current_voice_profile == "default"

    # プロファイル変更
    result = chat._change_voice_profile()

    # 変更されたか確認
    assert "音声を" in result
    assert mock_synthesizer.set_voice.called


def test_change_speaking_rate_faster(mock_session, mock_recognizer, mock_synthesizer, mock_settings):
    """話速変更 - 速くするテスト"""
    chat = VoiceChat(mock_session, mock_recognizer, mock_synthesizer)

    # 初期値
    assert chat.current_speaking_rate == 1.0

    # 速くする
    result = chat._change_speaking_rate(faster=True)

    # 変更されたか確認
    assert chat.current_speaking_rate == 1.25
    assert "話速を速くしました" in result


def test_change_speaking_rate_slower(mock_session, mock_recognizer, mock_synthesizer, mock_settings):
    """話速変更 - 遅くするテスト"""
    chat = VoiceChat(mock_session, mock_recognizer, mock_synthesizer)

    # 初期値
    assert chat.current_speaking_rate == 1.0

    # 遅くする
    result = chat._change_speaking_rate(faster=False)

    # 変更されたか確認
    assert chat.current_speaking_rate == 0.75
    assert "話速を遅くしました" in result


def test_change_speaking_rate_limits(mock_session, mock_recognizer, mock_synthesizer, mock_settings):
    """話速変更 - 上限・下限のテスト"""
    chat = VoiceChat(mock_session, mock_recognizer, mock_synthesizer)

    # 最速まで上げる
    for _ in range(10):
        chat._change_speaking_rate(faster=True)

    # 上限確認
    assert chat.current_speaking_rate <= 1.5

    # 最遅まで下げる
    for _ in range(20):
        chat._change_speaking_rate(faster=False)

    # 下限確認
    assert chat.current_speaking_rate >= 0.5


@patch('voice_chat.get_voice_profile')
def test_reset_voice_settings(mock_get_profile, mock_session, mock_recognizer, mock_synthesizer, mock_settings):
    """音声設定リセットのテスト"""
    chat = VoiceChat(mock_session, mock_recognizer, mock_synthesizer)

    # プロファイルのモック
    mock_profile = Mock()
    mock_profile.voice_name = "ja-JP-NanamiNeural"
    mock_get_profile.return_value = mock_profile

    # 設定を変更
    chat.current_voice_profile = "energetic"
    chat.current_speaking_rate = 1.5

    # リセット
    result = chat._reset_voice_settings()

    # デフォルトに戻ったか確認
    assert chat.current_voice_profile == "default"
    assert chat.current_speaking_rate == 1.0
    assert "リセット" in result


@pytest.mark.asyncio
async def test_handle_voice_command_summary(mock_session, mock_recognizer, mock_synthesizer, mock_settings):
    """音声コマンド処理 - 要約のテスト"""
    chat = VoiceChat(mock_session, mock_recognizer, mock_synthesizer)

    mock_session.get_conversation_history.return_value = [
        {"role": "user", "content": "test"}
    ]

    result = await chat._handle_voice_command("summary")
    assert "会話の要約です" in result


@pytest.mark.asyncio
async def test_handle_voice_command_unknown(mock_session, mock_recognizer, mock_synthesizer, mock_settings):
    """音声コマンド処理 - 不明なコマンドのテスト"""
    chat = VoiceChat(mock_session, mock_recognizer, mock_synthesizer)

    result = await chat._handle_voice_command("unknown_command")
    assert "認識できませんでした" in result


def test_print_session_statistics(mock_session, mock_recognizer, mock_synthesizer, mock_settings, capsys):
    """セッション統計表示のテスト"""
    chat = VoiceChat(mock_session, mock_recognizer, mock_synthesizer)

    # セッション情報を設定
    chat.turn_count = 5
    chat.session_start_time = time.time() - 120  # 2分前
    mock_session.get_conversation_history.return_value = [{"role": "user", "content": "test"}] * 10

    # 統計表示
    chat._print_session_statistics()

    # 出力確認
    captured = capsys.readouterr()
    assert "セッション統計" in captured.out
    assert "総ターン数: 5" in captured.out
    assert "セッション時間:" in captured.out
