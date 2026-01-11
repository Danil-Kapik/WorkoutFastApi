from sqlalchemy.ext.asyncio import AsyncSession
from app.dao.progress_dao import UserProgressDAO
from app.schemas.user_progress import (
    UserProgressCreateSchema,
    UserProgressUpdateSchema,
)
from app.models.models import UserProgress
from fastapi import HTTPException, status


class UserProgressService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.dao = UserProgressDAO(session)

    async def get_user_progress(self, user_id: int) -> list[UserProgress]:
        return await self.dao.get_by_user_id(user_id=user_id)

    async def create_progress(
        self, user_id: int, data: UserProgressCreateSchema
    ) -> UserProgress:
        existing = await self.dao.find_one_or_none(
            user_id=user_id,
            exercise_type=data.exercise_type,
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Прогресс по этому упражнению уже существует",
            )

        new_progress = await self.dao.create(
            user_id=user_id, **data.model_dump()
        )
        await self.session.commit()
        return new_progress

    async def update_progress(
        self, progress: UserProgress, data: UserProgressUpdateSchema
    ) -> UserProgress:
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(progress, field, value)

        await self.session.commit()
        return progress
