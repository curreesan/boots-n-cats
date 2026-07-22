import uuid
from datetime import datetime, timezone

from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime


class KnowledgeDocument(SQLModel, table=True):
    """One row per uploaded document, e.g. 'adoption-policy.pdf'."""

    __tablename__ = "knowledge_documents"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    filename: str
    document_type: str  # "adoption_policy" | "care_guide" | "faq" | etc.
    current_version_id: uuid.UUID | None = Field(default=None)  # no FK — breaks circular reference
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )


class KnowledgeDocumentVersion(SQLModel, table=True):
    """
    One row per ingestion attempt. status tracks the pipeline stage;
    chunk_count lets us reconstruct exact Pinecone chunk IDs later for
    deletion/supersession, per the doc's deterministic-ID approach.
    """

    __tablename__ = "knowledge_document_versions"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    document_id: uuid.UUID = Field(foreign_key="knowledge_documents.id", index=True)
    version_number: int
    status: str = Field(default="pending")  # pending | processing | active | failed
    chunk_count: int = Field(default=0)
    embedding_model: str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )