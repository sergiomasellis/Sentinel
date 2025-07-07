"""Configuration management for Sentinel"""

from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    # Application
    DEBUG: bool = False
    SECRET_KEY: str
    API_PREFIX: str = "/api/v1"
    
    # Azure OpenAI
    AZURE_OPENAI_API_KEY: str
    AZURE_OPENAI_ENDPOINT: str
    AZURE_OPENAI_API_VERSION: str = "2024-10-01"
    AZURE_OPENAI_DEPLOYMENT_NAME: str = "gpt-4"
    
    # AWS
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_REGION: str = "us-east-1"
    
    # Bitbucket
    BITBUCKET_API_URL: str = "https://api.bitbucket.org/2.0"
    BITBUCKET_ACCESS_TOKEN: str
    
    # Jira
    JIRA_URL: str
    JIRA_EMAIL: str
    JIRA_API_TOKEN: str
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Database
    DATABASE_URL: str
    
    # Observability
    ARIZE_PHOENIX_API_KEY: Optional[str] = None
    OTLP_ENDPOINT: str = "http://localhost:4317"


settings = Settings()