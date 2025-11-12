"""
音声対話ループ

Speech-to-Text、エージェント、Text-to-Speechを統合した音声対話システムです。
無限ループ防止のための安全機構を実装しています。
"""

import time
from typing import Optional
from speech.recognizer import SpeechRecognizer
from speech.synthesizer import SpeechSynthesizer
from agents.voice_agent import VoiceAgentSession
from config.settings import settings


class VoiceChat:
    """
    音声対話管理クラス

    音声認識、エージェント応答、音声合成を統合し、
    安全な対話ループを提供します。
    """

    def __init__(
        self,
        session: VoiceAgentSession,
        recognizer: Optional[SpeechRecognizer] = None,
        synthesizer: Optional[SpeechSynthesizer] = None
    ):
        """
        音声対話の初期化

        Args:
            session: 音声エージェントセッション
            recognizer: 音声認識器（省略時は新規作成）
            synthesizer: 音声合成器（省略時は新規作成）
        """
        self.session = session
        self.recognizer = recognizer or SpeechRecognizer()
        self.synthesizer = synthesizer or SpeechSynthesizer()

        # 安全カウンター
        self.turn_count = 0
        self.consecutive_errors = 0
        self.session_start_time = None

    def _check_safety_limits(self) -> tuple[bool, Optional[str]]:
        """
        安全制限のチェック

        Returns:
            (継続可能フラグ, 停止理由)のタプル
            継続可能な場合: (True, None)
            停止すべき場合: (False, "理由メッセージ")
        """
        # ターン数制限
        if self.turn_count >= settings.MAX_CONVERSATION_TURNS:
            return False, f"最大ターン数（{settings.MAX_CONVERSATION_TURNS}）に到達しました"

        # 連続エラー制限
        if self.consecutive_errors >= settings.MAX_CONSECUTIVE_ERRORS:
            return False, f"連続エラーが{settings.MAX_CONSECUTIVE_ERRORS}回発生しました"

        # セッション時間制限
        if self.session_start_time:
            elapsed = time.time() - self.session_start_time
            if elapsed > settings.MAX_SESSION_DURATION:
                minutes = settings.MAX_SESSION_DURATION / 60
                return False, f"最大セッション時間（{minutes}分）を超過しました"

        return True, None

    def _is_exit_command(self, text: str) -> bool:
        """
        終了コマンドかどうかを判定

        Args:
            text: ユーザー入力テキスト

        Returns:
            終了コマンドの場合True
        """
        return settings.is_exit_keyword(text)

    async def start_conversation(self):
        """
        音声対話を開始

        無限ループ防止の安全機構を実装した対話ループを実行します。
        """
        print("\n" + "=" * 60)
        print("🎙️  音声対話システム起動")
        print("=" * 60)
        print()

        # 安全設定の表示
        print("【安全設定】")
        print(f"  最大ターン数: {settings.MAX_CONVERSATION_TURNS}")
        print(f"  最大連続エラー: {settings.MAX_CONSECUTIVE_ERRORS}")
        print(f"  最大セッション時間: {settings.MAX_SESSION_DURATION // 60}分")
        print(f"  終了キーワード: {', '.join(settings.EXIT_KEYWORDS)}")
        print()

        # 開始メッセージ
        welcome_message = "こんにちは。音声アシスタントです。何かお手伝いできることはありますか？"
        print(f"🤖 アシスタント: {welcome_message}")
        success, _ = self.synthesizer.speak(welcome_message)

        if not success:
            print("⚠️  音声合成に失敗しました。テキストのみで継続します。")

        # セッション開始時刻を記録
        self.session_start_time = time.time()

        # 対話ループ
        while True:
            # 安全制限チェック
            can_continue, stop_reason = self._check_safety_limits()
            if not can_continue:
                print(f"\n⏹  対話を終了します: {stop_reason}")
                break

            print()
            print(f"--- ターン {self.turn_count + 1}/{settings.MAX_CONVERSATION_TURNS} ---")

            try:
                # 1. 音声認識（Phase 3: 再試行機能追加）
                user_text = None
                max_retries = 3  # 最大再試行回数
                recognition_success = False

                for retry in range(max_retries):
                    if retry > 0:
                        print(f"🔄 再試行中... ({retry}/{max_retries - 1})")

                    print("🎤 音声入力を待機中...")
                    success, user_text = self.recognizer.recognize_once()

                    if success:
                        # エラーカウンターリセット
                        self.consecutive_errors = 0
                        recognition_success = True
                        break
                    else:
                        print(f"❌ 音声認識エラー: {user_text}")

                        if retry < max_retries - 1:
                            print("💬 もう一度話しかけてください...")

                # 全ての再試行が失敗した場合
                if not recognition_success:
                    print("⚠️  音声認識に失敗しました。次のターンに進みます。")
                    self.consecutive_errors += 1
                    continue

                print(f"📝 認識結果: {user_text}")

                # 終了コマンドチェック
                if self._is_exit_command(user_text):
                    print("\n👋 終了コマンドを検出しました")
                    farewell_message = "ご利用ありがとうございました。さようなら。"
                    print(f"🤖 アシスタント: {farewell_message}")
                    self.synthesizer.speak(farewell_message)
                    break

                # 2. エージェント処理
                print("🤔 応答を生成中...")
                assistant_response = await self.session.send_message(user_text)
                print(f"🤖 アシスタント: {assistant_response}")

                # 3. 音声合成
                success, result = self.synthesizer.speak(assistant_response)

                if not success:
                    print(f"⚠️  音声合成エラー: {result}")
                    print("テキストのみで継続します")

                # ターン数をインクリメント
                self.turn_count += 1

            except KeyboardInterrupt:
                print("\n\n⏹  ユーザーによって中断されました")
                break

            except Exception as e:
                print(f"\n❌ 予期しないエラー: {str(e)}")
                self.consecutive_errors += 1

                # エラーが多すぎる場合は終了
                if self.consecutive_errors >= settings.MAX_CONSECUTIVE_ERRORS:
                    print(f"⚠️  連続エラーが{settings.MAX_CONSECUTIVE_ERRORS}回発生したため終了します")
                    break

        # 終了時の統計情報
        self._print_session_statistics()

    def _print_session_statistics(self):
        """セッション統計情報を表示"""
        print()
        print("=" * 60)
        print("📊 セッション統計")
        print("=" * 60)
        print(f"  総ターン数: {self.turn_count}")

        if self.session_start_time:
            elapsed = time.time() - self.session_start_time
            minutes = int(elapsed // 60)
            seconds = int(elapsed % 60)
            print(f"  セッション時間: {minutes}分{seconds}秒")

        print(f"  会話履歴: {len(self.session.get_conversation_history())}メッセージ")
        print("=" * 60)
        print()


async def start_voice_chat(session: VoiceAgentSession):
    """
    音声対話を開始する簡易ヘルパー関数

    Args:
        session: 音声エージェントセッション
    """
    chat = VoiceChat(session)
    await chat.start_conversation()


if __name__ == "__main__":
    """テスト実行"""
    import asyncio
    from agents.voice_agent import create_voice_session

    async def test_voice_chat():
        print("=== 音声対話システム テスト ===\n")

        # セッション作成
        print("セッションを作成中...")
        session = await create_voice_session(
            agent_name="TestVoiceAssistant",
            deployment_name="gpt-5"
        )

        print("✅ セッション作成完了\n")

        # 音声対話開始
        await start_voice_chat(session)

    # 非同期テスト実行
    try:
        asyncio.run(test_voice_chat())
    except KeyboardInterrupt:
        print("\n\nテストを終了しました")
