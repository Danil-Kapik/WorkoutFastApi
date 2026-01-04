from fastapi import APIRouter
from app.dao.progress_dao import UserProgressDAO


router = APIRouter(
    prefix="/user_progress",
    tags=["Прогресс пользователя"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_user_progress():
    return await UserProgressDAO.get_all_user_progress()
