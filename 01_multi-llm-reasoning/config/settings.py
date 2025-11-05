"""
設定管理

環境変数から設定を読み込みます。
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

    # Azure OpenAI 設定
    AZURE_OPENAI_ENDPOINT: str = os.getenv("AZURE_OPENAI_ENDPOINT", "")
    AZURE_OPENAI_API_VERSION: str = os.getenv("AZURE_OPENAI_API_VERSION", "2024-08-01-preview")
    AZURE_OPENAI_API_KEY: str | None = os.getenv("AZURE_OPENAI_API_KEY")
    AZURE_REGION: str = os.getenv("AZURE_REGION", "eastus2")

    # GPT-5 デプロイメント名
    AZURE_OPENAI_DEPLOYMENT_GPT5: str = os.getenv("AZURE_OPENAI_DEPLOYMENT_GPT5", "gpt-5")
    AZURE_OPENAI_DEPLOYMENT_GPT5_MINI: str = os.getenv("AZURE_OPENAI_DEPLOYMENT_GPT5_MINI", "gpt-5-mini")

    # Agent 設定
    MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", "3"))
    TIMEOUT_SECONDS: int = int(os.getenv("TIMEOUT_SECONDS", "60"))
    ENABLE_STREAMING: bool = os.getenv("ENABLE_STREAMING", "true").lower() == "true"

    # GPT-5 特有の設定
    GPT5_MAX_TOKENS: int = int(os.getenv("GPT5_MAX_TOKENS", "4096"))
    GPT5_TEMPERATURE: float = float(os.getenv("GPT5_TEMPERATURE", "0.7"))

    @classmethod
    def validate(cls) -> None:
        """
        設定の妥当性をチェック

        Raises:
            ValueError: 必須設定が不足している場合
        """
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

    @classmethod
    def get_deployment_name(cls, model_type: str) -> str:
        """
        モデルタイプからデプロイメント名を取得

        Args:
            model_type: "gpt5" or "gpt5-mini"

        Returns:
            デプロイメント名
        """
        if model_type == "gpt5":
            return cls.AZURE_OPENAI_DEPLOYMENT_GPT5
        elif model_type == "gpt5-mini":
            return cls.AZURE_OPENAI_DEPLOYMENT_GPT5_MINI
        else:
            raise ValueError(f"未対応のモデルタイプ: {model_type}")


# 設定インスタンス
settings = Settings()

# 起動時に設定を検証
settings.validate()
