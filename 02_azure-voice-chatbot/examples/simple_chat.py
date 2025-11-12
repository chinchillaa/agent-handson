"""
シンプル音声対話サンプル

最小限のコードで音声対話を実行する例です。
"""

import sys
import asyncio
from pathlib import Path

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from agents.voice_agent import create_voice_session
from voice_chat import start_voice_chat


async def simple_chat():
    """シンプルな音声対話の例"""

    print("=" * 60)
    print("シンプル音声対話サンプル")
    print("=" * 60)
    print()

    print("このサンプルでは、以下の流れで音声対話を体験できます:")
    print("  1. 音声エージェントの作成")
    print("  2. 音声認識による入力")
    print("  3. GPT-5による応答生成")
    print("  4. 音声合成による出力")
    print()

    # ステップ1: エージェントセッション作成
    print("【ステップ1】音声エージェントを作成中...")
    try:
        session = await create_voice_session(
            agent_name="SimpleVoiceAssistant",
            deployment_name="gpt-5"  # GPT-5を使用
        )
        print("✅ エージェント作成完了")
    except Exception as e:
        print(f"❌ エージェント作成エラー: {str(e)}")
        print()
        print("トラブルシューティング:")
        print("  - .envファイルが正しく設定されているか確認してください")
        print("  - AZURE_OPENAI_ENDPOINTが設定されているか確認してください")
        return

    print()

    # ステップ2: 音声対話開始
    print("【ステップ2】音声対話を開始します")
    print()
    print("💡 ヒント:")
    print("  - マイクに向かって話しかけてください")
    print("  - 「終了」または「さようなら」と言うと終了します")
    print("  - Ctrl+C でも終了できます")
    print()

    input("準備ができたらEnterキーを押してください...")
    print()

    # 音声対話を開始
    try:
        await start_voice_chat(session)
    except KeyboardInterrupt:
        print("\n\n⏹  ユーザーによって中断されました")
    except Exception as e:
        print(f"\n❌ エラー: {str(e)}")

    print()
    print("=" * 60)
    print("サンプル終了")
    print("=" * 60)


async def quick_test():
    """
    クイックテスト（テキストのみ）

    音声機能を使わず、エージェントの動作確認のみ行います。
    """
    print("=" * 60)
    print("クイックテスト（テキストのみ）")
    print("=" * 60)
    print()

    print("音声機能を使わず、エージェントの応答をテストします")
    print()

    try:
        # エージェント作成
        print("エージェントを作成中...")
        session = await create_voice_session(
            agent_name="TestAgent",
            deployment_name="gpt-5"
        )
        print("✅ エージェント作成完了\n")

        # テストメッセージ
        test_message = "こんにちは。簡単に自己紹介をしてください。"

        print(f"ユーザー: {test_message}")
        print("応答を生成中...\n")

        response = await session.send_message(test_message)

        print(f"アシスタント: {response}")
        print()

        print("✅ テスト成功")

    except Exception as e:
        print(f"❌ テスト失敗: {str(e)}")

    print()


def main():
    """メイン実行"""
    print()
    print("実行モードを選択してください:")
    print("  1. シンプル音声対話（音声入出力あり）")
    print("  2. クイックテスト（テキストのみ、音声なし）")
    print()

    choice = input("選択 (1/2): ").strip()

    print()

    if choice == "1":
        # 音声対話モード
        try:
            asyncio.run(simple_chat())
        except KeyboardInterrupt:
            print("\n\n終了しました")
    elif choice == "2":
        # テストモード
        try:
            asyncio.run(quick_test())
        except KeyboardInterrupt:
            print("\n\n終了しました")
    else:
        print("無効な選択です")

    print()


if __name__ == "__main__":
    main()
