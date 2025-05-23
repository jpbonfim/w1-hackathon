from pydantic import BaseModel, Field, constr


class Address(BaseModel):
    street: str = Field(examples=["Av. Paulista"])
    number: str = Field(examples=["1000"])
    neighborhood: str = Field(examples=["Bela Vista"])
    city: str = Field(examples=["São Paulo"])
    state: str = Field(examples=["SP"], min_length=2, max_length=2)
    zip_code: str = Field(examples=["01310-100"], pattern=r"^\d{5}-\d{3}$")
