import pytest
from app.models.models import UserProgress, Difficulty, ExerciseType

# --- Тесты логики Difficulty (без БД) ---


def test_reps_range_beginner():
    reps = Difficulty.BEGINNER.get_reps_range()
    assert reps == [1, 2, 3, 4, 5]
    assert len(reps) == 5


def test_get_reps_range_advanced():
    reps = Difficulty.ADVANCED.get_reps_range()
    assert reps[0] == 13
    assert reps[-1] == 30


# --- Тесты модели UserProgress (нужна фикстура session) ---


def test_try_upgrade_difficulty_beginner_to_intermediate(session):
    progress = UserProgress(
        user_id=1,
        exercise_type=ExerciseType.PULL_UPS,
        difficulty=Difficulty.BEGINNER,
        current_reps_per_set=6,
    )
    result = progress.try_upgrade_difficulty()
    assert result is True
    assert progress.difficulty == Difficulty.INTERMEDIATE


def test_validate_reps_error(session):
    """Проверяем, что валидатор не пускает некорректное число повторов"""
    progress = UserProgress(
        difficulty=Difficulty.BEGINNER, exercise_type=ExerciseType.PUSH_UPS
    )

    with pytest.raises(ValueError) as excinfo:
        progress.current_reps_per_set = 10  # Для новичка максимум 5

    assert "нельзя выбрать 10 повторов" in str(excinfo.value)
