from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Finance Dashboard API"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "super-secret-key-change-me-later"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8 
    DATABASE_URL: str = "sqlite:///./finance.db"

    class Config:
        env_file = ".env"

settings = Settings()
