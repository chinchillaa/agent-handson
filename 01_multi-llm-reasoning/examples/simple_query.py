"""
Simple Query Example - シンプルな質問の実行例

基本的な使い方を示すサンプルスクリプト
"""

import asyncio
import sys
from pathlib import Path

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from workflow import run_multi_agent_workflow


async def main():
    """メイン関数"""
    print("=" * 80)
    print("Multi-Agent Reasoning System - Simple Query Example")
    print("=" * 80)
    print()

    # シンプルな質問
    query = "人工知能（AI）の歴史について簡潔に教えてください"

    print(f"質問: {query}\n")
    print("エージェントワークフローを実行中...\n")

    try:
        # ワークフロー実行
        result = await run_multi_agent_workflow(query)

        # 結果表示
        print("\n" + "=" * 80)
        print("最終回答:")
        print("=" * 80)
        print(result['final_answer'])
        print("\n" + "=" * 80)
        print(f"実行時間: {result['execution_time']:.2f}秒")
        print("=" * 80)

    except Exception as e:
        print(f"\nエラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    # 非同期実行
    asyncio.run(main())
