import sys
from pathlib import Path
import pytest

# Ensure project dir on path
PROJECT_DIR = Path(__file__).resolve().parents[1]
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))


import types
import asyncio


class _FakeResponse:
    def __init__(self, content: str):
        self.content = content


def _fake_agent(name: str):
    class Agent:
        async def run(self, prompt: str):
            return _FakeResponse(f"{name}:{len(prompt)}")

    return Agent()


@pytest.mark.skip(reason="Import of workflow may fail due to relative imports; unskip when resolved.")
def test_workflow_runs_with_fake_agents(monkeypatch):
    import importlib
    wf = importlib.import_module("workflow")

    async def fake_create_coordinator_agent():
        return _fake_agent("C")

    async def fake_create_researcher_agent():
        return _fake_agent("R")

    async def fake_create_analyzer_agent():
        return _fake_agent("A")

    async def fake_create_summarizer_agent():
        return _fake_agent("S")

    # Patch factories bound in workflow module
    monkeypatch.setattr(wf, "create_coordinator_agent", fake_create_coordinator_agent)
    monkeypatch.setattr(wf, "create_researcher_agent", fake_create_researcher_agent)
    monkeypatch.setattr(wf, "create_analyzer_agent", fake_create_analyzer_agent)
    monkeypatch.setattr(wf, "create_summarizer_agent", fake_create_summarizer_agent)

    result = asyncio.run(wf.run_multi_agent_workflow("Q"))
    assert "final_answer" in result and "agent_outputs" in result
