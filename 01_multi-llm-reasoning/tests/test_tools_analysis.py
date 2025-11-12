import json
import sys
from pathlib import Path

# Ensure project dir on path
PROJECT_DIR = Path(__file__).resolve().parents[1]
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from tools.analysis_tools import (
    calculate_statistics,
    compare_data,
    extract_numbers_from_text,
    analyze_trend,
    categorize_data,
)


def test_calculate_statistics_happy_path():
    stats = json.loads(calculate_statistics([1, 2, 3, 4]))
    assert stats["count"] == 4
    assert stats["mean"] == 2.5


def test_compare_data_basic():
    res = json.loads(compare_data([1, 2], [3, 4], "A", "B"))
    assert "A" in res and "B" in res and "comparison" in res


def test_extract_numbers_from_text():
    nums = extract_numbers_from_text("売上は1,234.5、コストは-12です")
    assert 1234.5 in nums and -12.0 in nums


def test_analyze_trend_increasing():
    res = json.loads(analyze_trend([1, 2, 3, 5]))
    assert res["trend"] in ("上昇傾向", "横ばい", "下降傾向")


def test_categorize_data_threshold():
    res = json.loads(categorize_data({"a": 1, "b": 10}, threshold=5))
    assert res["high_category"] == {"b": 10}
    assert res["low_category"] == {"a": 1}

