"""
Complex Reasoning Example - 複雑な推論の実行例

複数の観点からの分析が必要な質問の実行例
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
    print("Multi-Agent Reasoning System - Complex Reasoning Example")
    print("=" * 80)
    print()

    # 複雑な推論が必要な質問
    queries = [
        {
            "title": "例1: 技術トレンド分析",
            "query": """
量子コンピューターと従来のコンピューターの違いを説明し、
量子コンピューターが実用化された場合の社会への影響を
技術的・経済的・セキュリティの観点から分析してください。
            """.strip()
        },
        {
            "title": "例2: 多角的分析",
            "query": """
再生可能エネルギーへの移行について、以下の観点から分析してください：
1. 環境面でのメリット・デメリット
2. 経済的な実現可能性
3. 技術的な課題
4. 政策的な取り組みの現状
            """.strip()
        }
    ]

    # 最初の例を実行（変更可能）
    selected_example = queries[0]

    print(f"【{selected_example['title']}】\n")
    print(f"質問:\n{selected_example['query']}\n")
    print("=" * 80)
    print("エージェントワークフローを実行中...")
    print("複雑な推論のため、通常より時間がかかる場合があります。")
    print("=" * 80)
    print()

    try:
        # ワークフロー実行
        result = await run_multi_agent_workflow(selected_example['query'])

        # 結果表示
        print("\n" + "=" * 80)
        print("最終回答:")
        print("=" * 80)
        print(result['final_answer'])

        # 各エージェントの出力を表示（オプション）
        print("\n\n" + "=" * 80)
        print("各エージェントの詳細出力:")
        print("=" * 80)

        print("\n" + "-" * 80)
        print("🎯 Coordinator（調査計画）")
        print("-" * 80)
        print(result['agent_outputs']['coordinator'][:500] + "...\n")

        print("-" * 80)
        print("🔍 Researcher（情報収集）")
        print("-" * 80)
        print(result['agent_outputs']['researcher'][:500] + "...\n")

        print("-" * 80)
        print("📊 Analyzer（データ分析）")
        print("-" * 80)
        print(result['agent_outputs']['analyzer'][:500] + "...\n")

        print("\n" + "=" * 80)
        print(f"実行時間: {result['execution_time']:.2f}秒")
        print("=" * 80)

        # 他の例を試す場合の案内
        print("\n💡 ヒント:")
        print(f"   - このファイルの queries リストには {len(queries)} 個の例があります")
        print("   - selected_example を変更して他の例を試すことができます")

    except Exception as e:
        print(f"\nエラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    # 非同期実行
    asyncio.run(main())
