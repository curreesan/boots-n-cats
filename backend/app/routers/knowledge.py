from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import get_session
from app.dependencies.auth import require_staff
from app.models.knowledge import KnowledgeDocument, KnowledgeDocumentVersion
from app.rag.ingestion import ingest_document

router = APIRouter(prefix="/admin/knowledge", tags=["knowledge"], dependencies=[Depends(require_staff)])


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    document_type: str = Form(...),
    session: AsyncSession = Depends(get_session),
):
    """
    Accepts a file upload, runs it through the full ingestion pipeline,
    returns the resulting version's status. Staff-only.
    """
    file_bytes = await file.read()

    try:
        version = await ingest_document(
            filename=file.filename,
            file_bytes=file_bytes,
            document_type=document_type,
            session=session,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")

    return {
        "filename": file.filename,
        "status": version.status,
        "chunk_count": version.chunk_count,
    }


@router.get("")
async def list_documents(session: AsyncSession = Depends(get_session)):
    """Returns every knowledge document with its current version's status/chunk count."""
    result = await session.exec(select(KnowledgeDocument))
    documents = result.all()

    output = []
    for doc in documents:
        version = None
        if doc.current_version_id:
            version = await session.get(KnowledgeDocumentVersion, doc.current_version_id)

        output.append({
            "id": doc.id,
            "filename": doc.filename,
            "document_type": doc.document_type,
            "status": version.status if version else "no_version",
            "chunk_count": version.chunk_count if version else 0,
        })

    return output