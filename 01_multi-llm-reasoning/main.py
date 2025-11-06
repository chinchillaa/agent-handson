"""
Multi-Agent Reasoning System - メインエントリーポイント

複数のLLMエージェントを使った推論システムのコマンドラインインターフェース
"""

import asyncio
import argparse
import sys
import os
from pathlib import Path
from datetime import datetime
from typing import Optional

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from workflow import run_multi_agent_workflow
from config.settings import settings


def print_banner():
    """バナーを表示"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     Multi-Agent Reasoning System                            ║
║     マルチエージェント推論システム                          ║
║                                                              ║
║     Powered by Microsoft Agent Framework & Azure OpenAI     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
    print(banner)


def print_section_header(title: str, char: str = "="):
    """セクションヘッダーを表示"""
    print(f"\n{char * 80}")
    print(f"{title:^80}")
    print(f"{char * 80}\n")


def print_agent_output(agent_name: str, output: str, verbose: bool = False):
    """エージェントの出力を表示"""
    if not verbose:
        return

    print_section_header(f"📋 {agent_name} の出力", "-")
    print(output)
    print()


def save_results_to_file(result: dict, output_dir: Path):
    """
    実行結果をファイルに保存

    Args:
        result: ワークフローの実行結果
        output_dir: 出力ディレクトリ
    """
    # 出力ディレクトリ作成
    output_dir.mkdir(parents=True, exist_ok=True)

    # タイムスタンプでファイル名を生成
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"result_{timestamp}.md"

    # Markdown形式で保存
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# Multi-Agent Reasoning System - 実行結果\n\n")
        f.write(f"**実行日時**: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}\n\n")
        f.write(f"**実行時間**: {result['execution_time']:.2f}秒\n\n")

        f.write("---\n\n")

        # 最終回答
        f.write("## 最終回答\n\n")
        f.write(result['final_answer'])
        f.write("\n\n---\n\n")

        # 各エージェントの出力
        f.write("## 各エージェントの詳細出力\n\n")

        agent_names = {
            "coordinator": "🎯 Coordinator（調査計画）",
            "researcher": "🔍 Researcher（情報収集）",
            "analyzer": "📊 Analyzer（データ分析）",
            "summarizer": "📝 Summarizer（最終統合）"
        }

        for key, name in agent_names.items():
            f.write(f"### {name}\n\n")
            f.write(result['agent_outputs'][key])
            f.write("\n\n")

    print(f"\n💾 結果をファイルに保存しました: {output_file}")


async def main():
    """メイン関数"""
    # コマンドライン引数のパース
    parser = argparse.ArgumentParser(
        description="Multi-Agent Reasoning System - マルチエージェント推論システム",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # 基本的な使用方法
  python main.py "量子コンピューターについて教えてください"

  # 各エージェントの出力も表示
  python main.py "量子コンピューターについて教えてください" --verbose

  # 結果をファイルに保存
  python main.py "量子コンピューターについて教えてください" --save-output
        """
    )

    parser.add_argument(
        "query",
        type=str,
        nargs="?",
        help="質問内容（省略時はインタラクティブモード）"
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="各エージェントの詳細な出力を表示"
    )

    parser.add_argument(
        "-s", "--save-output",
        action="store_true",
        help="結果をファイルに保存（output/ディレクトリ）"
    )

    parser.add_argument(
        "-o", "--output-dir",
        type=str,
        default="output",
        help="出力ディレクトリ（デフォルト: output/）"
    )

    parser.add_argument(
        "--no-banner",
        action="store_true",
        help="バナー表示を省略"
    )

    args = parser.parse_args()

    # バナー表示
    if not args.no_banner:
        print_banner()

    # 質問の取得
    query = args.query
    if not query:
        # インタラクティブモード
        print("質問を入力してください（終了するにはCtrl+Cを押してください）:")
        try:
            query = input("> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n👋 終了します")
            return

    if not query:
        print("❌ 質問が空です")
        return

    # 環境変数チェック
    required_env_vars = ["AZURE_OPENAI_ENDPOINT"]
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]

    if missing_vars:
        print(f"❌ エラー: 以下の環境変数が設定されていません:")
        for var in missing_vars:
            print(f"  - {var}")
        print("\n.envファイルを確認してください")
        return

    # 質問表示
    print_section_header("📝 質問")
    print(query)

    try:
        # ワークフロー実行
        print("\n🚀 マルチエージェントワークフローを開始します...\n")

        result = await run_multi_agent_workflow(query)

        # 各エージェントの出力表示（verbose モード）
        if args.verbose:
            print("\n" + "=" * 80)
            print("各エージェントの詳細出力")
            print("=" * 80)

            print_agent_output("Coordinator", result['agent_outputs']['coordinator'], True)
            print_agent_output("Researcher", result['agent_outputs']['researcher'], True)
            print_agent_output("Analyzer", result['agent_outputs']['analyzer'], True)
            print_agent_output("Summarizer", result['agent_outputs']['summarizer'], True)

        # 最終回答表示
        print_section_header("✨ 最終回答")
        print(result['final_answer'])

        # 実行時間表示
        print(f"\n⏱️  実行時間: {result['execution_time']:.2f}秒")

        # ファイル保存
        if args.save_output:
            output_dir = Path(args.output_dir)
            save_results_to_file(result, output_dir)

        print("\n✅ 処理が完了しました\n")

    except KeyboardInterrupt:
        print("\n\n⚠️  処理が中断されました")
        sys.exit(1)

    except Exception as e:
        print(f"\n❌ エラーが発生しました: {e}")
        import traceback
        if args.verbose:
            print("\n詳細なエラー情報:")
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    # 非同期実行
    asyncio.run(main())
