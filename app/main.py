import fastapi
from fastapi.middleware.cors import CORSMiddleware
from app.routers.auth import router as users_router
from app.routers.user_progress import router as user_progress_router
from app.routers.workout_session import router as workout_session_router


app = fastapi.FastAPI()

# Enable CORS for frontend (localhost:5173 in dev, configure for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)
app.include_router(user_progress_router)
app.include_router(workout_session_router)


@app.get("/")
async def root(request: fastapi.Request):
    return request.headers


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
