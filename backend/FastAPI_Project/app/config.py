from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mongodb_uri: str = "mongodb://mongo:gvIXvVistiZoXBdOeLXLcJaZLDoWMsFu@autorack.proxy.rlwy.net:32955"
    mongodb_db: str = "mydatabase"

    class Config:
        env_file = ".env"

settings = Settings()
