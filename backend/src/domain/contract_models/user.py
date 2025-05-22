from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from src.domain.entities.user import User


class UpdateUserRequest(BaseModel):
    name: Optional[str] = Field(examples=["Alice Smith"], min_length=1, max_length=100)
    email: Optional[EmailStr] = Field(examples=["alice@gmail.com"])
    password: Optional[str] = Field(examples=["newstrongpassword456"], min_length=6)


class CreateUserRequest(BaseModel):
    name: str = Field(examples=["João Silva"])
    email: EmailStr = Field(examples=["joao@example.com"])
    cpf: str = Field(examples=["123.456.789-00"])
    # phone: str = Field(examples=["(11) 91234-5678"])
    # birth_date: str = Field(examples=["1990-05-15"])
    # address: Address
    # user: User


class CreateUserResponse(BaseModel):
    success: bool
    user_id: str


class GetUserRequest(BaseModel):
    user_id: str

class GetUserResponse(BaseModel):
    success: bool
    user: User


class MeResponse(BaseModel):
    success: bool
    user_data: User

