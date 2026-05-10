from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str
    APP_ENV: str
    DEBUG: bool

    DATABASE_URL: str = ""
    DATABASE_SYNC_URL: str = ""

    JWT_SECRET: str
    JWT_ALGORITHM: str
    JWT_EXPIRE_DAYS: int

    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-3-flash-preview"

    CORS_ORIGINS: str = ""

    @property
    def cors_origins_list(self) -> List[str]:
        if not self.CORS_ORIGINS:
            return []

        return [
            origin.strip()
            for origin in self.CORS_ORIGINS.split(",")
        ]

    class Config:
        env_file = ".env"


settings = Settings()