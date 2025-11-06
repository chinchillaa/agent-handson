"""
Multi-Agent Workflow - マルチエージェントワークフロー

4つのエージェント（Coordinator、Researcher、Analyzer、Summarizer）を順次実行し、
複雑な推論タスクを協調的に処理します。
"""

import asyncio
import logging
from typing import Dict, Any, List
from datetime import datetime

from .agents import (
    create_coordinator_agent,
    create_researcher_agent,
    create_analyzer_agent,
    create_summarizer_agent
)

# ロガー設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MultiAgentWorkflow:
    """
    マルチエージェントワークフローの管理クラス

    4つのエージェントを順次実行し、各エージェントの出力を
    次のエージェントに引き継ぎます。
    """

    def __init__(self):
        """ワークフロー初期化"""
        self.coordinator = None
        self.researcher = None
        self.analyzer = None
        self.summarizer = None
        self.execution_history: List[Dict[str, Any]] = []

    async def initialize_agents(self):
        """
        全エージェントを初期化

        並列で全エージェントを作成し、起動時間を短縮します。
        """
        logger.info("エージェントを初期化中...")

        try:
            # 並列でエージェントを作成
            coordinator_task = create_coordinator_agent()
            researcher_task = create_researcher_agent()
            analyzer_task = create_analyzer_agent()
            summarizer_task = create_summarizer_agent()

            # 全エージェントの作成を待機
            self.coordinator, self.researcher, self.analyzer, self.summarizer = await asyncio.gather(
                coordinator_task,
                researcher_task,
                analyzer_task,
                summarizer_task
            )

            logger.info("✅ 全エージェントの初期化が完了しました")

        except Exception as e:
            logger.error(f"❌ エージェント初期化エラー: {e}")
            raise

    async def run_coordinator(self, user_query: str) -> str:
        """
        Coordinatorエージェントを実行

        Args:
            user_query: ユーザーからの質問

        Returns:
            Coordinatorの出力（調査計画）
        """
        logger.info("=" * 80)
        logger.info("🎯 Phase 1: Coordinator - 調査計画の立案")
        logger.info("=" * 80)

        try:
            # Coordinatorに質問を送信
            response = await self.coordinator.run(user_query)

            # 実行履歴に記録
            self.execution_history.append({
                "agent": "Coordinator",
                "timestamp": datetime.now().isoformat(),
                "input": user_query,
                "output": response.content
            })

            logger.info(f"✅ Coordinator完了: {len(response.content)}文字の計画を生成")
            return response.content

        except Exception as e:
            logger.error(f"❌ Coordinatorエラー: {e}")
            raise

    async def run_researcher(self, coordinator_output: str, original_query: str) -> str:
        """
        Researcherエージェントを実行

        Args:
            coordinator_output: Coordinatorの出力
            original_query: 元のユーザークエリ

        Returns:
            Researcherの出力（収集した情報）
        """
        logger.info("=" * 80)
        logger.info("🔍 Phase 2: Researcher - 情報収集")
        logger.info("=" * 80)

        try:
            # Researcherへの指示を作成
            researcher_prompt = f"""
【元の質問】
{original_query}

【Coordinatorからの調査指示】
{coordinator_output}

上記の調査指示に基づいて、必要な情報を収集してください。
Web検索ツールを活用し、最新の情報を含めてください。
"""

            # Researcherに送信
            response = await self.researcher.run(researcher_prompt)

            # 実行履歴に記録
            self.execution_history.append({
                "agent": "Researcher",
                "timestamp": datetime.now().isoformat(),
                "input": researcher_prompt,
                "output": response.content
            })

            logger.info(f"✅ Researcher完了: {len(response.content)}文字の情報を収集")
            return response.content

        except Exception as e:
            logger.error(f"❌ Researcherエラー: {e}")
            raise

    async def run_analyzer(self, researcher_output: str, coordinator_output: str, original_query: str) -> str:
        """
        Analyzerエージェントを実行

        Args:
            researcher_output: Researcherの出力
            coordinator_output: Coordinatorの出力
            original_query: 元のユーザークエリ

        Returns:
            Analyzerの出力（分析結果）
        """
        logger.info("=" * 80)
        logger.info("📊 Phase 3: Analyzer - データ分析と洞察")
        logger.info("=" * 80)

        try:
            # Analyzerへの指示を作成
            analyzer_prompt = f"""
【元の質問】
{original_query}

【調査計画（Coordinator）】
{coordinator_output}

【収集された情報（Researcher）】
{researcher_output}

上記の情報を分析し、深い洞察を導き出してください。
パターン、傾向、因果関係を特定し、データに基づいた論理的な推論を行ってください。
必要に応じてコードインタープリターやカスタムツールを活用してください。
"""

            # Analyzerに送信
            response = await self.analyzer.run(analyzer_prompt)

            # 実行履歴に記録
            self.execution_history.append({
                "agent": "Analyzer",
                "timestamp": datetime.now().isoformat(),
                "input": analyzer_prompt,
                "output": response.content
            })

            logger.info(f"✅ Analyzer完了: {len(response.content)}文字の分析を生成")
            return response.content

        except Exception as e:
            logger.error(f"❌ Analyzerエラー: {e}")
            raise

    async def run_summarizer(
        self,
        analyzer_output: str,
        researcher_output: str,
        coordinator_output: str,
        original_query: str
    ) -> str:
        """
        Summarizerエージェントを実行

        Args:
            analyzer_output: Analyzerの出力
            researcher_output: Researcherの出力
            coordinator_output: Coordinatorの出力
            original_query: 元のユーザークエリ

        Returns:
            Summarizerの出力（最終回答）
        """
        logger.info("=" * 80)
        logger.info("📝 Phase 4: Summarizer - 最終回答の作成")
        logger.info("=" * 80)

        try:
            # Summarizerへの指示を作成
            summarizer_prompt = f"""
【元の質問】
{original_query}

【調査計画（Coordinator）】
{coordinator_output}

【収集された情報（Researcher）】
{researcher_output}

【分析結果（Analyzer）】
{analyzer_output}

上記の全ての情報を統合し、ユーザーの質問に対する最終的な回答を作成してください。
わかりやすく構造化され、読みやすい形式で出力してください。
整形ツールを積極的に活用して、Markdown形式で美しく整形してください。
"""

            # Summarizerに送信
            response = await self.summarizer.run(summarizer_prompt)

            # 実行履歴に記録
            self.execution_history.append({
                "agent": "Summarizer",
                "timestamp": datetime.now().isoformat(),
                "input": summarizer_prompt,
                "output": response.content
            })

            logger.info(f"✅ Summarizer完了: {len(response.content)}文字の最終回答を生成")
            return response.content

        except Exception as e:
            logger.error(f"❌ Summarizerエラー: {e}")
            raise

    async def run(self, user_query: str) -> Dict[str, Any]:
        """
        完全なマルチエージェントワークフローを実行

        Args:
            user_query: ユーザーからの質問

        Returns:
            実行結果を含む辞書:
                - final_answer: 最終回答
                - execution_time: 実行時間（秒）
                - agent_outputs: 各エージェントの出力
        """
        start_time = datetime.now()

        logger.info("\n" + "=" * 80)
        logger.info("🚀 マルチエージェントワークフロー開始")
        logger.info("=" * 80)
        logger.info(f"質問: {user_query}\n")

        try:
            # エージェント初期化（まだの場合）
            if self.coordinator is None:
                await self.initialize_agents()

            # Phase 1: Coordinator
            coordinator_output = await self.run_coordinator(user_query)

            # Phase 2: Researcher
            researcher_output = await self.run_researcher(coordinator_output, user_query)

            # Phase 3: Analyzer
            analyzer_output = await self.run_analyzer(
                researcher_output,
                coordinator_output,
                user_query
            )

            # Phase 4: Summarizer
            final_answer = await self.run_summarizer(
                analyzer_output,
                researcher_output,
                coordinator_output,
                user_query
            )

            # 実行時間計算
            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds()

            logger.info("\n" + "=" * 80)
            logger.info("🎉 ワークフロー完了!")
            logger.info(f"⏱️  実行時間: {execution_time:.2f}秒")
            logger.info("=" * 80 + "\n")

            # 結果を返す
            return {
                "final_answer": final_answer,
                "execution_time": execution_time,
                "agent_outputs": {
                    "coordinator": coordinator_output,
                    "researcher": researcher_output,
                    "analyzer": analyzer_output,
                    "summarizer": final_answer
                },
                "execution_history": self.execution_history
            }

        except Exception as e:
            logger.error(f"\n❌ ワークフローエラー: {e}")
            raise


async def run_multi_agent_workflow(user_query: str) -> Dict[str, Any]:
    """
    マルチエージェントワークフローを実行する便利関数

    Args:
        user_query: ユーザーからの質問

    Returns:
        実行結果を含む辞書
    """
    workflow = MultiAgentWorkflow()
    return await workflow.run(user_query)


# 使用例
if __name__ == "__main__":
    async def main():
        # テスト用のクエリ
        query = "量子コンピューターの現状と将来性について教えてください"

        # ワークフロー実行
        result = await run_multi_agent_workflow(query)

        # 結果表示
        print("\n" + "=" * 80)
        print("最終回答:")
        print("=" * 80)
        print(result["final_answer"])
        print("\n" + "=" * 80)
        print(f"実行時間: {result['execution_time']:.2f}秒")
        print("=" * 80)

    # 実行
    asyncio.run(main())
