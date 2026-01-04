from pydantic import BaseModel, EmailStr
from app.schemas.base import ORMBaseSchema, TimestampSchema


class UserCreateSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserReadSchema(ORMBaseSchema, TimestampSchema):
    id: int
    username: str
    email: str


class UserLoginSchema(BaseModel):
    login: str  # email или username
    password: str
