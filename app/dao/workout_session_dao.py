from app.dao.base import BaseDAO
from app.models.models import ExerciseType, WorkoutSession


class WorkoutSessionsDAO(BaseDAO[WorkoutSession]):
    model = WorkoutSession

    async def list_by_user(
        self,
        user_id: int,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[WorkoutSession]:
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
    ) -> list[WorkoutSession]:
        return await self.list(
            user_id=user_id,
            exercise_type=exercise_type,
            order_by=self.model.created_at.desc(),
        )

    async def get_last_session(
        self,
        user_id: int,
        exercise_type: ExerciseType | None = None,
    ) -> WorkoutSession | None:
        filters = {"user_id": user_id}
        if exercise_type:
            filters["exercise_type"] = exercise_type

        res = await self.list(
            **filters, order_by=self.model.created_at.desc(), limit=1
        )
        return res[0] if res else None

    async def create_session(self, **data) -> WorkoutSession:
        return await self.create(**data)
