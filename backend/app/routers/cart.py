import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select, SQLModel, Field
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import get_session
from app.core.exceptions import NotFoundError
from app.dependencies.auth import get_current_user
from app.models.cart import CartItem
from app.models.product import Product
from app.models.user import User

router = APIRouter(prefix="/cart", tags=["cart"])


class CartItemCreate(SQLModel):
    """
    What POST /cart accepts. `quantity` is the amount to ADD to whatever's
    already in the cart, not the final total — see CartItemQuantityUpdate
    for setting an exact amount instead.
    """

    product_id: uuid.UUID
    quantity: int = Field(default=1, gt=0)


class CartItemQuantityUpdate(SQLModel):
    """What PATCH /cart/{product_id} accepts — sets the exact quantity, not an increment."""

    quantity: int = Field(gt=0)


class CartItemRead(SQLModel):
    """One cart line with the product's current details joined in, so the frontend never needs a second request to render the cart."""

    id: uuid.UUID
    product_id: uuid.UUID
    product_name: str
    unit_price: float
    stock_quantity: int
    image_url: str | None
    quantity: int


class CartResponse(SQLModel):
    """
    Every route below mutates the cart differently, but all of them end
    by returning this SAME shape — the full, current cart — so the
    frontend can just re-render from one response after any action
    instead of tracking deltas.
    """

    items: list[CartItemRead]
    subtotal: float


async def _build_cart_response(user_id: uuid.UUID, session: AsyncSession) -> CartResponse:
    result = await session.exec(
        select(CartItem, Product)
        .join(Product, CartItem.product_id == Product.id)
        .where(CartItem.user_id == user_id)
    )
    rows = result.all()

    items = [
        CartItemRead(
            id=item.id,
            product_id=item.product_id,
            product_name=product.name,
            unit_price=product.price,
            stock_quantity=product.stock_quantity,
            image_url=product.image_url,
            quantity=item.quantity,
        )
        for item, product in rows
    ]
    subtotal = sum(i.unit_price * i.quantity for i in items)
    return CartResponse(items=items, subtotal=subtotal)


@router.get("", response_model=CartResponse)
async def get_cart(user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return await _build_cart_response(user.id, session)


@router.post("", response_model=CartResponse)
async def add_to_cart(
    data: CartItemCreate,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    # Grabbed before commit() below — commit() expires every attribute on
    # `user`, so reading user.id afterward would trigger an implicit
    # reload that can't run in this async context (MissingGreenlet).
    user_id = user.id

    product = await session.get(Product, data.product_id)
    if not product or not product.is_active:
        raise NotFoundError("Product not found")

    result = await session.exec(
        select(CartItem).where(CartItem.user_id == user_id, CartItem.product_id == data.product_id)
    )
    existing = result.first()
    new_quantity = (existing.quantity if existing else 0) + data.quantity

    if new_quantity > product.stock_quantity:
        raise HTTPException(status_code=400, detail=f"Only {product.stock_quantity} of {product.name} in stock")

    if existing:
        existing.quantity = new_quantity
        session.add(existing)
    else:
        session.add(CartItem(user_id=user_id, product_id=data.product_id, quantity=new_quantity))

    await session.commit()
    return await _build_cart_response(user_id, session)


@router.patch("/{product_id}", response_model=CartResponse)
async def update_cart_item(
    product_id: uuid.UUID,
    data: CartItemQuantityUpdate,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    user_id = user.id
    result = await session.exec(
        select(CartItem).where(CartItem.user_id == user_id, CartItem.product_id == product_id)
    )
    item = result.first()
    if not item:
        raise NotFoundError("Item not in cart")

    product = await session.get(Product, product_id)
    if product and data.quantity > product.stock_quantity:
        raise HTTPException(status_code=400, detail=f"Only {product.stock_quantity} of {product.name} in stock")

    item.quantity = data.quantity
    session.add(item)
    await session.commit()
    return await _build_cart_response(user_id, session)


@router.delete("/{product_id}", response_model=CartResponse)
async def remove_from_cart(
    product_id: uuid.UUID,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    user_id = user.id
    result = await session.exec(
        select(CartItem).where(CartItem.user_id == user_id, CartItem.product_id == product_id)
    )
    item = result.first()
    if not item:
        raise NotFoundError("Item not in cart")

    await session.delete(item)
    await session.commit()
    return await _build_cart_response(user_id, session)


@router.delete("", response_model=CartResponse)
async def clear_cart(user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    user_id = user.id
    result = await session.exec(select(CartItem).where(CartItem.user_id == user_id))
    for item in result.all():
        await session.delete(item)
    await session.commit()
    return await _build_cart_response(user_id, session)
