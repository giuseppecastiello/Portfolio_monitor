import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

current_dir = os.path.dirname(os.path.abspath(__file__))
env_file = os.path.join(current_dir, '..', ".env")

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=env_file, env_file_encoding='utf-8')
    # APP settings
    app_name: str = "Portfolio Monitor API"
    app_version: str = "0.1.0"
    app_description: str = "API for monitoring portfolio performance"
    # Database settings
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "db"
    db_user: str = "user"
    db_password: SecretStr = "password"

