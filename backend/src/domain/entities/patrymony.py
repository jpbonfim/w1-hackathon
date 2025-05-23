from decimal import Decimal
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class Patrimony(BaseModel):
    stocks: Decimal = Field(default=0.0, ge=0)
    real_estate_funds: Decimal = Field(default=0, ge=0)
    investment_funds: Decimal = Field(default=0, ge=0)
    fixed_income: Decimal = Field(default=0, ge=0)
    companies: Decimal = Field(default=0, ge=0)
    real_estate: Decimal = Field(default=0, ge=0)
    others: Decimal = Field(default=0, ge=0)

    # @field_validator('stocks', 'real_estate_funds', 'investment_funds', 'fixed_income', 'companies', 'real_estate', 'others')
    # @staticmethod
    # def validate_decimal_places(value: Decimal) -> Decimal:
    #     if value.as_tuple().exponent < -2:  # More than 2 decimal places
    #         raise ValueError("Value must have at most 2 decimal places")
    #     return value

class Holding(BaseModel):
    status: str = Field(default="NO_HOLDING")
    tax_with: Decimal = Field(default=0, ge=0)
    tax_without: Decimal = Field(default=0, ge=0)

class PatrimonyInDB(Patrimony):
    id: int
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
