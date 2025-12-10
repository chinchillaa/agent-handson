"""
統合テスト (test_integration.py)

複数のモジュールを組み合わせた統合的な動作をテストします。
外部API呼び出しはモックで代替し、コストを発生させずにテストします。
"""

import sys
from pathlib import Path
from unittest.mock import Mock, AsyncMock, patch, MagicMock
import pytest

# プロジェクトディレクトリをパスに追加
PROJECT_DIR = Path(__file__).resolve().parents[1]
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))


@pytest.fixture
def mock_all_azure_services():
    """すべてのAzureサービスをモック化"""
    with patch('speech.recognizer.speechsdk') as mock_speech_sdk, \
         patch('speech.synthesizer.speechsdk') as mock_synth_sdk, \
         patch('agents.voice_agent.create_azure_agent') as mock_create_agent:

        # Speech SDK (Recognizer)
        mock_speech_config = MagicMock()
        mock_audio_config = MagicMock()
        mock_recognizer = MagicMock()

        mock_speech_sdk.SpeechConfig.return_value = mock_speech_config
        mock_speech_sdk.AudioConfig.return_value = mock_audio_config
        mock_speech_sdk.SpeechRecognizer.return_value = mock_recognizer
        mock_speech_sdk.ResultReason.RecognizedSpeech = 0

        # Speech SDK (Synthesizer)
        mock_synth_config = MagicMock()
        mock_synth_audio = MagicMock()
        mock_synthesizer = MagicMock()

        mock_synth_sdk.SpeechConfig.return_value = mock_synth_config
        mock_synth_sdk.AudioConfig.return_value = mock_synth_audio
        mock_synth_sdk.SpeechSynthesizer.return_value = mock_synthesizer
        mock_synth_sdk.ResultReason.SynthesizingAudioCompleted = 0

        # Agent
        mock_agent = Mock()
        mock_agent.send_message = AsyncMock()
        mock_create_agent.return_value = mock_agent

        yield {
            'speech_sdk': mock_speech_sdk,
            'synth_sdk': mock_synth_sdk,
            'recognizer': mock_recognizer,
            'synthesizer': mock_synthesizer,
            'agent': mock_agent,
        }


@pytest.mark.asyncio
async def test_end_to_end_conversation_flow(mock_all_azure_services):
    """エンドツーエンドの音声対話フローテスト"""
    from speech.recognizer import SpeechRecognizer
    from speech.synthesizer import SpeechSynthesizer
    from agents.voice_agent import create_voice_agent, VoiceAgentSession
    from voice_chat import VoiceChat

    # 音声認識の成功をモック
    mock_result = Mock()
    mock_result.reason = 0  # RecognizedSpeech
    mock_result.text = "こんにちは"
    mock_all_azure_services['recognizer'].recognize_once.return_value = mock_result

    # 音声合成の成功をモック
    mock_synth_result = Mock()
    mock_synth_result.reason = 0  # SynthesizingAudioCompleted
    mock_async = MagicMock()
    mock_async.get.return_value = mock_synth_result
    mock_all_azure_services['synthesizer'].speak_text_async.return_value = mock_async

    # エージェントの応答をモック
    mock_response = Mock()
    mock_response.get_content.return_value = "こんにちは。お元気ですか？"
    mock_all_azure_services['agent'].send_message.return_value = mock_response

    # コンポーネント初期化
    recognizer = SpeechRecognizer()
    synthesizer = SpeechSynthesizer()
    agent = await create_voice_agent()
    session = VoiceAgentSession(agent)

    # 1. 音声認識
    success, user_text = recognizer.recognize_once()
    assert success is True
    assert user_text == "こんにちは"

    # 2. エージェント処理
    response = await session.send_message(user_text)
    assert response == "こんにちは。お元気ですか？"

    # 3. 音声合成
    success, _ = synthesizer.speak(response)
    assert success is True

    # 会話履歴の確認
    history = session.get_conversation_history()
    assert len(history) == 2
    assert history[0]["role"] == "user"
    assert history[0]["content"] == "こんにちは"
    assert history[1]["role"] == "assistant"
    assert history[1]["content"] == "こんにちは。お元気ですか？"


@pytest.mark.asyncio
async def test_voice_chat_with_context_manager(mock_all_azure_services):
    """VoiceChatとContextManagerの統合テスト"""
    from agents.voice_agent import VoiceAgentSession
    from voice_chat import VoiceChat
    from tools.context_manager import ContextManager

    # エージェントの応答をモック
    mock_response = Mock()
    mock_response.get_content.return_value = "テスト応答"
    mock_all_azure_services['agent'].send_message.return_value = mock_response

    # セッション作成
    session = VoiceAgentSession(mock_all_azure_services['agent'])

    # 会話履歴に名前を含むメッセージを追加
    await session.send_message("私の名前は太郎です。")

    # ContextManagerでコンテキスト抽出
    context_manager = ContextManager()
    context_manager.extract_from_conversation(session.get_conversation_history())

    # 名前が抽出されたか確認
    extracted_name = context_manager.get_context("user_name")
    assert extracted_name == "太郎"


@pytest.mark.asyncio
async def test_voice_chat_with_summarizer(mock_all_azure_services):
    """VoiceChatとConversationSummarizerの統合テスト"""
    from agents.voice_agent import VoiceAgentSession
    from tools.conversation_summarizer import ConversationSummarizer

    # エージェントの応答をモック
    mock_response = Mock()
    mock_response.get_content.return_value = "テスト応答"
    mock_all_azure_services['agent'].send_message.return_value = mock_response

    # セッション作成
    session = VoiceAgentSession(mock_all_azure_services['agent'])

    # 複数ターンの会話
    for i in range(5):
        await session.send_message(f"メッセージ{i + 1}")

    # 要約生成
    summarizer = ConversationSummarizer()
    summary = summarizer.summarize_conversation(session.get_conversation_history())

    # 統計情報の確認
    assert "会話ターン数: 5" in summary

    # 統計情報取得
    stats = summarizer.get_conversation_stats(session.get_conversation_history())
    assert stats["total_turns"] == 5
    assert stats["total_messages"] == 10


@pytest.mark.asyncio
async def test_voice_chat_safety_limits_integration(mock_all_azure_services):
    """VoiceChatの安全制限機能の統合テスト"""
    from agents.voice_agent import VoiceAgentSession
    from voice_chat import VoiceChat
    from speech.recognizer import SpeechRecognizer
    from speech.synthesizer import SpeechSynthesizer

    # モック設定
    with patch('voice_chat.settings') as mock_settings:
        mock_settings.MAX_CONVERSATION_TURNS = 3
        mock_settings.MAX_CONSECUTIVE_ERRORS = 2
        mock_settings.MAX_SESSION_DURATION = 300
        mock_settings.is_exit_keyword = Mock(return_value=False)

        # コンポーネント作成
        session = VoiceAgentSession(mock_all_azure_services['agent'])
        recognizer = SpeechRecognizer()
        synthesizer = SpeechSynthesizer()
        chat = VoiceChat(session, recognizer, synthesizer)

        # ターン数を最大に設定
        chat.turn_count = 3

        # 安全制限チェック
        can_continue, reason = chat._check_safety_limits()

        # 制限に到達したか確認
        assert can_continue is False
        assert "最大ターン数" in reason


@pytest.mark.asyncio
async def test_voice_command_integration(mock_all_azure_services):
    """音声コマンド処理の統合テスト"""
    from agents.voice_agent import VoiceAgentSession
    from voice_chat import VoiceChat
    from speech.recognizer import SpeechRecognizer
    from speech.synthesizer import SpeechSynthesizer

    with patch('voice_chat.settings') as mock_settings:
        mock_settings.MAX_CONVERSATION_TURNS = 10
        mock_settings.MAX_CONSECUTIVE_ERRORS = 3
        mock_settings.MAX_SESSION_DURATION = 300

        # エージェントの応答をモック
        mock_response = Mock()
        mock_response.get_content.return_value = "テスト応答"
        mock_all_azure_services['agent'].send_message.return_value = mock_response

        # コンポーネント作成
        session = VoiceAgentSession(mock_all_azure_services['agent'])
        recognizer = SpeechRecognizer()
        synthesizer = SpeechSynthesizer()
        chat = VoiceChat(session, recognizer, synthesizer)

        # 会話履歴を追加
        await session.send_message("こんにちは")
        await session.send_message("今日の天気は？")

        # 要約コマンド
        is_command, command_type = chat._is_voice_command("会話を要約して")
        assert is_command is True
        assert command_type == "summary"

        # コマンド処理
        result = await chat._handle_voice_command(command_type)
        assert "会話の要約です" in result


