"""
設定モジュール (config/settings.py) のユニットテスト

環境変数の読み込みとバリデーションをテストします。
"""

import sys
import os
from pathlib import Path
from unittest.mock import patch
import pytest

# プロジェクトディレクトリをパスに追加
PROJECT_DIR = Path(__file__).resolve().parents[1]
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))


def test_settings_default_values():
    """デフォルト値のテスト"""
    # 環境変数をクリアして再インポート
    with patch.dict(os.environ, {}, clear=True):
        # モジュールを再読み込み
        import importlib
        if 'config.settings' in sys.modules:
            importlib.reload(sys.modules['config.settings'])
        from config.settings import Settings

        # デフォルト値の確認
        assert Settings.AZURE_OPENAI_API_VERSION == "2024-08-01-preview"
        assert Settings.AZURE_REGION == "eastus2"
        assert Settings.AZURE_SPEECH_LANGUAGE == "ja-JP"
        assert Settings.AZURE_SPEECH_VOICE_NAME == "ja-JP-NanamiNeural"
        assert Settings.MAX_CONVERSATION_TURNS == 50
        assert Settings.MAX_CONSECUTIVE_ERRORS == 3
        assert Settings.MAX_SESSION_DURATION == 1800


def test_settings_environment_variables():
    """環境変数からの読み込みテスト"""
    test_env = {
        'AZURE_OPENAI_ENDPOINT': 'https://test.openai.azure.com/',
        'AZURE_OPENAI_API_KEY': 'test-key-12345',
        'AZURE_SPEECH_API_KEY': 'speech-key-67890',
        'AZURE_SPEECH_REGION': 'westus',
        'MAX_CONVERSATION_TURNS': '100',
        'MAX_CONSECUTIVE_ERRORS': '5',
    }

    with patch.dict(os.environ, test_env, clear=True):
        # モジュールを再読み込み
        import importlib
        if 'config.settings' in sys.modules:
            importlib.reload(sys.modules['config.settings'])
        from config.settings import Settings

        # 環境変数の値が正しく読み込まれているか確認
        assert Settings.AZURE_OPENAI_ENDPOINT == 'https://test.openai.azure.com/'
        assert Settings.AZURE_OPENAI_API_KEY == 'test-key-12345'
        assert Settings.AZURE_SPEECH_API_KEY == 'speech-key-67890'
        assert Settings.AZURE_SPEECH_REGION == 'westus'
        assert Settings.MAX_CONVERSATION_TURNS == 100
        assert Settings.MAX_CONSECUTIVE_ERRORS == 5


def test_settings_integer_conversion():
    """整数型環境変数の変換テスト"""
    test_env = {
        'MAX_RETRIES': '10',
        'TIMEOUT_SECONDS': '120',
        'GPT5_MAX_TOKENS': '8192',
        'SPEECH_RECOGNITION_TIMEOUT': '15',
    }

    with patch.dict(os.environ, test_env, clear=True):
        import importlib
        if 'config.settings' in sys.modules:
            importlib.reload(sys.modules['config.settings'])
        from config.settings import Settings

        # 整数への変換が正しく行われているか確認
        assert Settings.MAX_RETRIES == 10
        assert Settings.TIMEOUT_SECONDS == 120
        assert Settings.GPT5_MAX_TOKENS == 8192
        assert Settings.SPEECH_RECOGNITION_TIMEOUT == 15
        assert isinstance(Settings.MAX_RETRIES, int)


def test_settings_float_conversion():
    """浮動小数点型環境変数の変換テスト"""
    test_env = {
        'GPT5_TEMPERATURE': '0.9',
    }

    with patch.dict(os.environ, test_env, clear=True):
        import importlib
        if 'config.settings' in sys.modules:
            importlib.reload(sys.modules['config.settings'])
        from config.settings import Settings

        # 浮動小数点への変換が正しく行われているか確認
        assert Settings.GPT5_TEMPERATURE == 0.9
        assert isinstance(Settings.GPT5_TEMPERATURE, float)


