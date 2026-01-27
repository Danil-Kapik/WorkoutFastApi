from sqlalchemy.ext.asyncio import AsyncSession
from app.dao.progress_dao import UserProgressDAO
from app.models.models import Difficulty, ExerciseType, UserProgress
from app.schemas.user_progress import UserProgressReadSchema


class UserProgressService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.dao = UserProgressDAO(session)

    async def get_user_progress(
        self, user_id: int
    ) -> list[UserProgressReadSchema]:
        progress = await self.dao.list_by_user_id(user_id=user_id)
        return [
            UserProgressReadSchema.model_validate(item) for item in progress
        ]

    async def get_progress_for_exercise(
        self,
        user_id: int,
        exercise_type: ExerciseType,
    ) -> UserProgressReadSchema | None:
        progress = await self.dao.get_by_user_and_exercise(
            user_id=user_id,
            exercise_type=exercise_type,
        )
        if progress:
            return UserProgressReadSchema.model_validate(progress)
        return None

    async def create_progress(
        self,
        user_id: int,
        exercise_type: ExerciseType,
        reps: int,
    ) -> UserProgress:
        difficulty = Difficulty.from_reps(reps)
        progress = await self.dao.create(
            user_id=user_id,
            exercise_type=exercise_type,
            difficulty=difficulty,
            current_reps_per_set=reps,
        )
        await self.session.commit()
        return progress
