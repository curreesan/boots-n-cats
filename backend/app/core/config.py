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

    # Ollama (OpenAI-compatible local endpoint)
    ollama_base_url: str = "http://localhost:11434/v1"
    ollama_chat_model: str = "llama3.2"
    ollama_embedding_model: str = "nomic-embed-text"
    embedding_dimension: int = 768

    class Config:
        env_file = ".env"


settings = Settings()