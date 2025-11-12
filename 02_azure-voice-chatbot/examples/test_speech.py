"""
音声入出力テストスクリプト

Azure Speech Serviceの動作確認を行います。
- Speech-to-Text（音声認識）
- Text-to-Speech（音声合成）
"""

import sys
from pathlib import Path

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from speech.recognizer import SpeechRecognizer
from speech.synthesizer import SpeechSynthesizer


def test_speech_to_text():
    """音声認識のテスト"""
    print("=" * 60)
    print("🎤 Speech-to-Text（音声認識）テスト")
    print("=" * 60)
    print()

    try:
        recognizer = SpeechRecognizer()

        # マイクテスト
        print("【ステップ1】マイクの動作確認")
        if not recognizer.test_microphone():
            print("❌ マイクが正常に動作していません")
            return False

        print()
        print("【ステップ2】音声認識テスト")
        print("何か話してください...")
        print()

        success, text = recognizer.recognize_once()

        if success:
            print()
            print(f"✅ 認識成功: {text}")
            return True
        else:
            print()
            print(f"❌ 認識失敗: {text}")
            return False

    except Exception as e:
        print(f"❌ エラー: {str(e)}")
        return False


def test_text_to_speech():
    """音声合成のテスト"""
    print("=" * 60)
    print("🔊 Text-to-Speech（音声合成）テスト")
    print("=" * 60)
    print()

    try:
        synthesizer = SpeechSynthesizer()

        # スピーカーテスト
        print("【ステップ1】スピーカーの動作確認")
        if not synthesizer.test_speaker():
            print("❌ スピーカーが正常に動作していません")
            return False

        print()
        print("【ステップ2】音声合成テスト")

        test_messages = [
            "こんにちは。",
            "Azure Speech Serviceの音声合成テストです。",
            "正常に動作しています。",
        ]

        for i, message in enumerate(test_messages, 1):
            print(f"\nメッセージ {i}/{len(test_messages)}: {message}")
            success, result = synthesizer.speak(message)

            if not success:
                print(f"❌ 音声合成失敗: {result}")
                return False

        print()
        print("✅ すべての音声合成テストが成功しました")
        return True

    except Exception as e:
        print(f"❌ エラー: {str(e)}")
        return False


def test_round_trip():
    """音声認識→音声合成のラウンドトリップテスト"""
    print("=" * 60)
    print("🔄 ラウンドトリップテスト（音声認識→音声合成）")
    print("=" * 60)
    print()

    try:
        recognizer = SpeechRecognizer()
        synthesizer = SpeechSynthesizer()

        print("何か話してください。認識後、その内容を音声で返します...")
        print()

        # 音声認識
        success, text = recognizer.recognize_once()

        if not success:
            print(f"❌ 音声認識失敗: {text}")
            return False

        print()
        print(f"認識結果: {text}")
        print()

        # 認識結果を音声合成
        response_text = f"あなたは「{text}」と言いましたね。"
        print(f"応答: {response_text}")

        success, result = synthesizer.speak(response_text)

        if success:
            print("✅ ラウンドトリップテスト成功")
            return True
        else:
            print(f"❌ 音声合成失敗: {result}")
            return False

    except Exception as e:
        print(f"❌ エラー: {str(e)}")
        return False


def main():
    """メイン実行"""
    print()
    print("╔" + "=" * 58 + "╗")
    print("║  Azure Speech Service 動作確認テスト                     ║")
    print("╚" + "=" * 58 + "╝")
    print()

    # テストメニュー
    print("実行するテストを選択してください:")
    print("  1. Speech-to-Text（音声認識）テスト")
    print("  2. Text-to-Speech（音声合成）テスト")
    print("  3. ラウンドトリップテスト（認識→合成）")
    print("  4. すべてのテストを実行")
    print()

    choice = input("選択 (1-4): ").strip()

    print()

    if choice == "1":
        test_speech_to_text()
    elif choice == "2":
        test_text_to_speech()
    elif choice == "3":
        test_round_trip()
    elif choice == "4":
        # すべてのテストを実行
        results = []

        print()
        results.append(("音声認識", test_speech_to_text()))

        print("\n")
        results.append(("音声合成", test_text_to_speech()))

        print("\n")
        results.append(("ラウンドトリップ", test_round_trip()))

        # 結果サマリー
        print()
        print("=" * 60)
        print("テスト結果サマリー")
        print("=" * 60)
        for test_name, result in results:
            status = "✅ 成功" if result else "❌ 失敗"
            print(f"  {test_name}: {status}")
        print("=" * 60)
    else:
        print("無効な選択です")

    print()


if __name__ == "__main__":
    main()
