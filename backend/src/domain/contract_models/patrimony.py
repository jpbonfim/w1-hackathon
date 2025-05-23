from typing import Optional, List

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

class Evolution(BaseModel):
    month: str
    value: float
class EvolutionResponse(BaseModel):
    success: bool
    evolution: List[Evolution]

