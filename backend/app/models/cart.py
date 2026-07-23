import uuid

from sqlmodel import SQLModel, Field, UniqueConstraint


class CartItem(SQLModel, table=True):
    """
    One row per (user, product) combination — quantity holds however many
    of that product are currently in the cart. Tied to user_id (not
    browser state), so it persists across logout/login, unlike the old
    frontend-only cart.

    The unique constraint means "add to cart" is an upsert: adding a
    product already in the cart increments its existing row's quantity
    instead of creating a duplicate line.
    """

    __tablename__ = "cart_items"
    __table_args__ = (UniqueConstraint("user_id", "product_id", name="uq_cart_items_user_product"),)

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    product_id: uuid.UUID = Field(foreign_key="products.id")
    quantity: int = Field(gt=0)
