from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    app_name: str = "Todo API"
    log_level: str = "info"
    database_url: str = "sqlite:///./todos.db" 

