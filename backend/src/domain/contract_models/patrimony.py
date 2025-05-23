from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from src.domain.entities.patrymony import Patrimony
from src.domain.entities.user import User


class GetPatrimonyResponse(BaseModel):
    success: bool
    patrimony: Patrimony


class UpdatePatrimonyRequest(BaseModel):
    success: bool
    patrimony: Patrimony


class UpdatePatrimonyResponse(BaseModel):
    success: bool
    patrimony: Patrimony
