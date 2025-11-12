"""
Azure音声チャットボット - メインエントリーポイント

GPT-5とAzure Speech Serviceを使用した音声対話システムです。
"""

import sys
import asyncio
from pathlib import Path

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from agents.voice_agent import create_voice_session
from voice_chat import start_voice_chat
from config.settings import settings


def print_banner():
    """起動バナーを表示"""
    print()
    print("╔" + "=" * 58 + "╗")
    print("║  Azure 音声チャットボット                               ║")
    print("║  Powered by GPT-5 & Azure Speech Service                ║")
    print("╚" + "=" * 58 + "╝")
    print()


def check_environment():
    """
    環境変数のチェック

    Returns:
        環境が正しく設定されている場合True
    """
    print("【環境チェック】")

    # 必須環境変数
    required_vars = {
        "AZURE_OPENAI_ENDPOINT": settings.AZURE_OPENAI_ENDPOINT,
        "AZURE_SPEECH_API_KEY": settings.AZURE_SPEECH_API_KEY,
        "AZURE_SPEECH_REGION": settings.AZURE_SPEECH_REGION,
    }

    missing_vars = []
    for var_name, var_value in required_vars.items():
        if not var_value:
            missing_vars.append(var_name)
            print(f"  ❌ {var_name}: 未設定")
        else:
            # 機密情報は一部のみ表示
            if "KEY" in var_name or "API" in var_name:
                masked = var_value[:8] + "..." if len(var_value) > 8 else "***"
                print(f"  ✅ {var_name}: {masked}")
            else:
                print(f"  ✅ {var_name}: {var_value}")

    # オプション環境変数
    print()
    print("【オプション設定】")
    print(f"  Azure OpenAI認証: {'APIキー' if settings.AZURE_OPENAI_API_KEY else 'Azure CLI'}")
    print(f"  デプロイメント名: {settings.AZURE_OPENAI_DEPLOYMENT_NAME}")
    print(f"  音声言語: {settings.AZURE_SPEECH_LANGUAGE}")
    print(f"  音声名: {settings.AZURE_SPEECH_VOICE_NAME}")
    print()

    if missing_vars:
        print()
        print("⚠️  必須環境変数が設定されていません:")
        for var in missing_vars:
            print(f"    - {var}")
        print()
        print("📝 .envファイルを確認してください")
        print("   詳細はREADME.mdを参照してください")
        return False

    return True


def print_usage_guide():
    """使用方法ガイドを表示"""
    print("【使い方】")
    print("  1. マイクに向かって話しかけてください")
    print("  2. 音声が自動的にテキストに変換されます")
    print("  3. GPT-5が応答を生成します")
    print("  4. 応答が音声で読み上げられます")
    print()
    print("【終了方法】")
    print("  - 「終了」「さようなら」などと話しかける")
    print("  - Ctrl+C を押す")
    print()
    print("【安全機能】")
    print(f"  - 最大ターン数: {settings.MAX_CONVERSATION_TURNS}")
    print(f"  - 最大セッション時間: {settings.MAX_SESSION_DURATION // 60}分")
    print(f"  - 連続エラー制限: {settings.MAX_CONSECUTIVE_ERRORS}回")
    print()


async def main():
    """メイン処理"""
    # バナー表示
    print_banner()

    # 環境チェック
    if not check_environment():
        sys.exit(1)

    # 使い方ガイド
    print_usage_guide()

    # 開始確認
    print("音声チャットボットを起動しますか？ [Y/n]: ", end="")
    response = input().strip().lower()

    if response and response not in ["y", "yes", ""]:
        print("キャンセルしました")
        sys.exit(0)

    print()
    print("=" * 60)
    print("🚀 音声チャットボットを起動しています...")
    print("=" * 60)
    print()

    try:
        # エージェントセッション作成
        print("🤖 GPT-5エージェントを初期化中...")
        session = await create_voice_session(
            agent_name=settings.VOICE_AGENT_NAME,
            deployment_name=settings.AZURE_OPENAI_DEPLOYMENT_NAME
        )

        print("✅ エージェント初期化完了")
        print()

        # 音声対話開始
        await start_voice_chat(session)

    except KeyboardInterrupt:
        print("\n\n⏹  ユーザーによって中断されました")
        print("👋 ご利用ありがとうございました")

    except Exception as e:
        print()
        print("=" * 60)
        print("❌ エラーが発生しました")
        print("=" * 60)
        print(f"エラー詳細: {str(e)}")
        print()
        print("🔍 トラブルシューティング:")
        print("  1. .envファイルの設定を確認してください")
        print("  2. Azure OpenAIサービスが利用可能か確認してください")
        print("  3. Azure Speech Serviceが利用可能か確認してください")
        print("  4. マイクとスピーカーが正常に動作しているか確認してください")
        print()
        print("詳細はREADME.mdを参照してください")
        sys.exit(1)

    print()
    print("=" * 60)
    print("👋 音声チャットボットを終了しました")
    print("=" * 60)
    print()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n終了しました")
        sys.exit(0)
