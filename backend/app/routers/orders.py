import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select, SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import get_session
from app.dependencies.auth import get_current_user
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.models.user import User

router = APIRouter(prefix="/orders", tags=["orders"])


class OrderItemRequest(SQLModel):
    """What the client sends per line when checking out — no DB table backs this."""
    product_id: uuid.UUID
    quantity: int


@router.post("")
async def checkout(
    items: list[OrderItemRequest],
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Checkout takes the cart directly from the client — validates stock,
    creates the order, decrements stock. No cart_items table involved.
    """
    if not items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total = 0.0
    order = Order(user_id=user.id, total_amount=0)
    session.add(order)
    await session.flush()

    for line in items:
        product = await session.get(Product, line.product_id)
        if not product or product.stock_quantity < line.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock for {product.name if product else line.product_id}",
            )

        total += product.price * line.quantity

        session.add(OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=line.quantity,
            unit_price=product.price,
        ))
        product.stock_quantity -= line.quantity
        session.add(product)

    order.total_amount = total
    session.add(order)
    await session.commit()
    await session.refresh(order)
    return order


@router.get("")
async def list_orders(user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    result = await session.exec(select(Order).where(Order.user_id == user.id))
    return result.all()


@router.get("/{order_id}")
async def get_order(
    order_id: uuid.UUID,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    order = await session.get(Order, order_id)
    if not order or order.user_id != user.id:
        raise HTTPException(status_code=404, detail="Order not found")

    result = await session.exec(
        select(OrderItem, Product)
        .join(Product, OrderItem.product_id == Product.id)
        .where(OrderItem.order_id == order.id)
    )
    rows = result.all()

    items = [
        {
            "id": item.id,
            "product_id": item.product_id,
            "product_name": product.name,
            "quantity": item.quantity,
            "unit_price": item.unit_price,
        }
        for item, product in rows
    ]

    return {"order": order, "items": items}