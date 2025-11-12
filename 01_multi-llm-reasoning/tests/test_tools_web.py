import json
import os
import sys
from pathlib import Path

# Ensure project dir on path
PROJECT_DIR = Path(__file__).resolve().parents[1]
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from tools.web_tools import (
    extract_key_information,
    summarize_search_results,
    organize_information,
    validate_sources,
)


def test_extract_key_information_basic():
    text = "Azureはクラウドプラットフォームです。OpenAIとの連携も可能。GPT-5が利用できます。"
    result = json.loads(extract_key_information(text, ["Azure", "GPT-5"]))
    assert isinstance(result, list)
    # Expect at least one match for each keyword
    keys = {item["keyword"] for item in result}
    assert "Azure" in keys and "GPT-5" in keys


def test_summarize_search_results_truncates():
    long_text = "。".join([f"文{i}" for i in range(100)])
    summary = summarize_search_results(long_text, max_length=20)
    assert len(summary) <= 40  # rough guard
    assert "文" in summary


def test_organize_information_groups_categories():
    raw = "性能が向上。コストが低下。性能の課題もある。他の話題。"
    organized = json.loads(organize_information(raw, ["性能", "コスト"]))
    assert "性能" in organized and "コスト" in organized
    # may include その他 bucket
    assert isinstance(organized, dict)


def test_validate_sources_detects_urls_and_quotes():
    text = '参考: https://example.com/article "重要な引用" も含む'
    res = validate_sources(text)
    assert res["found_urls"] >= 1
    assert res["has_sources"] is True

