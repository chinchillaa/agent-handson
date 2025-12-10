"""
Tools package exports

agent-frameworkに互換性のあるカスタムツールをエクスポートします。
"""

# Web検索ツール
from tools.web_tools import (
    extract_key_information,
    summarize_search_results,
    organize_information,
    validate_sources
)

# データ分析ツール
from tools.analysis_tools import (
    calculate_statistics,
    compare_data,
    extract_numbers_from_text,
    analyze_trend,
    categorize_data
)

# テキスト整形ツール
from tools.formatting_tools import (
    format_as_markdown,
    create_bullet_list,
    structure_as_json,
    create_summary_table,
    highlight_key_points,
    format_conclusion,
    clean_text,
    add_metadata
)

__all__ = [
    # Web tools
    "extract_key_information",
    "summarize_search_results",
    "organize_information",
    "validate_sources",
    # Analysis tools
    "calculate_statistics",
    "compare_data",
    "extract_numbers_from_text",
    "analyze_trend",
    "categorize_data",
    # Formatting tools
    "format_as_markdown",
    "create_bullet_list",
    "structure_as_json",
    "create_summary_table",
    "highlight_key_points",
    "format_conclusion",
    "clean_text",
    "add_metadata",
]
