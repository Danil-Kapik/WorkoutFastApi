from sqlalchemy import select
from app.dao.base import BaseDAO
from app.models.models import ExerciseType, WorkoutSession


class WorkoutSessionsDAO(BaseDAO[WorkoutSession]):
    model = WorkoutSession

    async def list_by_user(
        self,
        user_id: int,
        limit: int,
        offset: int,
    ) -> list[WorkoutSession]:
        """Получить сессии пользователя в хронологическом порядке."""
        return await self.list(
            user_id=user_id,
            order_by=self.model.created_at.desc(),
            limit=limit,
            offset=offset,
        )

    async def list_by_user_and_exercise(
        self,
        user_id: int,
        exercise_type: ExerciseType,
        limit: int,
        offset: int,
    ) -> list[WorkoutSession]:
        """Получить сессии по определенному упражнению."""
        return await self.list(
            user_id=user_id,
            exercise_type=exercise_type,
            order_by=self.model.created_at.desc(),
            limit=limit,
            offset=offset,
        )

    async def get_last_session(
        self,
        user_id: int,
        exercise_type: ExerciseType | None = None,
    ) -> WorkoutSession | None:
        """Получить последнюю сессию тренировки."""
        filters = {"user_id": user_id}
        if exercise_type:
            filters["exercise_type"] = exercise_type
        return await self.find_one(
            **filters, order_by=self.model.created_at.desc()
        )

    async def get_by_id_and_user(
        self,
        session_id: int,
        user_id: int,
    ) -> WorkoutSession | None:
        """Получить сессию по ID и ID пользователя."""
        stmt = select(self.model).where(
            self.model.id == session_id,
            self.model.user_id == user_id,
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_session(self, **data) -> WorkoutSession:
        """Создать новую сессию тренировки."""
        return await self.create(**data)
