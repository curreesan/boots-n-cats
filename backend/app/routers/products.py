from fastapi import APIRouter, Depends, Query
from sqlmodel import select, func
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import get_session
from app.core.exceptions import NotFoundError
from app.core.pagination import PaginatedResponse
from app.models.product import Product, ProductRead

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=PaginatedResponse[ProductRead])
async def list_products(
    species: str | None = None,
    category: str | None = None,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    session: AsyncSession = Depends(get_session),
):
    """
    Returns a page of products, optionally filtered by species and/or
    category. `total` is the count of ALL matching rows (not just this
    page) so the frontend can render "page 2 of 5" style controls without
    a second request.
    """
    query = select(Product).where(Product.is_active)
    count_query = select(func.count()).select_from(Product).where(Product.is_active)
    if species:
        query = query.where(Product.species == species)
        count_query = count_query.where(Product.species == species)
    if category:
        query = query.where(Product.category == category)
        count_query = count_query.where(Product.category == category)

    total = (await session.exec(count_query)).one()
    result = await session.exec(query.offset(offset).limit(limit))

    return PaginatedResponse(
        items=result.all(),
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get("/{product_id}", response_model=ProductRead)
async def get_product(product_id: str, session: AsyncSession = Depends(get_session)):
    """
    Returns a single product by id, or a 404 if it doesn't exist.
    Powers the /products/:id detail page.
    """
    product = await session.get(Product, product_id)
    if not product or not product.is_active:
        raise NotFoundError("Product not found")
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