import asyncio

from pinecone import Pinecone

from app.core.config import settings

pc = Pinecone(api_key=settings.pinecone_api_key)
index = pc.Index(settings.pinecone_index_name)

# The pinecone-client SDK is synchronous — every call below is wrapped in
# asyncio.to_thread so the network round-trip runs in a worker thread
# instead of blocking the event loop (and every other in-flight request)
# for the duration of the call.


async def upsert_chunks(chunk_records: list[dict]) -> None:
    """
    Writes chunks into Pinecone. Each record needs:
      id: str              — deterministic chunk id
      values: list[float]  — the embedding vector
      metadata: dict        — text + filters (document_type, document_version_id, etc.)
    "Upsert" = insert or update — if the id already exists, it's overwritten.
    """
    await asyncio.to_thread(index.upsert, vectors=chunk_records)


async def delete_chunks(chunk_ids: list[str]) -> None:
    """Deletes chunks by id — used when superseding an old document version."""
    await asyncio.to_thread(index.delete, ids=chunk_ids)


async def search(query_vector: list[float], top_k: int = 6, filters: dict | None = None):
    """
    Finds the top_k most similar vectors to query_vector, optionally
    restricted by metadata filters (e.g. document_type, species).
    Returns matches with their metadata and similarity score.
    """
    return await asyncio.to_thread(
        index.query,
        vector=query_vector,
        top_k=top_k,
        include_metadata=True,
        filter=filters,
    )