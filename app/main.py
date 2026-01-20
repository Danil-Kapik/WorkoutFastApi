import fastapi
from app.routers.auth import router as users_router
from app.routers.user_progress import router as user_progress_router
from app.routers.workout_session import router as workout_session_router


app = fastapi.FastAPI()

app.include_router(users_router)
app.include_router(user_progress_router)
app.include_router(workout_session_router)


@app.get("/")
async def root(request: fastapi.Request):
    return request.headers


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
