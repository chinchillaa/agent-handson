"""
音声認識モジュール (speech/recognizer.py) のユニットテスト

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

from speech.recognizer import SpeechRecognizer


@pytest.fixture
def mock_speech_sdk():
    """Azure Speech SDKのモック"""
    with patch('speech.recognizer.speechsdk') as mock_sdk:
        # SpeechConfigのモック
        mock_config = MagicMock()
        mock_sdk.SpeechConfig.return_value = mock_config

        # AudioConfigのモック
        mock_audio = MagicMock()
        mock_sdk.AudioConfig.return_value = mock_audio

        # SpeechRecognizerのモック
        mock_recognizer = MagicMock()
        mock_sdk.SpeechRecognizer.return_value = mock_recognizer

        # ResultReasonのモック（列挙型）
        mock_sdk.ResultReason.RecognizedSpeech = 0
        mock_sdk.ResultReason.NoMatch = 1
        mock_sdk.ResultReason.Canceled = 2

        yield {
            'sdk': mock_sdk,
            'config': mock_config,
            'audio': mock_audio,
            'recognizer': mock_recognizer
        }


@pytest.fixture
def mock_settings():
    """設定のモック"""
    with patch('speech.recognizer.settings') as mock_set:
        mock_set.AZURE_SPEECH_API_KEY = "test-api-key"
        mock_set.AZURE_SPEECH_REGION = "test-region"
        mock_set.AZURE_SPEECH_LANGUAGE = "ja-JP"
        mock_set.SPEECH_RECOGNITION_TIMEOUT = 10
        yield mock_set


def test_recognizer_initialization(mock_speech_sdk, mock_settings):
    """音声認識器の初期化テスト"""
    recognizer = SpeechRecognizer()

    # 設定が正しく読み込まれているか確認
    assert recognizer.api_key == "test-api-key"
    assert recognizer.region == "test-region"
    assert recognizer.language == "ja-JP"
    assert recognizer.timeout == 10

    # Speech SDKが正しく呼ばれているか確認
    mock_speech_sdk['sdk'].SpeechConfig.assert_called_once_with(
        subscription="test-api-key",
        region="test-region"
    )


def test_recognize_once_success(mock_speech_sdk, mock_settings):
    """音声認識成功のテスト"""
    # 認識結果のモック
    mock_result = Mock()
    mock_result.reason = mock_speech_sdk['sdk'].ResultReason.RecognizedSpeech
    mock_result.text = "こんにちは"

    mock_speech_sdk['recognizer'].recognize_once.return_value = mock_result

    # 音声認識実行
    recognizer = SpeechRecognizer()
    success, text = recognizer.recognize_once()

    # 結果確認
    assert success is True
    assert text == "こんにちは"


def test_recognize_once_no_match(mock_speech_sdk, mock_settings):
    """音声が認識できない場合のテスト（無音・雑音）"""
    # NoMatch結果のモック
    mock_result = Mock()
    mock_result.reason = mock_speech_sdk['sdk'].ResultReason.NoMatch

    mock_speech_sdk['recognizer'].recognize_once.return_value = mock_result

    # 音声認識実行
    recognizer = SpeechRecognizer()
    success, message = recognizer.recognize_once()

    # 結果確認
    assert success is False
    assert "認識できませんでした" in message


def test_recognize_once_canceled(mock_speech_sdk, mock_settings):
    """音声認識がキャンセルされた場合のテスト"""
    # Canceled結果のモック
    mock_result = Mock()
    mock_result.reason = mock_speech_sdk['sdk'].ResultReason.Canceled
    mock_result.cancellation_details = Mock()
    mock_result.cancellation_details.reason = "TimeoutError"

    mock_speech_sdk['recognizer'].recognize_once.return_value = mock_result

    # 音声認識実行
    recognizer = SpeechRecognizer()
    success, message = recognizer.recognize_once()

    # 結果確認
    assert success is False
    assert "キャンセル" in message


def test_recognizer_custom_parameters(mock_speech_sdk):
    """カスタムパラメータでの初期化テスト"""
    recognizer = SpeechRecognizer(
        api_key="custom-key",
        region="custom-region",
        language="en-US",
        timeout=20
    )

    # カスタムパラメータが設定されているか確認
    assert recognizer.api_key == "custom-key"
    assert recognizer.region == "custom-region"
    assert recognizer.language == "en-US"
    assert recognizer.timeout == 20

    # Speech SDKにカスタム値が渡されているか確認
    mock_speech_sdk['sdk'].SpeechConfig.assert_called_once_with(
        subscription="custom-key",
        region="custom-region"
    )


def test_recognize_once_exception_handling(mock_speech_sdk, mock_settings):
    """例外発生時のエラーハンドリングテスト"""
    # 例外をスローするモック
    mock_speech_sdk['recognizer'].recognize_once.side_effect = Exception("Network error")

    # 音声認識実行
    recognizer = SpeechRecognizer()
    success, message = recognizer.recognize_once()

    # 結果確認
    assert success is False
    assert "エラー" in message or "Network error" in message
