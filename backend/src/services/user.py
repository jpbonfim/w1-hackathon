from uuid import uuid4

from src.domain.entities.user import User
from src.domain.exceptions.infrastructure import RecordAlreadyExistsException
from src.domain.exceptions.service import EmailAlreadyInUse
from src.repositories.user import UserRepository


class UserService:
    @classmethod
    async def get_user(cls, user_id: str) -> User:
        user = await UserRepository.get_user(user_id)
        return user

    @classmethod
    async def create_user(cls, user_data: dict):
        user_id = str(uuid4())
        user = User(user_id=user_id, **user_data)
        try:
            await UserRepository.create_user(user)
        except RecordAlreadyExistsException:
            raise EmailAlreadyInUse()
        return user_id

    @classmethod
    async def update_user(cls, user_id: str, update_data: dict):
        pass
