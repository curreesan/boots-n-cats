from openai import AsyncOpenAI

from app.core.config import settings

client = AsyncOpenAI(base_url=settings.cloudflare_base_url, api_key=settings.cloudflare_api_token)


async def embed_text(text: str) -> list[float]:
    """
    Converts a single piece of text into a vector using Cloudflare
    Workers AI's bge-base-en-v1.5 model, via its OpenAI-compatible
    endpoint. Same 768 dimensions as the old nomic-embed-text model, so
    the Pinecone index didn't need to be recreated — only re-ingested,
    since vector values differ between models even at the same dimension.

    Async (not a blocking call) so this network round-trip doesn't stall
    the whole event loop — every other in-flight request would otherwise
    freeze for however long the call takes to respond.
    """
    response = await client.embeddings.create(
        model=settings.cloudflare_embedding_model,
        input=text,
    )
    return response.data[0].embedding