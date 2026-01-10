from app.dao.progress_dao import UserProgressDAO
from app.schemas.user_progress import (
    UserProgressCreateSchema,
    UserProgressUpdateSchema,
)
from app.models.models import UserProgress
from fastapi import HTTPException, status


class UserProgressService:

    @staticmethod
    async def get_user_progress(user_id: int) -> list[UserProgress]:
        return await UserProgressDAO.get_by_user_id(user_id=user_id)

    @staticmethod
    async def create_progress(
        user_id: int,
        data: UserProgressCreateSchema,
    ) -> UserProgress:
        existing = await UserProgressDAO.find_one_or_none(
            user_id=user_id,
            exercise_type=data.exercise_type,
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Прогресс по этому упражнению уже существует",
            )

        return await UserProgressDAO.create(
            user_id=user_id,
            exercise_type=data.exercise_type,
            difficulty=data.difficulty,
            current_reps_per_set=data.current_reps_per_set,
        )

    @staticmethod
    async def update_progress(
        progress: UserProgress,
        data: UserProgressUpdateSchema,
    ) -> UserProgress:
        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(progress, field, value)

        # commit через DAO (доработаем позже)
        return progress
