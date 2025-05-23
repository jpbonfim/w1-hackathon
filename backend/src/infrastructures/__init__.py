import logging
import os

from src.domain.exceptions.infrastructure import EnvironmentException

db_password = os.getenv("DB_PASSWORD")


def get_config(key: str) -> str:
    try:
        value = os.getenv(key)
        if value is None:
            raise Exception()
        return value
    except Exception:
        logging.error(f"Error getting environment variable: {key}")
        raise EnvironmentException()


__all__ = ["get_config"]
