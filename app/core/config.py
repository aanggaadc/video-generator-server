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
    GEMINI_MODEL: str = "gemini-1.5-flash"

    class Config:
        env_file = ".env"


settings = Settings()