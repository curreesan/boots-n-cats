from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import get_session
from app.dependencies.auth import require_staff
from app.models.consultation import AdoptionConsultation
from app.models.pet import Pet, PetCreate
from app.models.product import Product, ProductCreate
from app.models.user import User

router = APIRouter(prefix="/admin", tags=["admin"], dependencies=[Depends(require_staff)])
# Every route below inherits this dependency automatically — there's no
# way to accidentally add a new /admin/* route later and forget the staff
# check, since it's enforced at the router level, not per-route.


@router.post("/products")
async def create_product(data: ProductCreate, session: AsyncSession = Depends(get_session)):
    """Creates a new product. Staff-only, enforced by the router-level dependency above."""
    product = Product(**data.model_dump())
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product


@router.patch("/products/{product_id}")
async def update_product(product_id: str, data: ProductCreate, session: AsyncSession = Depends(get_session)):
    """Overwrites every field of an existing product with the submitted data."""
    product = await session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    for field, value in data.model_dump().items():
        setattr(product, field, value)
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product


@router.delete("/products/{product_id}")
async def delete_product(product_id: str, session: AsyncSession = Depends(get_session)):
    """Permanently removes a product from the catalog."""
    product = await session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    await session.delete(product)
    await session.commit()
    return {"detail": "Deleted"}


@router.post("/pets")
async def create_pet(data: PetCreate, session: AsyncSession = Depends(get_session)):
    """Creates a new pet listing."""
    pet = Pet(**data.model_dump())
    session.add(pet)
    await session.commit()
    await session.refresh(pet)
    return pet


@router.patch("/pets/{pet_id}")
async def update_pet(pet_id: str, data: PetCreate, session: AsyncSession = Depends(get_session)):
    """Overwrites every field of an existing pet listing with the submitted data."""
    pet = await session.get(Pet, pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    for field, value in data.model_dump().items():
        setattr(pet, field, value)
    session.add(pet)
    await session.commit()
    await session.refresh(pet)
    return pet


@router.delete("/pets/{pet_id}")
async def delete_pet(pet_id: str, session: AsyncSession = Depends(get_session)):
    """Permanently removes a pet listing."""
    pet = await session.get(Pet, pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    await session.delete(pet)
    await session.commit()
    return {"detail": "Deleted"}


@router.get("/adoption-consultations")
async def list_all_consultations(session: AsyncSession = Depends(get_session)):
    """
    Returns every consultation request from every user, oldest first —
    "first booked, first shown," matching what you asked for when we
    scoped this page down to just two admin pages.
    """
    result = await session.exec(
        select(AdoptionConsultation).order_by(AdoptionConsultation.created_at.asc())
    )
    return result.all()