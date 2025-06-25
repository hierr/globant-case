from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Manages application settings and environment variables
    """

    # Database Settings
    DB_USER: str
    DB_PASS_SECRET: str
    DB_NAME: str
    INSTANCE_CONNECTION_NAME: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
