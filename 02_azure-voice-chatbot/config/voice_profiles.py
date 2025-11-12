"""
音声プロファイル定義

Azure Speech Service Neural Voiceの各種設定とプロファイルを定義します。
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class VoiceProfile:
    """
    音声プロファイル

    音声の特性を定義するデータクラス
    """
    name: str  # プロファイル名
    voice_name: str  # Azure音声名
    language: str  # 言語コード
    gender: str  # 性別（Male/Female）
    description: str  # 説明
    style: Optional[str] = None  # 話し方スタイル（対応している場合）
    speaking_rate: float = 1.0  # 話速（0.5 ~ 2.0）
    pitch: str = "+0%"  # ピッチ（-50% ~ +50%）


# 日本語Neural Voice一覧
JAPANESE_VOICES = {
    # 女性音声
    "nanami": VoiceProfile(
        name="Nanami（ななみ）",
        voice_name="ja-JP-NanamiNeural",
        language="ja-JP",
        gender="Female",
        description="明るく親しみやすい女性の声。標準的な日本語。",
        style=None,
        speaking_rate=1.0,
        pitch="+0%"
    ),
    "mayu": VoiceProfile(
        name="Mayu（まゆ）",
        voice_name="ja-JP-MayuNeural",
        language="ja-JP",
        gender="Female",
        description="若々しく元気な女性の声。",
        style=None,
        speaking_rate=1.0,
        pitch="+0%"
    ),
    "shiori": VoiceProfile(
        name="Shiori（しおり）",
        voice_name="ja-JP-ShioriNeural",
        language="ja-JP",
        gender="Female",
        description="落ち着いた大人の女性の声。",
        style=None,
        speaking_rate=1.0,
        pitch="+0%"
    ),

    # 男性音声
    "keita": VoiceProfile(
        name="Keita（けいた）",
        voice_name="ja-JP-KeitaNeural",
        language="ja-JP",
        gender="Male",
        description="明るく親しみやすい男性の声。標準的な日本語。",
        style=None,
        speaking_rate=1.0,
        pitch="+0%"
    ),
    "daichi": VoiceProfile(
        name="Daichi（だいち）",
        voice_name="ja-JP-DaichiNeural",
        language="ja-JP",
        gender="Male",
        description="落ち着いた大人の男性の声。",
        style=None,
        speaking_rate=1.0,
        pitch="+0%"
    ),
    "naoki": VoiceProfile(
        name="Naoki（なおき）",
        voice_name="ja-JP-NaokiNeural",
        language="ja-JP",
        gender="Male",
        description="若々しく元気な男性の声。",
        style=None,
        speaking_rate=1.0,
        pitch="+0%"
    ),
}


# 話速プリセット
SPEAKING_RATES = {
    "very_slow": 0.5,    # とてもゆっくり
    "slow": 0.75,        # ゆっくり
    "normal": 1.0,       # 標準
    "fast": 1.25,        # 速い
    "very_fast": 1.5,    # とても速い
}


# ピッチプリセット
PITCH_PRESETS = {
    "very_low": "-30%",   # とても低い
    "low": "-15%",        # 低い
    "normal": "+0%",      # 標準
    "high": "+15%",       # 高い
    "very_high": "+30%",  # とても高い
}


# カスタムプロファイル（プリセット）
CUSTOM_PROFILES = {
    "default": VoiceProfile(
        name="デフォルト",
        voice_name="ja-JP-NanamiNeural",
        language="ja-JP",
        gender="Female",
        description="標準的な設定。明るく親しみやすい女性の声。",
        speaking_rate=1.0,
        pitch="+0%"
    ),

    "gentle": VoiceProfile(
        name="優しい",
        voice_name="ja-JP-ShioriNeural",
        language="ja-JP",
        gender="Female",
        description="落ち着いて優しい話し方。",
        speaking_rate=0.9,
        pitch="-5%"
    ),

    "energetic": VoiceProfile(
        name="元気",
        voice_name="ja-JP-MayuNeural",
        language="ja-JP",
        gender="Female",
        description="明るく元気な話し方。",
        speaking_rate=1.1,
        pitch="+5%"
    ),

    "calm_male": VoiceProfile(
        name="落ち着いた男性",
        voice_name="ja-JP-DaichiNeural",
        language="ja-JP",
        gender="Male",
        description="落ち着いて信頼感のある男性の声。",
        speaking_rate=0.95,
        pitch="-10%"
    ),

    "friendly_male": VoiceProfile(
        name="親しみやすい男性",
        voice_name="ja-JP-KeitaNeural",
        language="ja-JP",
        gender="Male",
        description="明るく親しみやすい男性の声。",
        speaking_rate=1.0,
        pitch="+0%"
    ),
}


def get_voice_profile(profile_name: str) -> Optional[VoiceProfile]:
    """
    プロファイル名から音声プロファイルを取得

    Args:
        profile_name: プロファイル名

    Returns:
        VoiceProfileオブジェクト（存在しない場合はNone）
    """
    # カスタムプロファイルから検索
    if profile_name in CUSTOM_PROFILES:
        return CUSTOM_PROFILES[profile_name]

    # 個別音声から検索
    if profile_name in JAPANESE_VOICES:
        return JAPANESE_VOICES[profile_name]

    return None


def list_available_profiles() -> list[str]:
    """
    利用可能なプロファイル名のリストを取得

    Returns:
        プロファイル名のリスト
    """
    return list(CUSTOM_PROFILES.keys()) + list(JAPANESE_VOICES.keys())


def get_profile_description(profile_name: str) -> str:
    """
    プロファイルの説明を取得

    Args:
        profile_name: プロファイル名

    Returns:
        プロファイルの説明（存在しない場合はエラーメッセージ）
    """
    profile = get_voice_profile(profile_name)
    if profile:
        return f"{profile.name}: {profile.description}"
    return f"プロファイル '{profile_name}' は存在しません。"


def create_custom_profile(
    name: str,
    base_voice: str = "nanami",
    speaking_rate: float = 1.0,
    pitch: str = "+0%",
    description: str = "カスタムプロファイル"
) -> VoiceProfile:
    """
    カスタム音声プロファイルを作成

    Args:
        name: プロファイル名
        base_voice: ベースとなる音声（JAPANESE_VOICESのキー）
        speaking_rate: 話速（0.5 ~ 2.0）
        pitch: ピッチ（-50% ~ +50%）
        description: 説明

    Returns:
        カスタムVoiceProfileオブジェクト
    """
    base = JAPANESE_VOICES.get(base_voice, JAPANESE_VOICES["nanami"])

    return VoiceProfile(
        name=name,
        voice_name=base.voice_name,
        language=base.language,
        gender=base.gender,
        description=description,
        speaking_rate=speaking_rate,
        pitch=pitch
    )


if __name__ == "__main__":
    """テスト実行"""
    print("=== 音声プロファイル一覧 ===\n")

    print("【カスタムプロファイル】")
    for key, profile in CUSTOM_PROFILES.items():
        print(f"  {key}: {profile.name}")
        print(f"    音声: {profile.voice_name}")
        print(f"    説明: {profile.description}")
        print(f"    話速: {profile.speaking_rate}x, ピッチ: {profile.pitch}")
        print()

    print("【日本語音声一覧】")
    for key, profile in JAPANESE_VOICES.items():
        print(f"  {key}: {profile.name} ({profile.gender})")
        print(f"    音声名: {profile.voice_name}")
        print(f"    説明: {profile.description}")
        print()

    print("【話速プリセット】")
    for key, rate in SPEAKING_RATES.items():
        print(f"  {key}: {rate}x")

    print("\n【ピッチプリセット】")
    for key, pitch in PITCH_PRESETS.items():
        print(f"  {key}: {pitch}")
