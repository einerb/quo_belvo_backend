from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, field_validator
from typing import List
import warnings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: PostgresDsn
    
    BELVO_SECRET_PASSWORD: str
    BELVO_SECRET_ID: str
    BELVO_API_URL: str
    SECRET: str
    
    ENV: str = "development"
    DEBUG: bool = True if ENV != "production" else False

    @field_validator('DATABASE_URL')
    def validate_db_url(cls, v):
        if "+asyncpg" not in str(v):
            raise ValueError("URL debe incluir +asyncpg")
        return v
    
    class Config:
        env_file = ".env" if os.getenv("ENV", "development") == "development" else None
        env_file_encoding = "utf-8"
        case_sensitive = True

settings = Settings(_env_file='.env')

if not settings.DATABASE_URL:
    raise ValueError("DATABASE_URL es requerido")