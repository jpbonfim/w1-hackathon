import logging
from typing import Any, Optional

from pydantic import BaseModel, ValidationError

from src.domain.exceptions.user import InconsistentUserData


class User(BaseModel):
    def __init__(self, **data: Any):
        try:
            super().__init__(**data)
        except ValidationError as error:
            logging.error(f"Could not build user object. Error: {error}")
            raise InconsistentUserData()

    user_id: str
    name: str
    username: str
    email: str
    # cpf: Optional[str]
