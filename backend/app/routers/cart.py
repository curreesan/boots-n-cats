import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import get_session
from app.dependencies.auth import get_current_user
from app.models.cart import CartItem, CartItemCreate, CartItemUpdate
from app.models.user import User

router = APIRouter(prefix="/cart", tags=["cart"])


@router.get("")
async def get_cart(user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    """
    Returns the logged-in user's own cart items — never anyone else's.
    Note there's no cart_id in the URL or request; "whose cart" comes
    entirely from the auth cookie via get_current_user.
    """
    result = await session.exec(select(CartItem).where(CartItem.user_id == user.id))
    return result.all()


@router.post("/items")
async def add_item(
    data: CartItemCreate,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Adds a product to the logged-in user's cart. user_id comes from the
    authenticated user, not from `data` — CartItemCreate deliberately has
    no user_id field, so there's nothing for a client to fake here.
    """
    item = CartItem(user_id=user.id, product_id=data.product_id, quantity=data.quantity)
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item


@router.patch("/items/{item_id}")
async def update_item(
    item_id: uuid.UUID,
    data: CartItemUpdate,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Updates a cart item's quantity. Checks item.user_id == user.id before
    allowing the change — without this check, any logged-in user could
    edit ANY cart item just by guessing its id.
    """
    item = await session.get(CartItem, item_id)
    if not item or item.user_id != user.id:
        raise HTTPException(status_code=404, detail="Cart item not found")
    item.quantity = data.quantity
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item


@router.delete("/items/{item_id}")
async def remove_item(
    item_id: uuid.UUID,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Removes a cart item — same ownership check as update_item, for the
    same reason.
    """
    item = await session.get(CartItem, item_id)
    if not item or item.user_id != user.id:
        raise HTTPException(status_code=404, detail="Cart item not found")
    await session.delete(item)
    await session.commit()
    return {"detail": "Removed"}