import importlib
import os
import sys
from pathlib import Path
import pytest

# Ensure project dir on path
PROJECT_DIR = Path(__file__).resolve().parents[1]
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))


def _reload_settings_module():
    # Drop cached modules to re-evaluate env
    sys.modules.pop("config", None)
    sys.modules.pop("config.settings", None)
    return importlib.import_module("config.settings")


def test_settings_validate_ok(monkeypatch):
    monkeypatch.setenv("AZURE_OPENAI_ENDPOINT", "https://example.openai.azure.com")
    m = _reload_settings_module()
    # If import succeeded, validate already ran; ensure values are set
    assert m.settings.AZURE_OPENAI_ENDPOINT.startswith("https://")


def test_settings_validate_missing_endpoint_raises(monkeypatch):
    monkeypatch.delenv("AZURE_OPENAI_ENDPOINT", raising=False)
    # Re-import should raise ValueError during validation
    sys.modules.pop("config", None)
    sys.modules.pop("config.settings", None)
    with pytest.raises(ValueError):
        importlib.import_module("config.settings")

