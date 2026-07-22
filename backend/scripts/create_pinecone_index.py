from pinecone import Pinecone, ServerlessSpec

from app.core.config import settings

pc = Pinecone(api_key=settings.pinecone_api_key)

existing = [index.name for index in pc.list_indexes()]

if settings.pinecone_index_name in existing:
    print(f"Index '{settings.pinecone_index_name}' already exists.")
else:
    pc.create_index(
        name=settings.pinecone_index_name,
        dimension=settings.embedding_dimension,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )
    print(f"Created index '{settings.pinecone_index_name}'.")