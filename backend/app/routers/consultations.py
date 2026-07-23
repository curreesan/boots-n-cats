from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import get_session
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