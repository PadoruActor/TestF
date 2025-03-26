"""
Configuration settings for Tron Address Info API.

Uses pydantic's BaseSettings for environment variable management.
"""

from pydantic import PostgresDsn
from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    Application settings.

    Loads from environment variables with .env file support.
    """
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "tron_info_db"
    TRON_NETWORK: str = "shasta"  # or "mainnet"
    TRON_NETWORK_URL: str = "https://api.shasta.trongrid.io"

    @property
    def database_url(self) -> PostgresDsn:
        """Construct PostgreSQL connection URL."""
        return f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def tron_network(self) -> str:
        """Determine network type from URL."""
        return "shasta" if "shasta" in self.TRON_NETWORK_URL else "mainnet"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()