import asyncio
import random

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
)
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.models.models import (
    User,
    UserProgress,
    WorkoutSession,
    ExerciseType,
    Difficulty,
)

# ---------------------------------------------------------
# Async engine и фабрика сессий
# ---------------------------------------------------------

DATABASE_URL = settings.DATABASE_URL

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# ---------------------------------------------------------
# Основная логика сидинга
# ---------------------------------------------------------


async def seed_data() -> None:
    async with AsyncSessionLocal() as db:
        try:
            # 1. Создаём пользователей
            users: list[User] = []

            for i in range(1, 7):
                user = User(
                    username=f"атлет_{i}",
                    email=f"user{i}@example.com",
                    password="hashed_password",
                )
                db.add(user)
                users.append(user)

            # Получаем ID пользователей
            await db.flush()

            # 2. Прогресс и тренировки
            for user in users:
                exercises = [
                    ExerciseType.PULL_UPS,
                    ExerciseType.PUSH_UPS,
                ]

                for ex_type in exercises:
                    progress = UserProgress(
                        user_id=user.id,
                        exercise_type=ex_type,
                        difficulty=Difficulty.BEGINNER,
                        current_reps_per_set=3,
                    )
                    db.add(progress)
                    await db.flush()

                    # 3. Генерируем 5 тренировок
                    for _ in range(5):
                        is_completed = random.choice([True, True, False])

                        session = WorkoutSession(
                            user_id=user.id,
                            exercise_type=ex_type,
                            difficulty=progress.difficulty,
                            reps_per_set_at_start=progress.current_reps_per_set,
                            completed=is_completed,
                            notes="Случайная тренировка",
                        )
                        db.add(session)

                        if is_completed:
                            progress.up_level()
                            progress.try_upgrade_difficulty()

                        await db.flush()

            await db.commit()
            print("База успешно наполнена!")

        except Exception as e:
            await db.rollback()
            print(f"Ошибка: {e}")


# ---------------------------------------------------------
# Точка входа
# ---------------------------------------------------------

if __name__ == "__main__":
    asyncio.run(seed_data())
