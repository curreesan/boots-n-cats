import uuid
from sqlmodel import SQLModel, Field


class ProductBase(SQLModel):
    """
    Fields shared by every version of Product. Unlike User, there's no
    sensitive data here — the split exists for a different reason: what a
    client sends to CREATE a product shouldn't include an `id`, since the
    database generates that.
    """

    name: str
    species: str  # "dog" | "cat"
    category: str  # "toy" | "mat" | "bed" | "food"
    price: float
    stock_quantity: int
    image_url: str | None = None


class Product(ProductBase, table=True):
    """The actual Postgres table — is-a ProductBase, plus the id column."""

    __tablename__ = "products"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


class ProductCreate(ProductBase):
    """
    What POST /admin/products accepts. Adds nothing on top of ProductBase —
    it exists as its own class anyway so the API's "shape for creating a
    product" is explicitly named and separate from "shape stored in the DB,"
    even though today they only differ by the missing `id`.
    """

    pass


class ProductRead(ProductBase):
    """What GET /products and GET /products/:id return to a client."""

    id: uuid.UUID