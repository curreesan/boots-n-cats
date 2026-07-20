from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import get_session
from app.models.pet import Pet, PetRead

router = APIRouter(prefix="/pets", tags=["pets"])


@router.get("", response_model=list[PetRead])
async def list_pets(species: str | None = None, session: AsyncSession = Depends(get_session)):
    """
    Returns pets, optionally filtered by species. Powers the /pets
    listing page.
    """
    query = select(Pet)
    if species:
        query = query.where(Pet.species == species)
    result = await session.exec(query)
    return result.all()


@router.get("/{pet_id}", response_model=PetRead)
async def get_pet(pet_id: str, session: AsyncSession = Depends(get_session)):
    """
    Returns a single pet by id, or a 404 if it doesn't exist. Powers the
    /pets/:id profile page, where the "Request adoption consultation"
    button lives.
    """
    pet = await session.get(Pet, pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    return pet


@router.get("/breeds/all")
async def list_breeds(session: AsyncSession = Depends(get_session)):
    """
    Returns every distinct breed currently in use — powers a filter
    dropdown, same idea as list_categories in products.py.
    """
    result = await session.exec(select(Pet.breed).distinct())
    return result.all()