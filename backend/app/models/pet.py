import uuid
from sqlmodel import SQLModel, Field


class PetBase(SQLModel):
    """
    Fields shared across every version of Pet. Same reasoning as
    ProductBase — no sensitive data here, the split exists mainly so
    "what the DB stores" and "what a client sends when creating one"
    stay separate, even though today they're nearly identical.
    """

    name: str
    species: str  # "dog" | "cat"
    breed: str
    description: str
    image_url: str | None = None


class Pet(PetBase, table=True):
    """The actual Postgres table — is-a PetBase, plus the id column."""

    __tablename__ = "pets"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


class PetCreate(PetBase):
    """What POST /admin/pets accepts — no id, the DB generates that."""

    pass


class PetRead(PetBase):
    """What GET /pets and GET /pets/:id return to a client."""

    id: uuid.UUID