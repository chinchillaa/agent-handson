"""
Text-to-Speech（音声合成）モジュール

Azure Speech Serviceを使用してテキストを音声に変換します。
"""

import azure.cognitiveservices.speech as speechsdk
from typing import Optional
from config.settings import settings


class SpeechSynthesizer:
    """音声合成クラス"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        region: Optional[str] = None,
        voice_name: Optional[str] = None,
        language: Optional[str] = None,
    ):
        """
        音声合成の初期化

        Args:
            api_key: Azure Speech Service API Key（省略時は設定から取得）
            region: Azureリージョン（省略時は設定から取得）
            voice_name: 音声名（省略時は設定から取得）
            language: 言語（省略時は設定から取得）
        """
        self.api_key = api_key or settings.AZURE_SPEECH_API_KEY
        self.region = region or settings.AZURE_SPEECH_REGION
        self.voice_name = voice_name or settings.AZURE_SPEECH_VOICE_NAME
        self.language = language or settings.AZURE_SPEECH_LANGUAGE

        # Speech設定
        self.speech_config = speechsdk.SpeechConfig(
            subscription=self.api_key,
            region=self.region
        )

        # 音声設定
        self.speech_config.speech_synthesis_voice_name = self.voice_name
        self.speech_config.speech_synthesis_language = self.language

        # オーディオ設定（デフォルトスピーカー使用）
        self.audio_config = speechsdk.AudioConfig(use_default_speaker=True)

        # 音声合成器
        self.synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=self.speech_config,
            audio_config=self.audio_config
        )

    def speak(self, text: str) -> tuple[bool, str]:
        """
        テキストを音声で読み上げる

        Args:
            text: 読み上げるテキスト

        Returns:
            (成功フラグ, メッセージ)のタプル
            成功時: (True, "音声合成が完了しました")
            失敗時: (False, エラーメッセージ)
        """
        try:
            if not text or not text.strip():
                return False, "⚠️  読み上げるテキストが空です"

            print(f"🔊 音声合成中: {text[:50]}...")

            # 音声合成を実行
            result = self.synthesizer.speak_text_async(text).get()

            # 結果の判定
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                print("✅ 音声合成が完了しました")
                return True, "音声合成が完了しました"

            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation = result.cancellation_details
                error_msg = f"❌ 音声合成がキャンセルされました: {cancellation.reason}"

                if cancellation.reason == speechsdk.CancellationReason.Error:
                    error_msg += f"\nエラー詳細: {cancellation.error_details}"

                print(error_msg)
                return False, error_msg

            else:
                error_msg = f"⚠️  予期しない結果: {result.reason}"
                print(error_msg)
                return False, error_msg

        except Exception as e:
            error_msg = f"❌ 音声合成エラー: {str(e)}"
            print(error_msg)
            return False, error_msg

    def speak_ssml(self, ssml: str) -> tuple[bool, str]:
        """
        SSMLを使用して音声合成（高度な制御）

        Args:
            ssml: SSML形式のテキスト

        Returns:
            (成功フラグ, メッセージ)のタプル
        """
        try:
            print("🔊 SSML音声合成中...")

            # SSML音声合成を実行
            result = self.synthesizer.speak_ssml_async(ssml).get()

            # 結果の判定
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                print("✅ SSML音声合成が完了しました")
                return True, "SSML音声合成が完了しました"

            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation = result.cancellation_details
                error_msg = f"❌ SSML音声合成がキャンセルされました: {cancellation.reason}"

                if cancellation.reason == speechsdk.CancellationReason.Error:
                    error_msg += f"\nエラー詳細: {cancellation.error_details}"

                print(error_msg)
                return False, error_msg

            else:
                error_msg = f"⚠️  予期しない結果: {result.reason}"
                print(error_msg)
                return False, error_msg

        except Exception as e:
            error_msg = f"❌ SSML音声合成エラー: {str(e)}"
            print(error_msg)
            return False, error_msg

    def set_voice(self, voice_name: str):
        """
        音声を変更

        Args:
            voice_name: 新しい音声名（例: ja-JP-KeitaNeural）
        """
        self.voice_name = voice_name
        self.speech_config.speech_synthesis_voice_name = voice_name
        print(f"🎙️  音声を変更しました: {voice_name}")

    def test_speaker(self) -> bool:
        """
        スピーカーの動作確認

        Returns:
            スピーカーが正常に動作している場合True
        """
        try:
            print("🔊 スピーカーのテスト中...")
            test_text = "こんにちは。音声合成のテストです。"

            result = self.synthesizer.speak_text_async(test_text).get()

            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                print("✅ スピーカーは正常に動作しています")
                return True
            else:
                print("❌ スピーカーの動作に問題があります")
                return False

        except Exception as e:
            print(f"❌ スピーカーテストエラー: {str(e)}")
            return False


def speak_text(text: str) -> bool:
    """
    テキストを音声で読み上げる簡易関数

    Args:
        text: 読み上げるテキスト

    Returns:
        成功時True
    """
    synthesizer = SpeechSynthesizer()
    success, _ = synthesizer.speak(text)
    return success


if __name__ == "__main__":
    """テスト実行"""
    print("=== Text-to-Speech テスト ===")

    synthesizer = SpeechSynthesizer()

    # テストメッセージ
    test_messages = [
        "こんにちは。Azure Speech Serviceのテストです。",
        "音声合成が正常に動作しています。",
        "ありがとうございました。",
    ]

    for i, message in enumerate(test_messages, 1):
        print(f"\n【テスト {i}/{len(test_messages)}】")
        success, result = synthesizer.speak(message)

        if not success:
            print(f"エラー: {result}")
            break

    print("\n=== テスト完了 ===")
