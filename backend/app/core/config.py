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
    access_token_expire_minutes: int = 360
    refresh_token_expire_days: int = 7

     # Pinecone
    pinecone_api_key: str
    pinecone_index_name: str = "boots-and-cats-knowledge"

    # Pinecone index dimension — must match whatever embedding model wrote
    # to it (currently Cloudflare's bge-base-en-v1.5, also 768-dim).
    embedding_dimension: int = 768

    # Cloudflare Workers AI (OpenAI-compatible endpoint) — chat + embedding models
    cloudflare_account_id: str = ""
    cloudflare_api_token: str = ""
    cloudflare_chat_model: str = "@cf/ibm-granite/granite-4.0-h-micro"
    cloudflare_embedding_model: str = "@cf/baai/bge-base-en-v1.5"

    @property
    def cloudflare_base_url(self) -> str:
        return f"https://api.cloudflare.com/client/v4/accounts/{self.cloudflare_account_id}/ai/v1"

    # Supabase Storage (product/pet images)
    supabase_url: str
    supabase_service_key: str
    supabase_storage_bucket: str = "images"

    # The deployed frontend's origin, for CORS. Falls back to Vite's local
    # dev server address so nothing breaks if it's left unset in dev.
    frontend_url: str = "http://localhost:5173"

    # "development" (default, plain http locally) or "production" (served
    # over https) — gates cookie `secure`, since that flag would otherwise
    # block cookies entirely on a local http:// dev server.
    environment: str = "development"

    @property
    def is_production(self) -> bool:
        return self.environment == "production"

    class Config:
        env_file = ".env"


settings = Settings()