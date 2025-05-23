import logging
from typing import Annotated

from fastapi import APIRouter, Header

from src.domain.contract_models.chatgpt import ChatRequest, ChatResponse
from src.services.auth import AuthService
from src.services.chatgpt import ChatGPTService


class ChatGPTRouter:
    __router = APIRouter(prefix="/chatgpt", tags=["ChatGPT Assistant"])

    @staticmethod
    def get_routes():
        return ChatGPTRouter.__router

    @staticmethod
    @__router.post("/ask", response_model=ChatResponse)
    async def ask_gpt(
        auth: Annotated[str, Header()],
        request: ChatRequest
    ):
        try:
            # Valida o token e extrai o user_id (mesmo que não seja usado agora, prepara pro futuro)
            token_data = AuthService.validate_token(auth)
            user_id = token_data.user_id

            # Chama o serviço do ChatGPT
            reply = ChatGPTService.ask(message=request.message)

            return ChatResponse(success=True, reply=reply)

        except Exception as e:
            logging.error("Erro ao processar pergunta no ChatGPT: %s", str(e))
            raise
