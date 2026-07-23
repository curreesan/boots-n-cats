from fastapi import APIRouter, Depends, Query
from sqlmodel import select, func
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import get_session
from app.core.exceptions import NotFoundError
from app.core.pagination import PaginatedResponse
from app.models.pet import Pet, PetRead

router = APIRouter(prefix="/pets", tags=["pets"])


@router.get("", response_model=PaginatedResponse[PetRead])
async def list_pets(
    species: str | None = None,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    session: AsyncSession = Depends(get_session),
):
    """
    Returns a page of pets, optionally filtered by species. `total` is the
    count of ALL matching rows (not just this page), same pagination shape
    as /products.
    """
    query = select(Pet).where(Pet.is_active)
    count_query = select(func.count()).select_from(Pet).where(Pet.is_active)
    if species:
        query = query.where(Pet.species == species)
        count_query = count_query.where(Pet.species == species)

    total = (await session.exec(count_query)).one()
    result = await session.exec(query.offset(offset).limit(limit))

    return PaginatedResponse(
        items=result.all(),
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get("/{pet_id}", response_model=PetRead)
async def get_pet(pet_id: str, session: AsyncSession = Depends(get_session)):
    """
    Returns a single pet by id, or a 404 if it doesn't exist. Powers the
    /pets/:id profile page, where the "Request adoption consultation"
    button lives.
    """
    pet = await session.get(Pet, pet_id)
    if not pet or not pet.is_active:
        raise NotFoundError("Pet not found")
    return pet