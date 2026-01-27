from pydantic import BaseModel, EmailStr, Field
from app.schemas.base import BaseSchema, TimestampSchema


class UserCreateSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str


class UserReadSchema(BaseSchema, TimestampSchema):
    id: int
    username: str
    email: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int | None = None
