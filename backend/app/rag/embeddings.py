from openai import AsyncOpenAI

from app.core.config import settings

client = AsyncOpenAI(base_url=settings.ollama_base_url, api_key="ollama")  # Ollama ignores the key, but the client requires one


async def embed_text(text: str) -> list[float]:
    """
    Converts a single piece of text into a vector using the local
    nomic-embed-text model, via Ollama's OpenAI-compatible endpoint.

    Async (not a blocking call) so this network round-trip doesn't stall
    the whole event loop — every other in-flight request would otherwise
    freeze for however long Ollama takes to respond.
    """
    response = await client.embeddings.create(
        model=settings.ollama_embedding_model,
        input=text,
    )
    return response.data[0].embedding