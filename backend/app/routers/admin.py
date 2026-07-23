from fastapi import APIRouter, Depends, Query
from sqlmodel import select, func
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import get_session
from app.core.exceptions import NotFoundError
from app.core.pagination import PaginatedResponse
from app.dependencies.auth import require_staff
from app.models.consultation import AdoptionConsultation
from app.models.pet import Pet, PetCreate, PetRead
from app.models.product import Product, ProductCreate, ProductRead
from app.models.user import User

router = APIRouter(prefix="/admin", tags=["admin"], dependencies=[Depends(require_staff)])
# Every route below inherits this dependency automatically — there's no
# way to accidentally add a new /admin/* route later and forget the staff
# check, since it's enforced at the router level, not per-route.


@router.post("/products", response_model=ProductRead)
async def create_product(data: ProductCreate, session: AsyncSession = Depends(get_session)):
    """Creates a new product. Staff-only, enforced by the router-level dependency above."""
    product = Product(**data.model_dump())
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product


@router.patch("/products/{product_id}", response_model=ProductRead)
async def update_product(product_id: str, data: ProductCreate, session: AsyncSession = Depends(get_session)):
    """
    Overwrites every field of an existing product with the submitted data.
    A soft-deleted product 404s here too — same rule as every read
    endpoint: is_active=False means "doesn't exist" everywhere, editing
    included, since there's no way to reactivate one through this route.
    """
    product = await session.get(Product, product_id)
    if not product or not product.is_active:
        raise NotFoundError("Product not found")
    for field, value in data.model_dump().items():
        setattr(product, field, value)
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product


@router.delete("/products/{product_id}")
async def delete_product(product_id: str, session: AsyncSession = Depends(get_session)):
    """
    Soft-deletes a product: sets is_active=False instead of removing the
    row, so past OrderItem rows referencing it still resolve correctly.
    Hides it from every public listing/detail endpoint from then on.
    """
    product = await session.get(Product, product_id)
    if not product or not product.is_active:
        raise NotFoundError("Product not found")
    product.is_active = False
    session.add(product)
    await session.commit()
    return {"detail": "Deleted"}


@router.post("/pets", response_model=PetRead)
async def create_pet(data: PetCreate, session: AsyncSession = Depends(get_session)):
    """Creates a new pet listing."""
    pet = Pet(**data.model_dump())
    session.add(pet)
    await session.commit()
    await session.refresh(pet)
    return pet


@router.patch("/pets/{pet_id}", response_model=PetRead)
async def update_pet(pet_id: str, data: PetCreate, session: AsyncSession = Depends(get_session)):
    """
    Overwrites every field of an existing pet listing with the submitted
    data. A soft-deleted pet 404s here too — same rule as every read
    endpoint: is_active=False means "doesn't exist" everywhere, editing
    included, since there's no way to reactivate one through this route.
    """
    pet = await session.get(Pet, pet_id)
    if not pet or not pet.is_active:
        raise NotFoundError("Pet not found")
    for field, value in data.model_dump().items():
        setattr(pet, field, value)
    session.add(pet)
    await session.commit()
    await session.refresh(pet)
    return pet


@router.delete("/pets/{pet_id}")
async def delete_pet(pet_id: str, session: AsyncSession = Depends(get_session)):
    """
    Soft-deletes a pet listing: sets is_active=False instead of removing
    the row, so past AdoptionConsultation rows referencing it still
    resolve correctly. Hides it from every public listing/detail endpoint
    from then on.
    """
    pet = await session.get(Pet, pet_id)
    if not pet or not pet.is_active:
        raise NotFoundError("Pet not found")
    pet.is_active = False
    session.add(pet)
    await session.commit()
    return {"detail": "Deleted"}


@router.get("/adoption-consultations", response_model=PaginatedResponse[AdoptionConsultation])
async def list_all_consultations(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    session: AsyncSession = Depends(get_session),
):
    """
    Returns a page of consultation requests from every user, oldest first —
    "first booked, first shown," matching what you asked for when we
    scoped this page down to just two admin pages.
    """
    total = (await session.exec(select(func.count()).select_from(AdoptionConsultation))).one()
    result = await session.exec(
        select(AdoptionConsultation)
        .order_by(AdoptionConsultation.created_at.asc())
        .offset(offset)
        .limit(limit)
    )
    return PaginatedResponse(items=result.all(), total=total, limit=limit, offset=offset)