from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    All config lives here, read once from environment variables (.env in dev).
    Nothing else in the app should call os.environ directly — import `settings`
    instead, so there's exactly one place that knows where config comes from.
    """

    database_url: str
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7

    class Config:
        env_file = ".env"


settings = Settings()