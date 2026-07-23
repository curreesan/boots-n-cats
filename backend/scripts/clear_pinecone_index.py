"""
One-off: wipes every vector from the Pinecone index. Needed when switching
embedding models (nomic-embed-text -> Cloudflare bge-base-en-v1.5) — old
vectors were embedded with a different model, so even at the same 768
dimensions they aren't comparable to new query vectors. Re-upload
documents through Admin > Knowledge afterward to repopulate.

Run once: python -m scripts.clear_pinecone_index
"""
from app.rag.vector_store import index


def main():
    stats = index.describe_index_stats()
    count = stats.get("total_vector_count", 0)
    print(f"Deleting all {count} vectors from the index...")
    index.delete(delete_all=True)
    print("Done.")


if __name__ == "__main__":
    main()
