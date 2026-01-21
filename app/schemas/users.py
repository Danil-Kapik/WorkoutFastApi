from pydantic import BaseModel, EmailStr
from app.schemas.base import BaseSchema, TimestampSchema


class UserCreateSchema(BaseModel):
    username: str
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
