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
from src.router.chatgpt import chatgpt_router


class BaseRouter:
    # Inicializa o app FastAPI
    app = FastAPI(
        title="W1 Hackathon Backend API",
        description="Documentation for the project's backend API.",
    )

    @staticmethod
    def register_routers():
        """
        Registra todas as rotas da aplicação.
        """
        user_router = AccountRouter.get_routes()
        auth_router = AuthRouter.get_routes()
        patrimony_router = PatrimonyRouter.get_routes()

        BaseRouter.app.include_router(user_router)
        BaseRouter.app.include_router(auth_router)
        BaseRouter.app.include_router(patrimony_router)

        # Rota do ChatGPT
        BaseRouter.app.include_router(chatgpt_router)

        return BaseRouter.app

    @staticmethod
    @app.middleware("http")
    async def middleware_response(request: Request, call_next):
        """
        Middleware para medir o tempo de execução da requisição
        e tratar exceções personalizadas.
        """
        try:
            start_time = time.perf_counter()
            response = await call_next(request)
            process_time = time.perf_counter() - start_time
            response.headers["X-Process-Time"] = str(process_time)
            return response

        except BadRequestError as err:
            logging.error(f"{err}")
            return _error_response(status.HTTP_400_BAD_REQUEST)

        except (NotFoundError, EntityNotFound) as err:
            logging.error(f"{err}")
            return _error_response(status.HTTP_404_NOT_FOUND)

        except Unauthorized as err:
            logging.error(f"{err}")
            return _error_response(
                status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password"
            )

        except CouldNotValidateCredentials as err:
            logging.error(f"{err}")
            return _error_response(
                status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )

        except EmailAlreadyInUse as err:
            logging.error(f"{err}")
            return _error_response(
                status.HTTP_409_CONFLICT,
                detail="Email already in use"
            )

        except EnvironmentException as err:
            logging.critical(f"ENVIRONMENT ERROR!!! -> {err}")
            raise err  # Nesse caso, propaga o erro (parar aplicação)

        except Exception as err:
            logging.error(f"{err}")
            return _error_response(status.HTTP_500_INTERNAL_SERVER_ERROR)


def _error_response(status_code: int, detail: str = "An error occurred"):
    """
    Função auxiliar para padronizar resposta de erro.
    """
    return Response(
        status_code=status_code,
        content=json.dumps({
            "success": False,
            "detail": detail
        }),
        media_type="application/json"
    )
