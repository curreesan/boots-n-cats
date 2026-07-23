from fastapi import APIRouter, Depends, Query
from sqlmodel import select, func
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import get_session
from app.core.pagination import PaginatedResponse
from app.dependencies.auth import get_current_user
from app.models.consultation import AdoptionConsultation, AdoptionConsultationCreate
from app.models.user import User

router = APIRouter(prefix="/adoption-consultations", tags=["adoption"])


@router.post("")
async def create_consultation(
    data: AdoptionConsultationCreate,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Creates a consultation request for a pet. Same pattern as cart's
    add_item: user_id comes from get_current_user, never from `data` —
    AdoptionConsultationCreate has no user_id field, so a client can't
    file a request pretending to be someone else. contact is likewise
    taken from the user's own account email, not accepted from the
    client, for the same reason.
    """
    consultation = AdoptionConsultation(
        user_id=user.id,
        pet_id=data.pet_id,
        contact=user.email,
        preferred_time=data.preferred_time,
    )
    session.add(consultation)
    await session.commit()
    await session.refresh(consultation)
    return consultation


@router.get("", response_model=PaginatedResponse[AdoptionConsultation])
async def list_own_consultations(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Returns a page of only the logged-in user's own consultation requests —
    powers the "your requests" section of /account. Deliberately does NOT
    return everyone's requests; that's what /admin/adoption-consultations
    (next file) is for, and it requires staff. Same pagination shape as
    every other list endpoint.
    """
    total = (
        await session.exec(
            select(func.count()).select_from(AdoptionConsultation).where(AdoptionConsultation.user_id == user.id)
        )
    ).one()
    result = await session.exec(
        select(AdoptionConsultation)
        .where(AdoptionConsultation.user_id == user.id)
        .order_by(AdoptionConsultation.created_at.desc())
        .offset(offset)
        .limit(limit)
    )
    return PaginatedResponse(items=result.all(), total=total, limit=limit, offset=offset)