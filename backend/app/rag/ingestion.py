import uuid

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import settings
from app.models.knowledge import KnowledgeDocument, KnowledgeDocumentVersion
from app.rag.extraction import extract_text
from app.rag.chunking import chunk_text
from app.rag.embeddings import embed_text
from app.rag.vector_store import upsert_chunks


async def ingest_document(
    filename: str,
    file_bytes: bytes,
    document_type: str,
    session: AsyncSession,
) -> KnowledgeDocumentVersion:
    """
    Full ingestion pipeline for one uploaded file:
      1. find or create the KnowledgeDocument row
      2. create a new version row (status=processing)
      3. extract text, chunk it, embed each chunk, store in Pinecone
      4. on success: mark version active, point document at it
      5. on failure: mark version failed, document keeps pointing at
         its last working version (if any)
    """
    result = await session.exec(
        select(KnowledgeDocument).where(KnowledgeDocument.filename == filename)
    )
    document = result.first()

    if not document:
        document = KnowledgeDocument(filename=filename, document_type=document_type)
        session.add(document)
        await session.flush()
        next_version_number = 1
    else:
        result = await session.exec(
            select(KnowledgeDocumentVersion).where(
                KnowledgeDocumentVersion.document_id == document.id
            )
        )
        existing_versions = result.all()
        next_version_number = max((v.version_number for v in existing_versions), default=0) + 1

    version = KnowledgeDocumentVersion(
        document_id=document.id,
        version_number=next_version_number,
        status="processing",
        embedding_model=settings.ollama_embedding_model,
    )
    session.add(version)
    await session.flush()

    try:
        text = extract_text(filename, file_bytes)
        chunks = chunk_text(text)

        records = []
        for i, chunk in enumerate(chunks):
            vector = embed_text(chunk)
            chunk_id = f"{version.id}:{i}"
            records.append({
                "id": chunk_id,
                "values": vector,
                "metadata": {
                    "text": chunk,
                    "document_type": document_type,
                    "document_version_id": str(version.id),
                    "source_filename": filename,
                },
            })

        upsert_chunks(records)

        version.status = "active"
        version.chunk_count = len(chunks)
        document.current_version_id = version.id

        session.add(version)
        session.add(document)
        await session.commit()
        await session.refresh(version)

        return version

    except Exception:
        version.status = "failed"
        session.add(version)
        await session.commit()
        raise