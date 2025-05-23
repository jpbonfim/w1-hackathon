from typing import Optional

from pydantic import BaseModel, EmailStr, Field, constr

from src.domain.entities.user import User


class RegisterRequest(BaseModel):
    name: str = Field(examples=["João Silva"])
    username: str = Field(examples=["joaosilva"])
    email: EmailStr = Field(examples=["joao@example.com"])
    password: constr(min_length=6) = Field(examples=["strongpassword123"])


class RegisterResponse(BaseModel):
    success: bool
    user_id: str


class LoginRequest(BaseModel):
    email: EmailStr = Field(examples=["joao@example.com"])
    password: constr(min_length=6) = Field(examples=["strongpassword123"])


class LoginResponse(BaseModel):
    success: bool
    user_id: str
    access_token: str
    token_type: str


class MeResponse(BaseModel):
    success: bool
    data: User


class TokenData(BaseModel):
    user_id: Optional[str] = None
