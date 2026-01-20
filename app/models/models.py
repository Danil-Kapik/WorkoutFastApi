from __future__ import annotations

import enum
from datetime import datetime, timezone
from typing import Annotated


from sqlalchemy import (
    ForeignKey,
    String,
    CheckConstraint,
    UniqueConstraint,
    func,
    Enum as SQLEnum,
    DateTime,
)

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)


class ExerciseType(str, enum.Enum):
    PULL_UPS = "подтягивания"
    PUSH_UPS = "отжимания"
    DEADLIFT = "тяга"
    SQUAT = "присед"


class Difficulty(str, enum.Enum):
    BEGINNER = "дохляк"
    INTERMEDIATE = "живчик"
    ADVANCED = "спортик"

    def get_reps_range(self) -> list[int]:
        """Возвращает диапазон повторений для текущего уровня сложности"""
        if self == Difficulty.BEGINNER:
            start, end = 1, 5
        elif self == Difficulty.INTERMEDIATE:
            start, end = 6, 12
        else:
            start, end = 13, 30

        return list(range(start, end + 1))

    @staticmethod
    def from_reps(reps: int) -> "Difficulty":
        """Определяет уровень сложности на основе количества повторений"""
        if reps <= 5:
            return Difficulty.BEGINNER
        elif reps <= 12:
            return Difficulty.INTERMEDIATE
        else:
            return Difficulty.ADVANCED


class Base(DeclarativeBase):
    pass


int_pk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
created_at = Annotated[
    datetime, mapped_column(nullable=False, server_default=func.now())
]
updated_at = Annotated[
    datetime,
    mapped_column(
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    ),
]


class User(Base):
    __tablename__ = "users"

    id: Mapped[int_pk] = mapped_column()
    username: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(100))

    sessions: Mapped[list["WorkoutSession"]] = relationship(
        "WorkoutSession",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="select",
    )
    progress: Mapped[list["UserProgress"]] = relationship(
        "UserProgress",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="select",
    )

    def __repr__(self) -> str:
        return (
            f"User(id={self.id!r}, "
            f"username={self.username!r}, "
            f"email={self.email!r})"
        )


class UserProgress(Base):
    __tablename__ = "user_progress"

    id: Mapped[int_pk] = mapped_column()
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    exercise_type: Mapped[ExerciseType] = mapped_column(
        SQLEnum(ExerciseType, name="exercise_type_enum"),
        nullable=False,
    )
    difficulty: Mapped[Difficulty] = mapped_column(
        SQLEnum(Difficulty, name="difficulty_enum"),
        nullable=False,
    )
    current_reps_per_set: Mapped[int] = mapped_column(default=1)
    last_success_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    user = relationship(
        "User",
        back_populates="progress",
        lazy="select",
    )

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "exercise_type",
            name="user_exercise_unique",
        ),
        CheckConstraint(
            "current_reps_per_set > 0", name="check_reps_positive"
        ),
    )

    def up_level(self) -> None:
        """Увеличивает количество повторений на 1"""
        self.current_reps_per_set += 1
        self.last_success_at = datetime.now(timezone.utc)

    def get_starting_reps(self) -> int:
        """Возвращает стартовое количество повторений для текущего уровня"""
        return {
            Difficulty.BEGINNER: 1,
            Difficulty.INTERMEDIATE: 6,
            Difficulty.ADVANCED: 13,
        }[self.difficulty]

    def try_upgrade_difficulty(self) -> bool:
        """
        Проверяет и повышает уровень сложности.
        Возвращает True, если апгрейд произошёл.
        """
        if (
            self.difficulty == Difficulty.BEGINNER
            and self.current_reps_per_set >= 6
        ):
            self.difficulty = Difficulty.INTERMEDIATE
            self.current_reps_per_set = 6
            return True

        if (
            self.difficulty == Difficulty.INTERMEDIATE
            and self.current_reps_per_set >= 13
        ):
            self.difficulty = Difficulty.ADVANCED
            self.current_reps_per_set = 13
            return True
        return False

    def set_reps(self, value: int) -> None:
        allowed_range = self.difficulty.get_reps_range()
        if value not in allowed_range:
            raise ValueError(
                f"Для уровня {self.difficulty.value} "
                f"допустимы повторы: {allowed_range}"
            )
        self.current_reps_per_set = value

    def __repr__(self) -> str:
        return (
            f"UserProgress(user_id={self.user_id!r}, "
            f"exercise={self.exercise_type.value!r}, "
            f"difficulty={self.difficulty.value!r}, "
            f"reps={self.current_reps_per_set!r})"
        )


class WorkoutSession(Base):
    __tablename__ = "workout_sessions"

    id: Mapped[int_pk] = mapped_column()
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    exercise_type: Mapped[ExerciseType] = mapped_column(
        SQLEnum(ExerciseType, name="exercise_type_enum"),
        nullable=False,
    )
    difficulty: Mapped[Difficulty] = mapped_column(
        SQLEnum(Difficulty, name="difficulty_enum"),
        nullable=False,
    )
    reps_per_set_at_start: Mapped[int]
    completed: Mapped[bool] = mapped_column(
        default=False
    )  # True — "готово", False — "сдулся"
    notes: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    user = relationship(
        "User",
        back_populates="sessions",
        lazy="select",
    )

    __table_args__ = (
        CheckConstraint("reps_per_set_at_start >= 1", name="check_start_reps"),
    )

    def __repr__(self) -> str:
        return (
            f"WorkoutSession(user_id={self.user_id}, "
            f"exercise={self.exercise_type.value}, "
            f"completed={self.completed}, "
            f"reps_at_start={self.reps_per_set_at_start})"
        )
