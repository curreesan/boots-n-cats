import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import get_session
from app.dependencies.auth import get_current_user
from app.models.cart import CartItem
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.models.user import User

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("")
async def checkout(user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    """
    This IS the "checkout" action — triggered from the /cart page, not a
    separate route (remember the earlier decision to combine cart +
    checkout into one page). For every item currently in the user's cart:
      1. checks the product still has enough stock
      2. copies it into a new OrderItem, snapshotting today's price
      3. decrements the product's stock
      4. removes the item from the cart
    Then totals everything up into one Order header row.
    """
    result = await session.exec(select(CartItem).where(CartItem.user_id == user.id))
    cart_items = result.all()
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total = 0.0
    order = Order(user_id=user.id, total_amount=0)
    session.add(order)
    await session.flush()  # assigns order.id without fully committing yet

    for item in cart_items:
        product = await session.get(Product, item.product_id)
        if not product or product.stock_quantity < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock for {product.name if product else item.product_id}",
            )

        line_total = product.price * item.quantity
        total += line_total

        session.add(OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=item.quantity,
            unit_price=product.price,  # snapshot — see order.py's docstring
        ))
        product.stock_quantity -= item.quantity
        session.add(product)
        await session.delete(item)

    order.total_amount = total
    session.add(order)
    await session.commit()
    await session.refresh(order)
    return order


@router.get("")
async def list_orders(user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    """Returns the logged-in user's own order history — powers /orders."""
    result = await session.exec(select(Order).where(Order.user_id == user.id))
    return result.all()


@router.get("/{order_id}")
async def get_order(
    order_id: uuid.UUID,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Returns one order plus its line items — powers /orders/:id. Same
    ownership check as cart.py's update/remove: order.user_id != user.id
    means "not yours," treated identically to "doesn't exist."
    """
    order = await session.get(Order, order_id)
    if not order or order.user_id != user.id:
        raise HTTPException(status_code=404, detail="Order not found")

    items_result = await session.exec(select(OrderItem).where(OrderItem.order_id == order.id))
    return {"order": order, "items": items_result.all()}