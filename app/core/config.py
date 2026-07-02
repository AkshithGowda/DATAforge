from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str

    UPLOAD_DIR: str = "uploads"
    CLEANED_DIR: str = "cleaned"
    REPORTS_DIR: str = "reports"

    MAX_FILE_SIZE_MB: int = 50

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()

Path(settings.UPLOAD_DIR).mkdir(exist_ok=True)
Path(settings.CLEANED_DIR).mkdir(exist_ok=True)
Path(settings.REPORTS_DIR).mkdir(exist_ok=True)