def test_settings_validate_success():
    """バリデーション成功のテスト"""
    test_env = {
        'AZURE_OPENAI_ENDPOINT': 'https://test.openai.azure.com/',
        'AZURE_OPENAI_API_KEY': 'test-key',
        'AZURE_SPEECH_API_KEY': 'speech-key',
        'AZURE_SPEECH_REGION': 'japaneast',
    }

    with patch.dict(os.environ, test_env, clear=True):
        import importlib
        if 'config.settings' in sys.modules:
            importlib.reload(sys.modules['config.settings'])
        from config.settings import Settings

        # バリデーションが成功することを確認（例外が発生しない）
        try:
            Settings.validate()
        except ValueError:
            pytest.fail("Validation should not raise ValueError with all required settings")


def test_settings_validate_missing_openai_endpoint():
    """OpenAIエンドポイント未設定時のバリデーションテスト"""
    test_env = {
        'AZURE_SPEECH_API_KEY': 'speech-key',
        'AZURE_SPEECH_REGION': 'japaneast',
    }

    with patch.dict(os.environ, test_env, clear=True):
        import importlib
        if 'config.settings' in sys.modules:
            importlib.reload(sys.modules['config.settings'])
        from config.settings import Settings

        # AZURE_OPENAI_ENDPOINTが未設定の場合、ValueErrorが発生することを確認
        with pytest.raises(ValueError, match="AZURE_OPENAI_ENDPOINT"):
            Settings.validate()


def test_settings_validate_missing_speech_api_key():
    """Speech API Key未設定時のバリデーションテスト"""
    test_env = {
        'AZURE_OPENAI_ENDPOINT': 'https://test.openai.azure.com/',
        'AZURE_OPENAI_API_KEY': 'test-key',
        'AZURE_SPEECH_REGION': 'japaneast',
    }

    with patch.dict(os.environ, test_env, clear=True):
        import importlib
        if 'config.settings' in sys.modules:
            importlib.reload(sys.modules['config.settings'])
        from config.settings import Settings

        # AZURE_SPEECH_API_KEYが未設定の場合、ValueErrorが発生することを確認
        with pytest.raises(ValueError, match="AZURE_SPEECH_API_KEY"):
            Settings.validate()


def test_settings_validate_missing_speech_region():
    """Speech Region未設定時のバリデーションテスト"""
    test_env = {
        'AZURE_OPENAI_ENDPOINT': 'https://test.openai.azure.com/',
        'AZURE_OPENAI_API_KEY': 'test-key',
        'AZURE_SPEECH_API_KEY': 'speech-key',
    }

    with patch.dict(os.environ, test_env, clear=True):
        import importlib
        if 'config.settings' in sys.modules:
            importlib.reload(sys.modules['config.settings'])
        from config.settings import Settings

        # AZURE_SPEECH_REGIONが未設定の場合、ValueErrorが発生することを確認
        with pytest.raises(ValueError, match="AZURE_SPEECH_REGION"):
            Settings.validate()


def test_exit_keywords():
    """終了キーワードのテスト"""
    from config.settings import Settings

    # EXIT_KEYWORDSが正しく定義されているか確認
    assert isinstance(Settings.EXIT_KEYWORDS, list)
    assert len(Settings.EXIT_KEYWORDS) > 0
    assert "終了" in Settings.EXIT_KEYWORDS
    assert "exit" in Settings.EXIT_KEYWORDS


def test_settings_is_exit_keyword():
    """is_exit_keyword メソッドのテスト"""
    from config.settings import settings

    # 終了キーワードの検出
    assert settings.is_exit_keyword("終了") is True
    assert settings.is_exit_keyword("さようなら") is True
    assert settings.is_exit_keyword("exit") is True
    assert settings.is_exit_keyword("こんにちは") is False
    assert settings.is_exit_keyword("") is False
