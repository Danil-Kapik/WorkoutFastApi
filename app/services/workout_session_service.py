from sqlalchemy.ext.asyncio import AsyncSession
import math
from app.dao.workout_session_dao import WorkoutSessionsDAO
from app.schemas.workout_session import (
    PaginatedResponse,
    WorkoutSessionReadSchema,
    WorkoutSessionUpdateSchema,
)
from app.models.models import (
    WorkoutSession,
    UserProgress,
    ExerciseType,
    Difficulty,
)


class WorkoutSessionService:
    def __init__(self, session: AsyncSession):
        self.session_dao = WorkoutSessionsDAO(session)

    async def get_user_sessions_paginated(
        self,
        user_id: int,
        page: int,
        size: int,
    ) -> PaginatedResponse[WorkoutSessionReadSchema]:
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
        return PaginatedResponse[WorkoutSessionReadSchema](
            items=items,
            total=total,
            page=page,
            size=size,
            pages=pages,
            has_next=page < pages,
            has_prev=page > 1,
        )

    async def get_sessions_by_exercise(
        self,
        user_id: int,
        exercise_type: ExerciseType,
    ) -> list[WorkoutSession]:
        """Получить все сессии по конкретному упражнению"""
        return await self.session_dao.list_by_user_and_exercise(
            user_id=user_id,
            exercise_type=exercise_type,
        )

    async def get_last_session(
        self,
        user_id: int,
        exercise_type: ExerciseType | None = None,
    ) -> WorkoutSession | None:
        """Получить последнюю сессию пользователя"""
        return await self.session_dao.get_last_session(
            user_id=user_id,
            exercise_type=exercise_type,
        )

    async def create_progress_and_session(
        self,
        user_id: int,
        exercise_type: ExerciseType,
        reps: int,
    ) -> tuple[UserProgress, WorkoutSession]:
        """
        Оркестрирует создание прогресса пользователя и его первую тренировочную сессию.

        Процесс:
        1. Вычисляет уровень сложности на основе количества повторений
        2. Создаёт запись прогресса пользователя (если ещё не существует)
        3. Создаёт тренировочную сессию с начальными параметрами

        Args:
            user_id: ID пользователя
            exercise_type: Тип упражнения
            reps: Количество повторений (сложность вычисляется автоматически)

        Returns:
            Кортеж (UserProgress, WorkoutSession)
        """
        # Вычисляем сложность на основе количества повторений
        difficulty = Difficulty.from_reps(reps)

        # Проверяем, есть ли уже прогресс для этого упражнения
        existing_progress = await self.progress_dao.get_by_user_and_exercise(
            user_id=user_id,
            exercise_type=exercise_type,
        )

        if existing_progress:
            progress = existing_progress
        else:
            # Создаём новый прогресс
            progress = await self.progress_dao.create(
                user_id=user_id,
                exercise_type=exercise_type,
                difficulty=difficulty,
                current_reps_per_set=reps,
            )

        # Получаем стартовое количество повторений
        starting_reps = progress.current_reps_per_set

        # Создаём новую тренировочную сессию
        session = await self.session_dao.create_session(
            user_id=user_id,
            exercise_type=exercise_type,
            difficulty=progress.difficulty,
            reps_per_set_at_start=starting_reps,
            completed=False,
        )

        await self.session.flush()
        return progress, session

    async def complete_workout_session_and_update_progress(
        self,
        session_id: int,
        completed: bool,
        notes: str | None = None,
    ) -> tuple[WorkoutSession, UserProgress | None]:
        """
        Оркестрирует завершение тренировочной сессии
        и обновление прогресса пользователя.

        Если сессия успешно завершена:
        1. Обновляет статус сессии
        2. Увеличивает количество повторений в прогрессе
        3. Проверяет возможность повышения уровня сложности

        Args:
            session_id: ID тренировочной сессии
            completed: Успешно ли завершена сессия
            notes: Дополнительные заметки

        Returns:
            Кортеж (WorkoutSession, UserProgress) или (WorkoutSession, None)
        """
        # Получаем сессию
        session = await self.session_dao.get_by_id(session_id)
        if not session:
            raise ValueError(
                f"Тренировочная сессия с ID {session_id} не найдена"
            )

        # Обновляем статус сессии
        session.completed = completed
        if notes is not None:
            session.notes = notes

        progress = None

        # Если сессия успешно завершена, обновляем прогресс
        if completed:
            # Получаем текущий прогресс пользователя
            progress = await self.progress_dao.get_by_user_and_exercise(
                user_id=session.user_id,
                exercise_type=session.exercise_type,
            )

            if progress:
                # Увеличиваем количество повторений
                progress.up_level()

                # Проверяем возможность повышения уровня сложности
                upgraded = progress.try_upgrade_difficulty()
                if upgraded:
                    # Если произошёл апгрейд, логируем или добавляем заметку
                    session.notes = (
                        f"{session.notes or ''}\n[Автоматический апгрейд "
                        f"до {progress.difficulty.value}]"
                    ).strip()

        await self.session.flush()
        return session, progress

    async def update_session(
        self,
        session_id: int,
        data: WorkoutSessionUpdateSchema,
    ) -> tuple[WorkoutSession, UserProgress | None]:
        """
        Обновляет тренировочную сессию и при необходимости обновляет прогресс.

        Args:
            session_id: ID тренировочной сессии
            data: Данные для обновления

        Returns:
            Кортеж (обновленная сессия, обновленный прогресс или None)
        """
        completed = data.completed
        notes = data.notes

        return await self.complete_workout_session_and_update_progress(
            session_id=session_id,
            completed=completed if completed is not None else False,
            notes=notes,
        )

    async def create_new_session_from_last(
        self,
        user_id: int,
        exercise_type: ExerciseType,
    ) -> WorkoutSession:
        """
        Оркестрирует создание новой тренировочной сессии на основе последней.

        Процесс:
        1. Получает последнюю сессию пользователя для упражнения
        2. Получает текущий прогресс
        3. Создаёт новую сессию с текущими параметрами прогресса

        Args:
            user_id: ID пользователя
            exercise_type: Тип упражнения

        Returns:
            Новая WorkoutSession
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

        await self.session.flush()
        return new_session
