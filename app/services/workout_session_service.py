from sqlalchemy.ext.asyncio import AsyncSession
import math
from app.dao.workout_session_dao import WorkoutSessionsDAO
from app.dao.progress_dao import UserProgressDAO
from app.models.models import (
    WorkoutSession,
    UserProgress,
    ExerciseType,
    Difficulty,
)


class WorkoutSessionService:
    def __init__(self, session: AsyncSession):
        self.session_dao = WorkoutSessionsDAO(session)
        self.progress_dao = UserProgressDAO(session)

    async def get_user_sessions_paginated(
        self,
        user_id: int,
        page: int,
        size: int,
    ) -> dict:
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

    async def create_progress_and_session(
        self,
        user_id: int,
        exercise_type: ExerciseType,
        reps: int,
    ) -> tuple[UserProgress, WorkoutSession]:
        """
        Создаёт (при необходимости) прогресс пользователя
        и стартовую тренировочную сессию.
        """
        difficulty = Difficulty.from_reps(reps)

        progress = await self.progress_dao.get_by_user_and_exercise(
            user_id=user_id,
            exercise_type=exercise_type,
        )
        if not progress:
            progress = await self.progress_dao.create(
                user_id=user_id,
                exercise_type=exercise_type,
                difficulty=difficulty,
                current_reps_per_set=reps,
            )
        workout_session = await self.session_dao.create(
            user_id=user_id,
            exercise_type=exercise_type,
            difficulty=progress.difficulty,
            reps_per_set_at_start=progress.current_reps_per_set,
            completed=False,
        )
        return progress, workout_session

    async def complete_workout_session_and_update_progress(
        self,
        session_id: int,
        completed: bool,
        notes: str | None = None,
    ) -> tuple[WorkoutSession, UserProgress | None]:
        """
        Завершает тренировочную сессию
        и при необходимости обновляет прогресс.
        """
        workout_session = await self.session_dao.get_by_id(session_id)
        if not workout_session:
            raise ValueError(
                f"Тренировочная сессия с ID {session_id} не найдена"
            )
        workout_session.completed = completed

        if notes is not None:
            workout_session.notes = notes
        progress: UserProgress | None = None

        if completed:
            progress = await self.progress_dao.get_by_user_and_exercise(
                user_id=workout_session.user_id,
                exercise_type=workout_session.exercise_type,
            )
            if progress:
                progress.up_level()
                if progress.try_upgrade_difficulty():
                    workout_session.notes = (
                        f"{workout_session.notes or ''}\n"
                        f"[Автоматический апгрейд до {progress.difficulty.value}]"
                    ).strip()
        return workout_session, progress

    async def update_session(
        self,
        session_id: int,
        completed: bool | None = None,
        notes: str | None = None,
    ) -> tuple[WorkoutSession, UserProgress | None]:
        """
        Обновляет тренировочную сессию
        и при необходимости прогресс пользователя.
        """
        return await self.complete_workout_session_and_update_progress(
            session_id=session_id,
            completed=bool(completed),
            notes=notes,
        )

    async def create_new_session_from_last(
        self,
        user_id: int,
        exercise_type: ExerciseType,
    ) -> WorkoutSession:
        """
        Оркестрирует создание новой тренировочной сессии на основе последней.
        """
        # Получаем последнюю сессию
        last_session = await self.session_dao.get_last_session(
            user_id=user_id,
            exercise_type=exercise_type,
        )

        if not last_session:
            raise ValueError(
                f"Нет ни одной сессии для пользователя {user_id} "
                f"по упражнению {exercise_type.value}"
            )

        # Получаем текущий прогресс
        progress = await self.progress_dao.get_by_user_and_exercise(
            user_id=user_id,
            exercise_type=exercise_type,
        )

        if not progress:
            raise ValueError(
                f"Прогресс не найден для пользователя {user_id} "
                f"по упражнению {exercise_type.value}"
            )

        # Создаём новую сессию с текущими параметрами
        new_session = await self.session_dao.create_session(
            user_id=user_id,
            exercise_type=exercise_type,
            difficulty=progress.difficulty,
            reps_per_set_at_start=progress.current_reps_per_set,
            completed=False,
        )
        return new_session
