from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import get_session
from app.models.product import Product, ProductRead

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=list[ProductRead])
async def list_products(
    species: str | None = None,
    category: str | None = None,
    session: AsyncSession = Depends(get_session),
):
    """
    Returns products, optionally filtered by species and/or category.
    Both filters are optional — passing neither returns everything.
    Called by both the public /products page AND reused by whatever
    admin catalog page you build, since reads don't need a role check.
    """
    query = select(Product)
    if species:
        query = query.where(Product.species == species)
    if category:
        query = query.where(Product.category == category)

    result = await session.exec(query)
    return result.all()


@router.get("/{product_id}", response_model=ProductRead)
async def get_product(product_id: str, session: AsyncSession = Depends(get_session)):
    """
    Returns a single product by id, or a 404 if it doesn't exist.
    Powers the /products/:id detail page.
    """
    product = await session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.get("/categories/all")
async def list_categories(session: AsyncSession = Depends(get_session)):
    """
    Returns every distinct category currently in use (e.g. "toy", "bed",
    "food") — powers the filter dropdown on the /products listing page,
    without hardcoding the category list anywhere in the frontend.
    """
    result = await session.exec(select(Product.category).distinct())
    return result.all()