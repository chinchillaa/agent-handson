"""
高度な音声対話サンプル

Phase 3で実装した以下の機能を活用します：
- 会話要約
- コンテキスト管理
- 音声プロファイル変更
- エラーハンドリング強化
"""

import sys
import asyncio
from pathlib import Path

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from agents.voice_agent import create_voice_session
from tools.conversation_summarizer import ConversationSummarizer
from tools.context_manager import ContextManager
from config.voice_profiles import get_voice_profile, CUSTOM_PROFILES


async def advanced_chat():
    """高度な音声対話の例"""

    print("=" * 70)
    print("高度な音声対話サンプル（Phase 3機能デモ）")
    print("=" * 70)
    print()

    print("このサンプルでは、以下のPhase 3機能を体験できます:")
    print("  1. 会話要約（ConversationSummarizer）")
    print("  2. コンテキスト管理（ContextManager）")
    print("  3. 音声プロファイル変更")
    print("  4. エラーハンドリング強化（音声認識再試行）")
    print()

    # エージェントセッション作成
    print("【ステップ1】音声エージェントを作成中...")
    try:
        session = await create_voice_session(
            agent_name="AdvancedVoiceAssistant",
            deployment_name="gpt-5"
        )
        print("✅ エージェント作成完了")
    except Exception as e:
        print(f"❌ エージェント作成エラー: {str(e)}")
        return

    print()

    # ツールの初期化
    print("【ステップ2】支援ツールを初期化中...")
    summarizer = ConversationSummarizer()
    context_manager = ContextManager()
    print("✅ ツール初期化完了")

    print()

    # メニュー表示
    print("=" * 70)
    print("対話モードを選択してください:")
    print("  1. テキストのみ対話（音声なし、Phase 3機能デモ）")
    print("  2. フル機能対話（音声あり、実装予定）")
    print("=" * 70)
    print()

    choice = input("選択 (1/2): ").strip()

    if choice == "1":
        await text_only_demo(session, summarizer, context_manager)
    elif choice == "2":
        print("⚠️  フル機能対話モードは実装予定です。")
        print("    テキストのみ対話モードに切り替えます。")
        print()
        await text_only_demo(session, summarizer, context_manager)
    else:
        print("無効な選択です")


async def text_only_demo(session, summarizer, context_manager):
    """テキストのみのデモ（Phase 3機能を体験）"""

    print()
    print("=" * 70)
    print("テキストのみ対話モード（Phase 3機能デモ）")
    print("=" * 70)
    print()

    print("💡 使い方:")
    print("  - メッセージを入力してEnterキーを押してください")
    print("  - 'summary' と入力すると会話要約を表示します")
    print("  - 'context' と入力するとコンテキスト情報を表示します")
    print("  - 'stats' と入力すると統計情報を表示します")
    print("  - 'profile' と入力すると音声プロファイル一覧を表示します")
    print("  - 'exit' または 'quit' で終了します")
    print()

    turn_count = 0
    max_turns = 20

    while turn_count < max_turns:
        print(f"\n--- ターン {turn_count + 1}/{max_turns} ---")

        # ユーザー入力
        user_input = input("あなた: ").strip()

        if not user_input:
            print("⚠️  入力が空です。もう一度入力してください。")
            continue

        # 特殊コマンド処理
        if user_input.lower() in ["exit", "quit", "終了", "さようなら"]:
            print("\n👋 対話を終了します...")
            break

        elif user_input.lower() == "summary":
            # 会話要約
            print("\n【会話要約】")
            summary = summarizer.summarize_conversation(
                session.get_conversation_history()
            )
            print(summary)
            continue

        elif user_input.lower() == "context":
            # コンテキスト情報
            print("\n【コンテキスト情報】")
            print(context_manager.format_context_summary())
            continue

        elif user_input.lower() == "stats":
            # 統計情報
            print("\n【統計情報】")
            stats = summarizer.get_conversation_stats(
                session.get_conversation_history()
            )
            print(summarizer.format_stats(stats))
            continue

        elif user_input.lower() == "profile":
            # 音声プロファイル一覧
            print("\n【音声プロファイル一覧】")
            for key, profile in CUSTOM_PROFILES.items():
                print(f"  {key}: {profile.name}")
                print(f"    音声: {profile.voice_name}")
                print(f"    説明: {profile.description}")
            continue

        # 通常の対話
        try:
            # コンテキスト抽出（自動）
            context_manager.extract_from_conversation(
                session.get_conversation_history() + [
                    {"role": "user", "content": user_input}
                ]
            )

            # エージェントに送信
            print("🤔 応答を生成中...")
            response = await session.send_message(user_input)

            print(f"アシスタント: {response}")

            # 重要な情報をコンテキストに追加
            if "名前" in user_input:
                context_manager.add_context(
                    "mentioned_name_in_turn",
                    str(turn_count + 1),
                    importance="normal"
                )

            turn_count += 1

        except Exception as e:
            print(f"❌ エラー: {str(e)}")
            continue

    # 終了時の統計
    print()
    print("=" * 70)
    print("対話終了 - 最終レポート")
    print("=" * 70)

    # 会話要約
    print("\n【会話要約】")
    summary = summarizer.summarize_conversation(
        session.get_conversation_history()
    )
    print(summary)

    # コンテキスト情報
    print("\n【保存されたコンテキスト】")
    print(context_manager.format_context_summary())

    # 統計情報
    print("\n【統計情報】")
    stats = summarizer.get_conversation_stats(
        session.get_conversation_history()
    )
    print(summarizer.format_stats(stats))

    print()
    print("=" * 70)
    print("サンプル終了")
    print("=" * 70)


def main():
    """メイン実行"""
    print()
    try:
        asyncio.run(advanced_chat())
    except KeyboardInterrupt:
        print("\n\n終了しました")

    print()


if __name__ == "__main__":
    main()
