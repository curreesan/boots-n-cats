from openai import OpenAI

from app.core.config import settings

client = OpenAI(base_url=settings.ollama_base_url, api_key="ollama")  # Ollama ignores the key, but the client requires one


def embed_text(text: str) -> list[float]:
    """
    Converts a single piece of text into a vector using the local
    nomic-embed-text model, via Ollama's OpenAI-compatible endpoint.
    """
    response = client.embeddings.create(
        model=settings.ollama_embedding_model,
        input=text,
    )
    return response.data[0].embedding