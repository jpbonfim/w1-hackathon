import logging
from datetime import datetime, timedelta, UTC
from typing import Optional

import bcrypt
import jwt
from fastapi.security import OAuth2PasswordBearer

from src.domain.contract_models.auth import TokenData
from src.domain.entities.user import User
from src.domain.exceptions.repository import DataNotFound
from src.domain.exceptions.service import CouldNotValidateCredentials
from src.infrastructures import get_config
from src.repositories.user import UserRepository


class AuthService:
    __SECRET_KEY = get_config("AUTH_KEY")
    __ALGORITHM = "HS256"
    __ACCESS_TOKEN_EXPIRE_MINUTES = int(get_config("AUTH_TOKEN_EXPIRE_MINUTES"))
    __oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

    @classmethod
    def get_token_expiration_time(cls) -> int:
        return cls.__ACCESS_TOKEN_EXPIRE_MINUTES

    @classmethod
    async def verify_password(cls, username: str, password: str) -> bool:
        password_bytes = bytes(password, "utf-8")
        hashed_password = await UserRepository.get_password_by_email(username)
        if bcrypt.checkpw(password_bytes, hashed_password):
            return True
        return False

    @classmethod
    def get_password_hash(cls, password: str) -> bytes:
        password_bytes = bytes(password, "utf-8")
        salt = bcrypt.gensalt()
        hash_pass = bcrypt.hashpw(password_bytes, salt)
        return hash_pass

    @classmethod
    async def authenticate_user(cls, username: str, password: str) -> Optional[User]:
        try:
            user = await UserRepository.get_user_by_email(username)
        except DataNotFound:
            user = None
        if not user:
            return None
        correct_password = await cls.verify_password(username, password)
        if not correct_password:
            return None
        return user

    @classmethod
    def create_access_token(
        cls, data: dict, expires_delta: Optional[timedelta] = None
    ) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(UTC) + expires_delta
        else:
            expire = datetime.now(UTC) + timedelta(
                minutes=cls.__ACCESS_TOKEN_EXPIRE_MINUTES
            )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, cls.__SECRET_KEY, algorithm=cls.__ALGORITHM)
        return encoded_jwt

    @classmethod
    def validate_token(cls, token: str) -> TokenData:
        try:
            payload = jwt.decode(token, cls.__SECRET_KEY, algorithms=[cls.__ALGORITHM])
            user_id = payload.get("user_id")
            if user_id is None:
                raise CouldNotValidateCredentials()
            token_data = TokenData(user_id=user_id)
            return token_data

        except Exception as error:
            message = f"Failed to decode token. Error: {error}"
            logging.error(message)
            raise CouldNotValidateCredentials()
