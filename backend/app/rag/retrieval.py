from app.rag.embeddings import embed_text
from app.rag.vector_store import search


async def search_knowledge(query: str, top_k: int = 6, document_type: str | None = None) -> list[dict]:
    """
    Embeds a user's question, searches Pinecone, returns matching chunks
    with their source metadata. Applies a similarity threshold — weak
    matches are dropped rather than padded into a false-confident answer.
    """
    query_vector = await embed_text(query)

    filters = {}
    if document_type:
        filters["document_type"] = document_type

    results = await search(query_vector, top_k=top_k, filters=filters or None)

    MIN_SIMILARITY = 0.5

    chunks = []
    for match in results["matches"]:
        if match["score"] < MIN_SIMILARITY:
            continue
        chunks.append({
            "text": match["metadata"]["text"],
            "source_filename": match["metadata"]["source_filename"],
            "score": match["score"],
        })

    return chunks