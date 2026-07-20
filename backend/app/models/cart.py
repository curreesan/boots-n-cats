import uuid
from sqlmodel import SQLModel, Field


class CartItem(SQLModel, table=True):
    """
    The actual Postgres table. No separate CartBase this time — unlike
    User/Product/Pet, a cart item has no sensitive fields to hide AND no
    fields the DB adds that a client shouldn't send except the id itself,
    so there's nothing meaningful to split into a shared parent yet.

    One row per (user, product) pair — quantity tracks how many of that
    product are in the cart. No separate `carts` table (see the earlier
    schema discussion for why).
    """

    __tablename__ = "cart_items"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    product_id: uuid.UUID = Field(foreign_key="products.id")
    quantity: int = Field(default=1)


class CartItemCreate(SQLModel):
    """
    What POST /cart/items accepts. Deliberately does NOT include user_id —
    the logged-in user comes from their auth cookie (via get_current_user
    in the route), never from something the client types into a request
    body. Letting a client specify whose cart to add to would be a
    security hole — anyone could add items to someone else's cart.
    """

    product_id: uuid.UUID
    quantity: int = 1


class CartItemUpdate(SQLModel):
    """What PATCH /cart/items/:id accepts — just a new quantity."""

    quantity: int