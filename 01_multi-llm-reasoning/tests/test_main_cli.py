import asyncio
import sys
from pathlib import Path

import builtins
import types

# Ensure project dir on path
PROJECT_DIR = Path(__file__).resolve().parents[1]
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))


async def _fake_workflow(query: str):
    # Minimal shape expected by main.py
    return {
        "final_answer": f"回答: {query}",
        "execution_time": 0.12,
        "agent_outputs": {
            "coordinator": "c",
            "researcher": "r",
            "analyzer": "a",
            "summarizer": "s",
        },
    }


def test_main_cli_runs_with_stubbed_workflow(monkeypatch):
    # Prepare environment
    monkeypatch.setenv("AZURE_OPENAI_ENDPOINT", "https://example.openai.azure.com")

    import importlib
    main = importlib.import_module("main")

    # Stub workflow function
    monkeypatch.setattr(main, "run_multi_agent_workflow", _fake_workflow)

    # Simulate CLI args
    monkeypatch.setenv("PYTHONIOENCODING", "utf-8")
    test_args = ["prog", "テスト質問", "--no-banner"]
    monkeypatch.setattr(sys, "argv", test_args)

    # Run the async main
    asyncio.run(main.main())

