from pydantic import PostgresDsn
from pydantic import BaseSettings


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "tron_info_db"
    TRON_NETWORK: str = "shasta"  # или "mainnet" для основной сети
    TRON_NETWORK_URL: str = "https://api.shasta.trongrid.io"
    @property
    def database_url(self) -> str:
        return f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    @property
    def tron_network(self):
        return "shasta" if "shasta" in self.TRON_NETWORK_URL else "mainnet"
    class Config:
        env_file = ".env"


settings = Settings()