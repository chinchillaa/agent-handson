"""
高度な音声対話サンプル（Phase 3機能デモ）

このサンプルでは以下の機能をデモンストレーションします：
- 音声コマンド処理（要約、音声変更、話速調整）
- コンテキスト管理
- 会話要約
- 音声プロファイル切り替え
"""

import sys
import asyncio
from pathlib import Path

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from agents.voice_agent import create_voice_session
from voice_chat import VoiceChat
from config.settings import settings


def print_banner():
    """デモバナーを表示"""
    print()
    print("╔" + "=" * 68 + "╗")
    print("║  Azure 音声チャットボット - Phase 3 高度な機能デモ             ║")
    print("║  コンテキスト管理 | 会話要約 | 音声プロファイル動的切り替え     ║")
    print("╚" + "=" * 68 + "╝")
    print()


def print_available_commands():
    """利用可能な音声コマンドを表示"""
    print("【利用可能な音声コマンド】")
    print()
    print("  📝 会話要約:")
    print("     「要約して」「まとめて」「サマリーを見せて」")
    print()
    print("  🎙️  音声プロファイル変更:")
    print("     「音声を変更して」「声を変えて」")
    print()
    print("  ⏩ 話速調整:")
    print("     「速く話して」「早く話して」")
    print("     「ゆっくり話して」「遅く話して」")
    print()
    print("  🔄 設定リセット:")
    print("     「音声をリセット」「音声を初期化」")
    print()
    print("  🚪 終了:")
    print("     「終了」「さようなら」「バイバイ」")
    print()


def print_demo_scenario():
    """デモシナリオを表示"""
    print("【デモシナリオ例】")
    print()
    print("  1. 通常の質問をする")
    print("     例: 「こんにちは」「Pythonについて教えて」")
    print()
    print("  2. 音声コマンドを試す")
    print("     例: 「音声を変更して」→ 音声が変わります")
    print("     例: 「速く話して」→ 話速が速くなります")
    print()
    print("  3. 会話要約を確認")
    print("     例: 「要約して」→ これまでの会話を要約します")
    print()
    print("  4. 終了")
    print("     例: 「終了」")
    print()


async def demo_context_management(chat: VoiceChat):
    """
    コンテキスト管理のデモ

    Args:
        chat: VoiceChatインスタンス
    """
    print("\n" + "=" * 70)
    print("📊 コンテキスト管理デモ")
    print("=" * 70)

    # コンテキスト情報を表示
    context_summary = chat.context_manager.format_context_summary()
    print(context_summary)
    print()


async def demo_conversation_summary(chat: VoiceChat):
    """
    会話要約のデモ

    Args:
        chat: VoiceChatインスタンス
    """
    print("\n" + "=" * 70)
    print("📝 会話要約デモ")
    print("=" * 70)

    history = chat.session.get_conversation_history()
    if history:
        # 要約を生成
        summary = chat.summarizer.summarize_conversation(history)
        print(summary)

        # 統計情報を表示
        print()
        stats = chat.summarizer.get_conversation_stats(history)
        print(chat.summarizer.format_stats(stats))
    else:
        print("会話履歴がまだありません。")

    print()


async def demo_voice_profiles(chat: VoiceChat):
    """
    音声プロファイルのデモ

    Args:
        chat: VoiceChatインスタンス
    """
    print("\n" + "=" * 70)
    print("🎙️  音声プロファイル設定")
    print("=" * 70)

    print(f"現在の音声プロファイル: {chat.current_voice_profile}")
    print(f"現在の話速: {chat.current_speaking_rate}x")
    print()


async def main():
    """メイン処理"""
    # バナー表示
    print_banner()

    # 環境チェック（簡易版）
    if not settings.AZURE_SPEECH_API_KEY or not settings.AZURE_OPENAI_ENDPOINT:
        print("❌ エラー: 環境変数が設定されていません")
        print("   .envファイルを確認してください")
        sys.exit(1)

    # 利用可能なコマンドを表示
    print_available_commands()

    # デモシナリオを表示
    print_demo_scenario()

    # 開始確認
    print("高度な音声対話デモを開始しますか？ [Y/n]: ", end="")
    response = input().strip().lower()

    if response and response not in ["y", "yes", ""]:
        print("キャンセルしました")
        sys.exit(0)

    print()
    print("=" * 70)
    print("🚀 音声チャットボット（Phase 3機能付き）を起動しています...")
    print("=" * 70)
    print()

    try:
        # エージェントセッション作成
        print("🤖 GPT-5エージェントを初期化中...")
        session = await create_voice_session(
            agent_name="AdvancedVoiceAssistant",
            deployment_name=settings.AZURE_OPENAI_DEPLOYMENT_GPT5
        )

        print("✅ エージェント初期化完了")
        print()

        # VoiceChatインスタンス作成（Phase 3機能有効）
        chat = VoiceChat(session)

        # 初期状態を表示
        await demo_voice_profiles(chat)

        print("💡 ヒント: 上記の音声コマンドを使って機能を試してみてください")
        print()

        # 音声対話開始
        await chat.start_conversation()

        # 終了時にデモを表示
        print("\n" + "=" * 70)
        print("📊 セッション終了後の情報")
        print("=" * 70)

        # コンテキスト管理デモ
        await demo_context_management(chat)

        # 会話要約デモ
        await demo_conversation_summary(chat)

    except KeyboardInterrupt:
        print("\n\n⏹  ユーザーによって中断されました")
        print("👋 デモを終了します")

    except Exception as e:
        print()
        print("=" * 70)
        print("❌ エラーが発生しました")
        print("=" * 70)
        print(f"エラー詳細: {str(e)}")
        print()
        print("🔍 トラブルシューティング:")
        print("  1. .envファイルの設定を確認してください")
        print("  2. Azure OpenAIサービスが利用可能か確認してください")
        print("  3. Azure Speech Serviceが利用可能か確認してください")
        print("  4. マイクとスピーカーが正常に動作しているか確認してください")
        print()
        sys.exit(1)

    print()
    print("=" * 70)
    print("👋 高度な音声対話デモを終了しました")
    print("=" * 70)
    print()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n終了しました")
        sys.exit(0)
