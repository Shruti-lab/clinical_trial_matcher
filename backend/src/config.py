"""Application configuration management."""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field


class Settings(BaseSettings):
    """Application settings."""

    # Application
    app_name: str = "Clinical Trial Matcher"
    debug: bool = False
    
    # Database components
    db_host: str = "localhost"
    db_port: int = 3306
    db_name: str = "trialmatch"
    db_user: str = "root"
    db_password: str = "password"
    # database_url: str = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    
    # AWS
    aws_region: str = "us-east-1"
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    s3_bucket_name: str = "trialmatch-documents"
    s3_region: str = "us-east-1"
    
    
    # Security
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440  # 24 hours
    
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)
    
    @computed_field
    @property
    def database_url(self) -> str:
        """Build database URL from individual components."""
        return f"mysql+pymysql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


settings = Settings()
