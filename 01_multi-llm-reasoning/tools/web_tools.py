"""
Web検索関連のカスタムツール

Researcher Agentが使用する情報抽出・整理機能を提供します。
"""

from typing import List, Dict, Any
import json
import re


def extract_key_information(text: str, keywords: List[str]) -> str:
    """
    テキストからキーワードに関連する重要情報を抽出する

    Args:
        text: 抽出対象のテキスト
        keywords: 検索するキーワードのリスト

    Returns:
        抽出された情報を含むJSON文字列
    """
    results = []

    # テキストを文単位に分割
    sentences = re.split(r'[。．.!?！？\n]+', text)

    for keyword in keywords:
        keyword_lower = keyword.lower()
        matched_sentences = []

        for sentence in sentences:
            if keyword_lower in sentence.lower() and sentence.strip():
                matched_sentences.append(sentence.strip())

        if matched_sentences:
            results.append({
                "keyword": keyword,
                "matches": matched_sentences[:3]  # 最大3件まで
            })

    return json.dumps(results, ensure_ascii=False, indent=2)


def summarize_search_results(results: str, max_length: int = 500) -> str:
    """
    検索結果を要約する

    Args:
        results: 検索結果のテキスト
        max_length: 要約の最大文字数

    Returns:
        要約されたテキスト
    """
    # 改行を除去して整形
    cleaned = re.sub(r'\s+', ' ', results).strip()

    if len(cleaned) <= max_length:
        return cleaned

    # 文単位で分割
    sentences = re.split(r'[。．.!?！？]', cleaned)

    # 重要な文を選択（先頭から順に）
    summary = []
    current_length = 0

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue

        if current_length + len(sentence) <= max_length:
            summary.append(sentence)
            current_length += len(sentence)
        else:
            break

    result = '。'.join(summary)
    if result and not result.endswith('。'):
        result += '。'

    return result


def organize_information(raw_data: str, categories: List[str]) -> str:
    """
    生データを指定されたカテゴリに整理する

    Args:
        raw_data: 整理する生データ
        categories: カテゴリのリスト

    Returns:
        カテゴリ別に整理された情報のJSON文字列
    """
    organized = {}

    # テキストを文単位に分割
    sentences = re.split(r'[。．.!?！？\n]+', raw_data)

    for category in categories:
        category_lower = category.lower()
        matched_sentences = []

        for sentence in sentences:
            if category_lower in sentence.lower() and sentence.strip():
                matched_sentences.append(sentence.strip())

        if matched_sentences:
            organized[category] = matched_sentences[:5]  # 最大5件まで

    # カテゴリに該当しない情報
    all_matched = set()
    for items in organized.values():
        all_matched.update(items)

    other_sentences = [
        s.strip() for s in sentences
        if s.strip() and s.strip() not in all_matched
    ][:3]  # その他は最大3件

    if other_sentences:
        organized["その他"] = other_sentences

    return json.dumps(organized, ensure_ascii=False, indent=2)


def validate_sources(text: str) -> Dict[str, Any]:
    """
    テキスト内のURL・引用元の妥当性を簡易チェック

    Args:
        text: チェック対象のテキスト

    Returns:
        検証結果の辞書
    """
    # URLパターンを検索
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    urls = re.findall(url_pattern, text)

    # 引用パターン（「」や""で囲まれた部分）
    quote_pattern = r'[「""]([^」""]+)[」""]'
    quotes = re.findall(quote_pattern, text)

    return {
        "found_urls": len(urls),
        "urls": urls[:5],  # 最大5件まで
        "found_quotes": len(quotes),
        "quotes": quotes[:5],  # 最大5件まで
        "has_sources": len(urls) > 0 or len(quotes) > 0
    }
