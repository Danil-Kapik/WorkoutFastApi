from sqlalchemy.ext.asyncio import AsyncSession
import math
from app.dao.workout_session_dao import WorkoutSessionsDAO
from app.dao.progress_dao import UserProgressDAO
from app.models.models import (
    WorkoutSession,
    ExerciseType,
)


class WorkoutSessionService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.session_dao = WorkoutSessionsDAO(session)
        self.progress_dao = UserProgressDAO(session)

    async def get_user_sessions_paginated(
        self,
        user_id: int,
        page: int,
        size: int,
    ) -> dict:
        """Получить все сессии пользователя с разбиением на страницы."""
        total = await self.session_dao.count(user_id=user_id)
        pages = math.ceil(total / size) if total else 0

        if page > pages and pages != 0:
            page = pages

        offset = (page - 1) * size
        items = await self.session_dao.list_by_user(
            user_id=user_id,
            limit=size,
            offset=offset,
        )
        return {
            "items": items,
            "total": total,
            "page": page,
            "size": size,
            "pages": pages,
            "has_next": page < pages,
            "has_prev": page > 1,
        }

    async def get_sessions_by_exercise_paginated(
        self,
        user_id: int,
        exercise_type: ExerciseType,
        page: int,
        size: int,
    ) -> dict:
        """Получить сессии по упражнению с разбиением на страницы."""
        total = await self.session_dao.count(
            user_id=user_id,
            exercise_type=exercise_type,
        )
        pages = math.ceil(total / size) if total else 0

        if page > pages and pages != 0:
            page = pages
        offset = (page - 1) * size
        items = await self.session_dao.list_by_user_and_exercise(
            user_id=user_id,
            exercise_type=exercise_type,
            limit=size,
            offset=offset,
        )
        return {
            "items": items,
            "total": total,
            "page": page,
            "size": size,
            "pages": pages,
            "has_next": page < pages,
            "has_prev": page > 1,
        }

    async def get_last_session(
        self,
        user_id: int,
        exercise_type: ExerciseType | None = None,
    ) -> WorkoutSession | None:
        """Получить последнюю сессию пользователя"""
        session = await self.session_dao.get_last_session(
            user_id=user_id,
            exercise_type=exercise_type,
        )
        return session

    async def start_session(
        self,
        user_id: int,
        exercise_type: ExerciseType,
    ) -> WorkoutSession:
        """Начать сессию тренировки для уровня текущего прогресса."""
        progress = await self.progress_dao.get_by_user_and_exercise(
            user_id=user_id,
            exercise_type=exercise_type,
        )
        if not progress:
            raise ValueError(
                f"Тренировка для упражнения {exercise_type} не найден"
            )
        workout_session = await self.session_dao.create(
            user_id=user_id,
            exercise_type=exercise_type,
            difficulty=progress.difficulty,
            reps_per_set_at_start=progress.current_reps_per_set,
        )
        await self.session.commit()
        return workout_session

    async def finish_session(
        self,
        session_id: int,
        user_id: int,
        completed: bool,
        notes: str | None = None,
    ) -> WorkoutSession:
        """Завершить сессию и обновить прогресс."""
        session = await self.session_dao.get_by_id_and_user(
            session_id, user_id
        )
        if not session:
            raise ValueError("Сессия не найдена")

        session.completed = completed
        session.notes = notes

        if completed:
            progress = await self.progress_dao.get_by_user_and_exercise(
                user_id, session.exercise_type
            )
            progress.up_level()
            progress.try_upgrade_difficulty()

        await self.session.commit()
        await self.session.refresh(session)
        return session
