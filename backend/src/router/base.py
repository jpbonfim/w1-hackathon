import json
import logging
import time

from fastapi import FastAPI, Request, Response
from starlette import status

from src.domain.exceptions.infrastructure import EnvironmentException
from src.domain.exceptions.router import (
    BadRequestError,
    NotFoundError,
    EntityNotFound,
    Unauthorized,
)
from src.domain.exceptions.service import CouldNotValidateCredentials, EmailAlreadyInUse
from src.router.auth import AuthRouter
from src.router.patrimony import PatrimonyRouter
from src.router.user import AccountRouter


class BaseRouter:
    app = FastAPI(
        title="W1 Hackathon Backend API",
        description="Documentation for the project's backend API.",
    )

    @staticmethod
    def register_routers():
        user_router = AccountRouter.get_routes()
        auth_router = AuthRouter.get_routes()
        patrimony_router = PatrimonyRouter.get_routes()
        BaseRouter.app.include_router(user_router)
        BaseRouter.app.include_router(auth_router)
        BaseRouter.app.include_router(patrimony_router)
        return BaseRouter.app

    @staticmethod
    @app.middleware("http")
    async def middleware_response(request: Request, call_next):
        try:
            start_time = time.perf_counter()
            response = await call_next(request)
            process_time = time.perf_counter() - start_time
            response.headers["X-Process-Time"] = str(process_time)
            return response

        except BadRequestError as err:
            logging.error(f"{err}")
            return Response(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=json.dumps({"success": False}),
            )

        except NotFoundError as err:
            logging.error(f"{err}")
            return Response(
                status_code=status.HTTP_404_NOT_FOUND,
                content=json.dumps({"success": False}),
            )

        except EntityNotFound as err:
            logging.error(f"{err}")
            return Response(
                status_code=status.HTTP_404_NOT_FOUND,
                content=json.dumps({"success": False}),
            )

        except Unauthorized as err:
            logging.error(f"{err}")
            return Response(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content=json.dumps(
                    {"success": False, "detail": "Incorrect username or password"}
                ),
            )

        except CouldNotValidateCredentials as err:
            logging.error(f"{err}")
            return Response(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content=json.dumps(
                    {"success": False, "detail": "Could not validate credentials"}
                ),
            )
        except EmailAlreadyInUse as err:
            logging.error(f"{err}")
            return Response(
                status_code=status.HTTP_409_CONFLICT,
                content=json.dumps(
                    {"success": False, "detail": "Email already in use"}
                ),
            )
        except EnvironmentException as err:
            logging.error(f"ENVIRONMENT ERROR!!! ->{err}")
            raise err

        except Exception as err:
            logging.error(f"{err}")
            return Response(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=json.dumps({"success": False}),
            )
