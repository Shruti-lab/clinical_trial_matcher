"""Application configuration management."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    # Application
    app_name: str = "Clinical Trial Matcher"
    debug: bool = False
    
    # Database
    database_url: str = "postgresql://user:password@localhost:5432/trialmatch"
    
    # AWS
    aws_region: str = "us-east-1"
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    s3_bucket_name: str = "trialmatch-documents"
    
    # Redis
    redis_url: str = "redis://localhost:6379/0"
    
    # Security
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440  # 24 hours
    
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)


settings = Settings()
