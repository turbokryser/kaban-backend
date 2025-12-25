from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # SMTP Settings for Mail.ru
    SMTP_HOST: str = "smtp.mail.ru"
    SMTP_PORT: int = 587
    SMTP_USER: str
    SMTP_PASSWORD: str
    SMTP_FROM_EMAIL: str
    FRONTEND_URL: str = "http://localhost:3000"  # URL для ссылок активации

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()



