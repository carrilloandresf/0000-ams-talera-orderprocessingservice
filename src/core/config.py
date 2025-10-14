from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "order-processing-service"
    app_env: str = "local"
    app_port: int = 8000

    mongo_host: str = "mongodb"
    mongo_port: int = 27017
    mongo_db: str = "orders_db"
    mongo_user: str = "root"
    mongo_password: str = "secret"
    mongo_auth_source: str = "admin"

    log_level: str = "INFO"

    class Config:
        env_file = ".env"

settings = Settings()