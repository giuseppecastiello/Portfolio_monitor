from os.path import join, dirname, abspath
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

current_dir = dirname(abspath(__file__))
env_file = join(current_dir, '..', ".env")

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=env_file, env_file_encoding='utf-8')
    # APP settings
    app_name: str
    app_version: str
    app_description: str
    # Database settings
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: SecretStr

settings = Settings()
