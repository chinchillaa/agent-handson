"""
設定管理

環境変数から設定を読み込みます。
Azure OpenAI ServiceとAzure Speech Serviceの設定を管理します。
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# プロジェクトルートの.envファイルを読み込み
project_root = Path(__file__).parent.parent.parent
env_path = project_root / ".env"
load_dotenv(env_path)


class Settings:
    """環境変数設定クラス"""

    # ========================================
    # Azure OpenAI 設定
    # ========================================
    AZURE_OPENAI_ENDPOINT: str = os.getenv("AZURE_OPENAI_ENDPOINT", "")
    AZURE_OPENAI_API_VERSION: str = os.getenv("AZURE_OPENAI_API_VERSION", "2024-08-01-preview")
    AZURE_OPENAI_API_KEY: str | None = os.getenv("AZURE_OPENAI_API_KEY")
    AZURE_REGION: str = os.getenv("AZURE_REGION", "eastus2")

    # GPT-5 デプロイメント名
    AZURE_OPENAI_DEPLOYMENT_GPT5: str = os.getenv("AZURE_OPENAI_DEPLOYMENT_GPT5", "gpt-5")

    # Agent 設定
    VOICE_AGENT_NAME: str = os.getenv("VOICE_AGENT_NAME", "VoiceAgent")
    MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", "3"))
    TIMEOUT_SECONDS: int = int(os.getenv("TIMEOUT_SECONDS", "60"))

    # GPT-5 特有の設定
    GPT5_MAX_TOKENS: int = int(os.getenv("GPT5_MAX_TOKENS", "4096"))
    GPT5_TEMPERATURE: float = float(os.getenv("GPT5_TEMPERATURE", "0.7"))

    # ========================================
    # Azure Speech Service 設定
    # ========================================
    AZURE_SPEECH_API_KEY: str = os.getenv("AZURE_SPEECH_API_KEY", "")
    AZURE_SPEECH_REGION: str = os.getenv("AZURE_SPEECH_REGION", "japaneast")
    AZURE_SPEECH_LANGUAGE: str = os.getenv("AZURE_SPEECH_LANGUAGE", "ja-JP")
    AZURE_SPEECH_VOICE_NAME: str = os.getenv("AZURE_SPEECH_VOICE_NAME", "ja-JP-NanamiNeural")

    # 音声認識設定
    SPEECH_RECOGNITION_TIMEOUT: int = int(os.getenv("SPEECH_RECOGNITION_TIMEOUT", "10"))  # 秒
    SPEECH_RECOGNITION_PHRASE_TIMEOUT: int = int(os.getenv("SPEECH_RECOGNITION_PHRASE_TIMEOUT", "5"))  # 秒

    # ========================================
    # 対話ループ安全設定（無限ループ防止）
    # ========================================
    # 最大対話回数（0=無制限、注意！）
    MAX_CONVERSATION_TURNS: int = int(os.getenv("MAX_CONVERSATION_TURNS", "50"))

    # 連続エラーの許容回数（この回数を超えたらセッション終了）
    MAX_CONSECUTIVE_ERRORS: int = int(os.getenv("MAX_CONSECUTIVE_ERRORS", "3"))

    # セッション最大時間（秒、0=無制限）
    MAX_SESSION_DURATION: int = int(os.getenv("MAX_SESSION_DURATION", "1800"))  # デフォルト30分

    # 終了キーワード
    EXIT_KEYWORDS: list[str] = ["exit", "quit", "終了", "さようなら", "バイバイ"]

    @classmethod
    def validate(cls) -> None:
        """
        設定の妥当性をチェック

        Raises:
            ValueError: 必須設定が不足している場合
        """
        # Azure OpenAI設定の検証
        if not cls.AZURE_OPENAI_ENDPOINT:
            raise ValueError(
                "AZURE_OPENAI_ENDPOINTが設定されていません。"
                ".envファイルを確認してください。"
            )

        if not cls.AZURE_OPENAI_API_KEY:
            print(
                "⚠️  AZURE_OPENAI_API_KEYが設定されていません。"
                "Azure CLI認証を使用します。'az login'を実行してください。"
            )

        # Azure Speech Service設定の検証
        if not cls.AZURE_SPEECH_API_KEY:
            raise ValueError(
                "AZURE_SPEECH_API_KEYが設定されていません。"
                ".envファイルを確認してください。"
            )

        if not cls.AZURE_SPEECH_REGION:
            raise ValueError(
                "AZURE_SPEECH_REGIONが設定されていません。"
                ".envファイルを確認してください。"
            )

        # 安全設定の警告
        if cls.MAX_CONVERSATION_TURNS == 0:
            print(
                "⚠️  MAX_CONVERSATION_TURNSが0（無制限）に設定されています。"
                "Azureリソースの使いすぎに注意してください。"
            )

        if cls.MAX_SESSION_DURATION == 0:
            print(
                "⚠️  MAX_SESSION_DURATIONが0（無制限）に設定されています。"
                "Azureリソースの使いすぎに注意してください。"
            )

    @classmethod
    def get_deployment_name(cls, model_type: str = "gpt5") -> str:
        """
        モデルタイプからデプロイメント名を取得

        Args:
            model_type: "gpt5" (デフォルト)

        Returns:
            デプロイメント名
        """
        if model_type == "gpt5":
            return cls.AZURE_OPENAI_DEPLOYMENT_GPT5
        else:
            raise ValueError(f"未対応のモデルタイプ: {model_type}")

    @classmethod
    def is_exit_keyword(cls, text: str) -> bool:
        """
        終了キーワードかどうかを判定

        Args:
            text: 判定するテキスト

        Returns:
            終了キーワードの場合True
        """
        return text.lower().strip() in [kw.lower() for kw in cls.EXIT_KEYWORDS]


# 設定インスタンス
settings = Settings()

# 注意: 起動時の自動検証はコメントアウト（main.py側で環境チェックを実施）
# settings.validate()
