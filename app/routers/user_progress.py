from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.services.user_progress_service import UserProgressService
from app.core.security import get_current_user
from app.models.models import User

router = APIRouter(prefix="/progress", tags=["Progress"])


async def get_progress_service(session: AsyncSession = Depends(get_session)):
    return UserProgressService(session)


@router.get("/")
async def get_user_progress(
    current_user: User = Depends(get_current_user),
    service: UserProgressService = Depends(get_progress_service),
):
    return await service.get_user_progress(user_id=current_user.id)
