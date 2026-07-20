import uuid
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime


class UserBase(SQLModel):
    """
    Fields shared by every "flavor" of User below. Not a database table by
    itself (no table=True) — just the common shape that Create, Read, and
    the actual table class all inherit from, so we don't repeat these two
    fields three times.
    """

    email: str = Field(unique=True, index=True)
    name: str


class User(UserBase, table=True):
    """
    The actual Postgres table. This is what gets stored, and it's the only
    one of the four classes that should ever touch the database directly.
    Never return this object straight from an API route — password_hash
    has no business leaving the server, ever.
    """

    __tablename__ = "users"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    password_hash: str
    role: str = Field(default="customer")  # "customer" | "staff"
    created_at: datetime = Field(
    default_factory=lambda: datetime.now(timezone.utc),
    sa_column=Column(DateTime(timezone=True), nullable=False),
)


class UserCreate(UserBase):
    """
    What POST /auth/register is allowed to accept from a client. Notice
    this has `password`, not `password_hash` — the plain password is only
    ever allowed to exist in memory for the brief moment between the
    client sending it and us calling hash_password() on it.
    """

    password: str


class UserRead(UserBase):
    """
    What GET /auth/me (and anywhere else a user gets returned) is allowed
    to send back to a client. Deliberately excludes password_hash — this
    class defines the "safe to expose" shape of a user.
    """

    id: uuid.UUID
    role: str