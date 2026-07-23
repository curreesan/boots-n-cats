import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import update
from sqlmodel import select, func
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import get_session
from app.core.exceptions import NotFoundError
from app.core.pagination import PaginatedResponse
from app.dependencies.auth import get_current_user
from app.models.cart import CartItem
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.models.user import User

router = APIRouter(prefix="/orders", tags=["orders"])


async def perform_checkout(user_id: uuid.UUID, session: AsyncSession) -> Order:
    """
    Checks out whatever is currently in the user's persisted cart — no
    client-supplied item list, so a tampered request body can't claim
    different products/quantities than what's actually in the cart.
    Validates stock, creates the order, decrements stock, then clears the
    cart, all in one transaction: nothing commits until the very end (see
    get_session's docstring), so a failure partway through leaves both
    the order and the cart untouched.

    Factored out of the POST /orders route so the chat agent's checkout
    tool can call the exact same logic directly — never duplicate this,
    since it's the one place stock decrement + order creation atomicity
    is guaranteed.
    """
    cart_result = await session.exec(select(CartItem).where(CartItem.user_id == user_id))
    cart_items = cart_result.all()
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total = 0.0
    order = Order(user_id=user_id, total_amount=0)
    session.add(order)
    await session.flush()

    for line in cart_items:
        # Atomic check-and-decrement: stock_quantity >= line.quantity and
        # is_active are checked in the same UPDATE that decrements stock,
        # so two checkouts racing on the same product can't both pass a
        # separate read-then-write check, and a product soft-deleted while
        # sitting in someone's cart can't be checked out either.
        stmt = (
            update(Product)
            .where(Product.id == line.product_id, Product.is_active, Product.stock_quantity >= line.quantity)
            .values(stock_quantity=Product.stock_quantity - line.quantity)
            .returning(Product.price)
        )
        result = await session.exec(stmt)
        row = result.first()

        if row is None:
            product = await session.get(Product, line.product_id)
            name = product.name if product else str(line.product_id)
            raise HTTPException(status_code=400, detail=f"Insufficient stock for {name}")

        unit_price = row[0]
        total += unit_price * line.quantity

        session.add(OrderItem(
            order_id=order.id,
            product_id=line.product_id,
            quantity=line.quantity,
            unit_price=unit_price,
        ))
        await session.delete(line)

    order.total_amount = total
    session.add(order)
    await session.commit()
    await session.refresh(order)
    return order


@router.post("")
async def checkout(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    return await perform_checkout(user.id, session)


@router.get("", response_model=PaginatedResponse[Order])
async def list_orders(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    total = (
        await session.exec(select(func.count()).select_from(Order).where(Order.user_id == user.id))
    ).one()
    result = await session.exec(
        select(Order).where(Order.user_id == user.id).order_by(Order.created_at.desc()).offset(offset).limit(limit)
    )
    return PaginatedResponse(items=result.all(), total=total, limit=limit, offset=offset)


@router.get("/{order_id}")
async def get_order(
    order_id: uuid.UUID,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    order = await session.get(Order, order_id)
    if not order or order.user_id != user.id:
        raise NotFoundError("Order not found")

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