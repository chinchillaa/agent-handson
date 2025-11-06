"""
データ分析関連のカスタムツール

Analyzer Agentが使用するデータ分析・統計機能を提供します。
注: 複雑な計算はHostedCodeInterpreterToolを使用してください。
"""

from typing import List, Dict, Any, Union
import json
import statistics
import re


def calculate_statistics(numbers: List[Union[int, float]]) -> str:
    """
    数値リストの基本統計量を計算する

    Args:
        numbers: 数値のリスト

    Returns:
        統計量を含むJSON文字列
    """
    if not numbers:
        return json.dumps({"error": "数値リストが空です"}, ensure_ascii=False)

    try:
        stats = {
            "count": len(numbers),
            "sum": sum(numbers),
            "mean": statistics.mean(numbers),
            "median": statistics.median(numbers),
            "min": min(numbers),
            "max": max(numbers),
            "range": max(numbers) - min(numbers)
        }

        # 標準偏差（要素数が2以上の場合のみ）
        if len(numbers) >= 2:
            stats["stdev"] = statistics.stdev(numbers)
            stats["variance"] = statistics.variance(numbers)

        return json.dumps(stats, ensure_ascii=False, indent=2)

    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)


def compare_data(data1: List[Union[int, float]], data2: List[Union[int, float]],
                 label1: str = "データ1", label2: str = "データ2") -> str:
    """
    2つのデータセットを比較する

    Args:
        data1: 最初のデータセット
        data2: 2番目のデータセット
        label1: データ1のラベル
        label2: データ2のラベル

    Returns:
        比較結果のJSON文字列
    """
    if not data1 or not data2:
        return json.dumps({"error": "データセットが空です"}, ensure_ascii=False)

    try:
        result = {
            label1: {
                "count": len(data1),
                "mean": statistics.mean(data1),
                "median": statistics.median(data1),
                "min": min(data1),
                "max": max(data1)
            },
            label2: {
                "count": len(data2),
                "mean": statistics.mean(data2),
                "median": statistics.median(data2),
                "min": min(data2),
                "max": max(data2)
            },
            "comparison": {
                "mean_difference": statistics.mean(data2) - statistics.mean(data1),
                "median_difference": statistics.median(data2) - statistics.median(data1)
            }
        }

        # 平均の比較
        mean1 = statistics.mean(data1)
        mean2 = statistics.mean(data2)

        if mean2 > mean1:
            result["comparison"]["mean_trend"] = f"{label2}の平均が{label1}より高い"
        elif mean2 < mean1:
            result["comparison"]["mean_trend"] = f"{label1}の平均が{label2}より高い"
        else:
            result["comparison"]["mean_trend"] = "平均値は同じ"

        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)


def extract_numbers_from_text(text: str) -> List[float]:
    """
    テキストから数値を抽出する

    Args:
        text: 数値を含むテキスト

    Returns:
        抽出された数値のリスト
    """
    # 数値パターン（整数、小数、カンマ区切りの数値）
    pattern = r'-?\d+(?:,\d{3})*(?:\.\d+)?'
    matches = re.findall(pattern, text)

    # カンマを除去して数値に変換
    numbers = []
    for match in matches:
        try:
            num = float(match.replace(',', ''))
            numbers.append(num)
        except ValueError:
            continue

    return numbers


def analyze_trend(data: List[Union[int, float]]) -> str:
    """
    データのトレンド（増加傾向・減少傾向）を分析する

    Args:
        data: 時系列データのリスト

    Returns:
        トレンド分析結果のJSON文字列
    """
    if len(data) < 2:
        return json.dumps({"error": "データポイントが不足しています（最低2個必要）"}, ensure_ascii=False)

    try:
        # 差分を計算
        differences = [data[i+1] - data[i] for i in range(len(data) - 1)]

        # 増加・減少のカウント
        increases = sum(1 for d in differences if d > 0)
        decreases = sum(1 for d in differences if d < 0)
        no_change = sum(1 for d in differences if d == 0)

        # トレンド判定
        if increases > decreases:
            trend = "上昇傾向"
        elif decreases > increases:
            trend = "下降傾向"
        else:
            trend = "横ばい"

        # 平均変化率
        avg_change = statistics.mean(differences) if differences else 0

        result = {
            "trend": trend,
            "total_points": len(data),
            "increases": increases,
            "decreases": decreases,
            "no_change": no_change,
            "average_change": avg_change,
            "total_change": data[-1] - data[0],
            "percent_change": ((data[-1] - data[0]) / data[0] * 100) if data[0] != 0 else 0
        }

        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)


def categorize_data(data: Dict[str, Any], threshold: Union[int, float]) -> str:
    """
    データを閾値に基づいてカテゴリ分けする

    Args:
        data: カテゴリ分けするデータ（キー: 項目名、値: 数値）
        threshold: 分類の閾値

    Returns:
        カテゴリ分けされた結果のJSON文字列
    """
    try:
        high = {}
        low = {}

        for key, value in data.items():
            if isinstance(value, (int, float)):
                if value >= threshold:
                    high[key] = value
                else:
                    low[key] = value

        result = {
            "threshold": threshold,
            "high_category": high,
            "low_category": low,
            "high_count": len(high),
            "low_count": len(low)
        }

        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)
