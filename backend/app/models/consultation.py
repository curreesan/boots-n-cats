import uuid
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime

class AdoptionConsultationBase(SQLModel):
    """
    Fields shared between the table and what a client sends when creating
    one. Notice user_id, status, and contact are NOT here — contact is
    derived server-side from the logged-in user's account email rather
    than trusted from client input, since the chat agent proved
    unreliable about actually asking for it instead of inventing a
    placeholder. See AdoptionConsultationCreate below for the client shape.
    """

    pet_id: uuid.UUID = Field(foreign_key="pets.id")
    preferred_time: str  # free text — no calendar/slot logic for now


class AdoptionConsultation(AdoptionConsultationBase, table=True):
    """
    The actual Postgres table — is-a AdoptionConsultationBase, plus the
    fields that only make sense once a request actually exists.
    """

    __tablename__ = "adoption_consultations"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    contact: str  # snapshotted from the user's account email at request time

    # Unused today — the contacted/scheduled/completed workflow was
    # deliberately deferred (see earlier discussion), but adding this
    # column now costs nothing and saves a migration later if it comes back.
    status: str = Field(default="requested")

    created_at: datetime = Field(
    default_factory=lambda: datetime.now(timezone.utc),
    sa_column=Column(DateTime(timezone=True), nullable=False),
)


class AdoptionConsultationCreate(AdoptionConsultationBase):
    """
    What POST /adoption-consultations accepts from a client. Adds nothing
    beyond AdoptionConsultationBase — same reasoning as ProductCreate:
    the name documents "this is the create-shape" even where it's
    currently identical to the base.
    """

    pass