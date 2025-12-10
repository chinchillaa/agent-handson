"""
音声合成モジュール (speech/synthesizer.py) のユニットテスト

Azure Speech SDKの呼び出しはモックで代替します。
"""

import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import pytest

# プロジェクトディレクトリをパスに追加
PROJECT_DIR = Path(__file__).resolve().parents[1]
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from speech.synthesizer import SpeechSynthesizer


@pytest.fixture
def mock_speech_sdk():
    """Azure Speech SDKのモック"""
    with patch('speech.synthesizer.speechsdk') as mock_sdk:
        # SpeechConfigのモック
        mock_config = MagicMock()
        mock_sdk.SpeechConfig.return_value = mock_config

        # AudioConfigのモック
        mock_audio = MagicMock()
        mock_sdk.AudioConfig.return_value = mock_audio

        # SpeechSynthesizerのモック
        mock_synthesizer = MagicMock()
        mock_sdk.SpeechSynthesizer.return_value = mock_synthesizer

        # ResultReasonのモック
        mock_sdk.ResultReason.SynthesizingAudioCompleted = 0
        mock_sdk.ResultReason.Canceled = 1

        yield {
            'sdk': mock_sdk,
            'config': mock_config,
            'audio': mock_audio,
            'synthesizer': mock_synthesizer
        }


@pytest.fixture
def mock_settings():
    """設定のモック"""
    with patch('speech.synthesizer.settings') as mock_set:
        mock_set.AZURE_SPEECH_API_KEY = "test-api-key"
        mock_set.AZURE_SPEECH_REGION = "test-region"
        mock_set.AZURE_SPEECH_VOICE_NAME = "ja-JP-NanamiNeural"
        mock_set.AZURE_SPEECH_LANGUAGE = "ja-JP"
        yield mock_set


def test_synthesizer_initialization(mock_speech_sdk, mock_settings):
    """音声合成器の初期化テスト"""
    synthesizer = SpeechSynthesizer()

    # 設定が正しく読み込まれているか確認
    assert synthesizer.api_key == "test-api-key"
    assert synthesizer.region == "test-region"
    assert synthesizer.voice_name == "ja-JP-NanamiNeural"
    assert synthesizer.language == "ja-JP"

    # Speech SDKが正しく呼ばれているか確認
    mock_speech_sdk['sdk'].SpeechConfig.assert_called_once_with(
        subscription="test-api-key",
        region="test-region"
    )


def test_speak_success(mock_speech_sdk, mock_settings):
    """音声合成成功のテスト"""
    # 合成結果のモック
    mock_result = Mock()
    mock_result.reason = mock_speech_sdk['sdk'].ResultReason.SynthesizingAudioCompleted

    # 非同期メソッドのモック
    mock_async = MagicMock()
    mock_async.get.return_value = mock_result
    mock_speech_sdk['synthesizer'].speak_text_async.return_value = mock_async

    # 音声合成実行
    synthesizer = SpeechSynthesizer()
    success, message = synthesizer.speak("こんにちは")

    # 結果確認
    assert success is True
    assert "完了" in message


def test_speak_empty_text(mock_speech_sdk, mock_settings):
    """空のテキストでの音声合成テスト"""
    synthesizer = SpeechSynthesizer()

    # 空文字列
    success, message = synthesizer.speak("")
    assert success is False
    assert "空" in message

    # スペースのみ
    success, message = synthesizer.speak("   ")
    assert success is False
    assert "空" in message


def test_speak_canceled(mock_speech_sdk, mock_settings):
    """音声合成がキャンセルされた場合のテスト"""
    # Canceled結果のモック
    mock_result = Mock()
    mock_result.reason = mock_speech_sdk['sdk'].ResultReason.Canceled
    mock_result.cancellation_details = Mock()
    mock_result.cancellation_details.reason = "Error"
    mock_result.cancellation_details.error_details = "API Error"

    # 非同期メソッドのモック
    mock_async = MagicMock()
    mock_async.get.return_value = mock_result
    mock_speech_sdk['synthesizer'].speak_text_async.return_value = mock_async

    # 音声合成実行
    synthesizer = SpeechSynthesizer()
    success, message = synthesizer.speak("テストテキスト")

    # 結果確認
    assert success is False
    assert "キャンセル" in message or "エラー" in message


def test_synthesizer_custom_parameters(mock_speech_sdk):
    """カスタムパラメータでの初期化テスト"""
    synthesizer = SpeechSynthesizer(
        api_key="custom-key",
        region="custom-region",
        voice_name="en-US-JennyNeural",
        language="en-US"
    )

    # カスタムパラメータが設定されているか確認
    assert synthesizer.api_key == "custom-key"
    assert synthesizer.region == "custom-region"
    assert synthesizer.voice_name == "en-US-JennyNeural"
    assert synthesizer.language == "en-US"


def test_set_voice(mock_speech_sdk, mock_settings):
    """音声設定変更のテスト"""
    synthesizer = SpeechSynthesizer()

    # 初期音声
    assert synthesizer.voice_name == "ja-JP-NanamiNeural"

    # 音声変更
    synthesizer.set_voice("ja-JP-KeitaNeural")
    assert synthesizer.voice_name == "ja-JP-KeitaNeural"


def test_speak_with_options(mock_speech_sdk, mock_settings):
    """オプション付き音声合成のテスト"""
    # 合成結果のモック
    mock_result = Mock()
    mock_result.reason = mock_speech_sdk['sdk'].ResultReason.SynthesizingAudioCompleted

    # 非同期メソッドのモック（SSMLベース）
    mock_async = MagicMock()
    mock_async.get.return_value = mock_result
    mock_speech_sdk['synthesizer'].speak_ssml_async.return_value = mock_async

    # 音声合成実行（話速指定）
    synthesizer = SpeechSynthesizer()
    success, message = synthesizer.speak_with_options("こんにちは", rate=1.2)

    # 結果確認
    assert success is True
    assert "完了" in message

    # SSMLメソッドが呼ばれたか確認
    mock_speech_sdk['synthesizer'].speak_ssml_async.assert_called_once()


def test_speak_exception_handling(mock_speech_sdk, mock_settings):
    """例外発生時のエラーハンドリングテスト"""
    # 例外をスローするモック
    mock_speech_sdk['synthesizer'].speak_text_async.side_effect = Exception("Network error")

    # 音声合成実行
    synthesizer = SpeechSynthesizer()
    success, message = synthesizer.speak("テスト")

    # 結果確認
    assert success is False
    assert "エラー" in message or "Network error" in message
