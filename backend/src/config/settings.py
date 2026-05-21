"""Application settings loaded from environment variables."""

import os


class Settings:
    """Application configuration."""

    API_BASE_URL: str = os.getenv("API_BASE_URL", "https://practice.expandtesting.com/notes/api")


settings = Settings()
