"""
テキスト整形関連のカスタムツール

Summarizer Agentが使用するテキスト整形・構造化機能を提供します。
"""

from typing import List, Dict, Any
import json
import re


def format_as_markdown(content: Dict[str, Any], title: str = "分析結果") -> str:
    """
    辞書データをMarkdown形式に整形する

    Args:
        content: 整形するコンテンツ（辞書形式）
        title: ドキュメントタイトル

    Returns:
        Markdown形式のテキスト
    """
    md_lines = [f"# {title}", ""]

    for key, value in content.items():
        # セクションヘッダー
        md_lines.append(f"## {key}")
        md_lines.append("")

        # 値の型に応じて整形
        if isinstance(value, list):
            for item in value:
                md_lines.append(f"- {item}")
        elif isinstance(value, dict):
            for sub_key, sub_value in value.items():
                md_lines.append(f"**{sub_key}**: {sub_value}")
        else:
            md_lines.append(str(value))

        md_lines.append("")

    return "\n".join(md_lines)


def create_bullet_list(items: List[str], ordered: bool = False) -> str:
    """
    箇条書きリストを作成する

    Args:
        items: リスト項目
        ordered: 順序付きリストにするか（True: 番号付き、False: 記号）

    Returns:
        整形されたリスト文字列
    """
    if not items:
        return ""

    lines = []
    for i, item in enumerate(items, 1):
        if ordered:
            lines.append(f"{i}. {item}")
        else:
            lines.append(f"- {item}")

    return "\n".join(lines)


def structure_as_json(data: Dict[str, Any], pretty: bool = True) -> str:
    """
    データをJSON形式で構造化する

    Args:
        data: 構造化するデータ
        pretty: 読みやすく整形するか

    Returns:
        JSON文字列
    """
    if pretty:
        return json.dumps(data, ensure_ascii=False, indent=2)
    else:
        return json.dumps(data, ensure_ascii=False)


def create_summary_table(headers: List[str], rows: List[List[Any]]) -> str:
    """
    Markdown形式のテーブルを作成する

    Args:
        headers: テーブルヘッダー
        rows: テーブルの各行データ

    Returns:
        Markdown形式のテーブル
    """
    if not headers or not rows:
        return ""

    # ヘッダー行
    header_row = "| " + " | ".join(str(h) for h in headers) + " |"

    # 区切り行
    separator = "| " + " | ".join("---" for _ in headers) + " |"

    # データ行
    data_rows = []
    for row in rows:
        # ヘッダー数に合わせて調整
        adjusted_row = row[:len(headers)]
        while len(adjusted_row) < len(headers):
            adjusted_row.append("")

        data_row = "| " + " | ".join(str(cell) for cell in adjusted_row) + " |"
        data_rows.append(data_row)

    # 結合
    table = [header_row, separator] + data_rows
    return "\n".join(table)


def highlight_key_points(text: str, keywords: List[str]) -> str:
    """
    テキスト内のキーワードを強調表示する（Markdown形式）

    Args:
        text: 元のテキスト
        keywords: 強調したいキーワードのリスト

    Returns:
        キーワードが強調されたテキスト
    """
    result = text

    for keyword in keywords:
        # 大文字小文字を区別しない置換
        pattern = re.compile(re.escape(keyword), re.IGNORECASE)
        result = pattern.sub(f"**{keyword}**", result)

    return result


def format_conclusion(
    summary: str,
    key_findings: List[str],
    recommendations: List[str] = None
) -> str:
    """
    結論セクションを整形する

    Args:
        summary: 要約
        key_findings: 主要な発見事項のリスト
        recommendations: 推奨事項のリスト（オプション）

    Returns:
        整形された結論セクション
    """
    sections = ["# 結論", "", "## 要約", summary, ""]

    # 主要な発見事項
    sections.append("## 主要な発見事項")
    sections.append("")
    for i, finding in enumerate(key_findings, 1):
        sections.append(f"{i}. {finding}")
    sections.append("")

    # 推奨事項（存在する場合）
    if recommendations:
        sections.append("## 推奨事項")
        sections.append("")
        for i, rec in enumerate(recommendations, 1):
            sections.append(f"{i}. {rec}")
        sections.append("")

    return "\n".join(sections)


def clean_text(text: str) -> str:
    """
    テキストをクリーンアップする（余分な空白・改行を削除）

    Args:
        text: クリーンアップするテキスト

    Returns:
        クリーンアップされたテキスト
    """
    # 連続する空白を1つに
    text = re.sub(r' +', ' ', text)

    # 連続する改行を最大2つに
    text = re.sub(r'\n{3,}', '\n\n', text)

    # 前後の空白を削除
    text = text.strip()

    return text


def add_metadata(content: str, metadata: Dict[str, str]) -> str:
    """
    コンテンツにメタデータを追加する

    Args:
        content: 元のコンテンツ
        metadata: 追加するメタデータ（キー: 値）

    Returns:
        メタデータ付きコンテンツ
    """
    meta_lines = ["---"]
    for key, value in metadata.items():
        meta_lines.append(f"{key}: {value}")
    meta_lines.append("---")
    meta_lines.append("")

    return "\n".join(meta_lines) + content
