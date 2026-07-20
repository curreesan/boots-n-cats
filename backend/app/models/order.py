import uuid
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime


class Order(SQLModel, table=True):
    """
    The header — one row per checkout event. Holds what's true about the
    whole order once: who placed it, when, and the total. Doesn't know or
    care what was actually purchased — that's OrderItem's job.
    """

    __tablename__ = "orders"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    total_amount: float
    created_at: datetime = Field(
    default_factory=lambda: datetime.now(timezone.utc),
    sa_column=Column(DateTime(timezone=True), nullable=False),
)


class OrderItem(SQLModel, table=True):
    """
    The detail — one row per product within an order. Many OrderItem rows
    can point back to the same Order (that's the one-to-many relationship:
    one order, several purchased products).

    unit_price is a SNAPSHOT of the product's price at the moment of
    purchase, deliberately duplicated from products.price rather than
    looked up live. If the product's price changes next month, this order's
    history must still show what was actually paid — that's the whole
    reason this column exists instead of just joining to Product.price.
    """

    __tablename__ = "order_items"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    order_id: uuid.UUID = Field(foreign_key="orders.id", index=True)
    product_id: uuid.UUID = Field(foreign_key="products.id")
    quantity: int
    unit_price: float