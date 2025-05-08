import logging
import os

from src.domain.exceptions.infrastructure import EnvironmentException

db_password = os.getenv("DB_PASSWORD")


def get_config(key: str):
    try:
        return os.getenv(key)
    except Exception as error:
        logging.error(f"Error getting environment variable: {key}")
        raise EnvironmentException()


__all__ = ["get_config"]