@pytest.mark.asyncio
async def test_multiple_turn_conversation_with_tools(mock_all_azure_services):
    """複数ターンの会話とツール機能の統合テスト"""
    from agents.voice_agent import VoiceAgentSession
    from tools.context_manager import ContextManager
    from tools.conversation_summarizer import ConversationSummarizer

    # エージェントの応答をモック
    responses = [
        "こんにちは、太郎さん。",
        "今日は晴れです。",
        "Pythonは使いやすい言語です。",
    ]

    mock_responses = []
    for resp in responses:
        mock_resp = Mock()
        mock_resp.get_content.return_value = resp
        mock_responses.append(mock_resp)

    mock_all_azure_services['agent'].send_message.side_effect = mock_responses

    # セッション作成
    session = VoiceAgentSession(mock_all_azure_services['agent'])
    context_manager = ContextManager()
    summarizer = ConversationSummarizer()

    # 複数ターンの会話
    test_messages = [
        "私の名前は太郎です。",
        "今日の天気は？",
        "Pythonについて教えて。",
    ]

    for message in test_messages:
        await session.send_message(message)
        # コンテキスト抽出
        context_manager.extract_from_conversation(session.get_conversation_history())

    # コンテキスト確認
    user_name = context_manager.get_context("user_name")
    assert user_name == "太郎"

    # 話題確認
    last_topic = context_manager.get_context("last_topic")
    assert last_topic == "プログラミング"

    # 要約確認
    summary = summarizer.summarize_conversation(session.get_conversation_history())
    assert "会話ターン数: 3" in summary

    # 統計確認
    stats = summarizer.get_conversation_stats(session.get_conversation_history())
    assert stats["total_turns"] == 3
    assert stats["user_messages"] == 3
    assert stats["assistant_messages"] == 3


@pytest.mark.asyncio
async def test_error_recovery_integration(mock_all_azure_services):
    """エラーリカバリーの統合テスト"""
    from speech.recognizer import SpeechRecognizer
    from agents.voice_agent import VoiceAgentSession

    # 1回目は失敗、2回目は成功
    mock_result_fail = Mock()
    mock_result_fail.reason = 1  # NoMatch

    mock_result_success = Mock()
    mock_result_success.reason = 0  # RecognizedSpeech
    mock_result_success.text = "成功"

    mock_all_azure_services['recognizer'].recognize_once.side_effect = [
        mock_result_fail,
        mock_result_success,
    ]

    # 音声認識器作成
    recognizer = SpeechRecognizer()

    # 1回目（失敗）
    success1, result1 = recognizer.recognize_once()
    assert success1 is False

    # 2回目（成功）
    success2, result2 = recognizer.recognize_once()
    assert success2 is True
    assert result2 == "成功"


@pytest.mark.asyncio
async def test_session_history_management(mock_all_azure_services):
    """セッション履歴管理の統合テスト"""
    from agents.voice_agent import VoiceAgentSession

    # エージェントの応答をモック
    mock_response = Mock()
    mock_response.get_content.return_value = "応答"
    mock_all_azure_services['agent'].send_message.return_value = mock_response

    # セッション作成
    session = VoiceAgentSession(mock_all_azure_services['agent'])

    # 会話を追加
    for i in range(5):
        await session.send_message(f"メッセージ{i + 1}")

    # 履歴確認
    history = session.get_conversation_history()
    assert len(history) == 10  # 5ターン = 10メッセージ

    # ターン数確認
    assert session.get_turn_count() == 5

    # 履歴クリア
    session.clear_history()
    assert len(session.get_conversation_history()) == 0
    assert session.get_turn_count() == 0


def test_configuration_validation_integration():
    """設定バリデーションの統合テスト"""
    from config.settings import Settings
    import os
    from unittest.mock import patch

    # 必須環境変数が揃っている場合
    test_env = {
        'AZURE_OPENAI_ENDPOINT': 'https://test.openai.azure.com/',
        'AZURE_OPENAI_API_KEY': 'test-key',
        'AZURE_SPEECH_API_KEY': 'speech-key',
        'AZURE_SPEECH_REGION': 'eastus',
    }

    with patch.dict(os.environ, test_env, clear=True):
        import importlib
        if 'config.settings' in sys.modules:
            importlib.reload(sys.modules['config.settings'])
        from config.settings import Settings

        # バリデーション成功（例外が発生しない）
        try:
            Settings.validate()
            validation_success = True
        except ValueError:
            validation_success = False

        assert validation_success is True
