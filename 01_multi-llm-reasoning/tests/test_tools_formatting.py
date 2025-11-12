import json
import sys
from pathlib import Path

# Ensure project dir on path
PROJECT_DIR = Path(__file__).resolve().parents[1]
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from tools.formatting_tools import (
    format_as_markdown,
    create_bullet_list,
    structure_as_json,
    create_summary_table,
    highlight_key_points,
    format_conclusion,
    clean_text,
    add_metadata,
)


def test_format_as_markdown_dict_and_list():
    md = format_as_markdown({"セクション": ["A", "B"], "詳細": {"x": 1}})
    assert "#" in md and "## セクション" in md and "- A" in md


def test_create_bullet_list():
    ul = create_bullet_list(["a", "b"]) 
    ol = create_bullet_list(["a", "b"], ordered=True)
    assert ul.startswith("-") and ol.startswith("1.")


def test_structure_as_json():
    s = structure_as_json({"a": 1}, pretty=True)
    assert json.loads(s)["a"] == 1


def test_create_summary_table():
    t = create_summary_table(["H1", "H2"], [[1, 2], [3, 4]])
    assert "| H1 | H2 |" in t and "---" in t


def test_highlight_key_points():
    out = highlight_key_points("AzureとOpenAI", ["Azure"]) 
    assert "**Azure**" in out


def test_format_conclusion_and_clean_text_and_add_metadata():
    doc = format_conclusion("まとめ", ["発見1"])
    cleaned = clean_text(doc + "\n\n\n")
    with_meta = add_metadata(cleaned, {"title": "t"})
    assert "# 結論" in with_meta and "title: t" in with_meta

