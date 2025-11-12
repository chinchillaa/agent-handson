"""
Speech-to-Text（音声認識）モジュール

Azure Speech Serviceを使用して音声をテキストに変換します。
"""

import azure.cognitiveservices.speech as speechsdk
from typing import Optional
from ..config.settings import settings


class SpeechRecognizer:
    """音声認識クラス"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        region: Optional[str] = None,
        language: Optional[str] = None,
        timeout: Optional[int] = None,
    ):
        """
        音声認識の初期化

        Args:
            api_key: Azure Speech Service API Key（省略時は設定から取得）
            region: Azureリージョン（省略時は設定から取得）
            language: 認識言語（省略時は設定から取得）
            timeout: タイムアウト秒数（省略時は設定から取得）
        """
        self.api_key = api_key or settings.AZURE_SPEECH_API_KEY
        self.region = region or settings.AZURE_SPEECH_REGION
        self.language = language or settings.AZURE_SPEECH_LANGUAGE
        self.timeout = timeout or settings.SPEECH_RECOGNITION_TIMEOUT

        # Speech設定
        self.speech_config = speechsdk.SpeechConfig(
            subscription=self.api_key,
            region=self.region
        )
        self.speech_config.speech_recognition_language = self.language

        # オーディオ設定（デフォルトマイク使用）
        self.audio_config = speechsdk.AudioConfig(use_default_microphone=True)

        # 音声認識器
        self.recognizer = speechsdk.SpeechRecognizer(
            speech_config=self.speech_config,
            audio_config=self.audio_config
        )

    def recognize_once(self) -> tuple[bool, str]:
        """
        1回の音声入力を認識

        Returns:
            (成功フラグ, 認識結果テキスト)のタプル
            成功時: (True, "認識されたテキスト")
            失敗時: (False, エラーメッセージ)
        """
        try:
            print("🎤 音声入力を待機中... (話しかけてください)")

            # 音声認識を実行
            result = self.recognizer.recognize_once()

            # 結果の判定
            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                text = result.text
                print(f"✅ 認識結果: {text}")
                return True, text

            elif result.reason == speechsdk.ResultReason.NoMatch:
                error_msg = "⚠️  音声が認識できませんでした（無音または雑音）"
                print(error_msg)
                return False, error_msg

            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation = result.cancellation_details
                error_msg = f"❌ 音声認識がキャンセルされました: {cancellation.reason}"

                if cancellation.reason == speechsdk.CancellationReason.Error:
                    error_msg += f"\nエラー詳細: {cancellation.error_details}"

                print(error_msg)
                return False, error_msg

            else:
                error_msg = f"⚠️  予期しない結果: {result.reason}"
                print(error_msg)
                return False, error_msg

        except Exception as e:
            error_msg = f"❌ 音声認識エラー: {str(e)}"
            print(error_msg)
            return False, error_msg

    def recognize_continuous_start(self, callback_func):
        """
        連続音声認識を開始（イベントドリブン）

        Args:
            callback_func: 認識結果を受け取るコールバック関数
                          引数: (text: str)
        """
        def recognized_handler(evt):
            """認識成功時のハンドラ"""
            if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
                callback_func(evt.result.text)

        # イベントハンドラを登録
        self.recognizer.recognized.connect(recognized_handler)

        # 連続認識を開始
        print("🎤 連続音声認識を開始しました...")
        self.recognizer.start_continuous_recognition()

    def recognize_continuous_stop(self):
        """連続音声認識を停止"""
        self.recognizer.stop_continuous_recognition()
        print("⏹  連続音声認識を停止しました")

    def test_microphone(self) -> bool:
        """
        マイクの動作確認

        Returns:
            マイクが正常に動作している場合True
        """
        try:
            print("🔊 マイクのテスト中...")
            result = self.recognizer.recognize_once()

            if result.reason in [
                speechsdk.ResultReason.RecognizedSpeech,
                speechsdk.ResultReason.NoMatch
            ]:
                print("✅ マイクは正常に動作しています")
                return True
            else:
                print("❌ マイクの動作に問題があります")
                return False

        except Exception as e:
            print(f"❌ マイクテストエラー: {str(e)}")
            return False


def recognize_speech_once() -> Optional[str]:
    """
    音声を1回認識する簡易関数

    Returns:
        認識されたテキスト（失敗時はNone）
    """
    recognizer = SpeechRecognizer()
    success, text = recognizer.recognize_once()

    if success:
        return text
    else:
        return None


if __name__ == "__main__":
    """テスト実行"""
    print("=== Speech-to-Text テスト ===")
    print("話しかけてください...")

    recognizer = SpeechRecognizer()
    success, text = recognizer.recognize_once()

    if success:
        print(f"\n【認識結果】")
        print(f"  {text}")
    else:
        print(f"\n【失敗】")
        print(f"  {text}")
