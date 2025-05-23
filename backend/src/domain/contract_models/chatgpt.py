# src/domain/contract_models/chatgpt.py

from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    success: bool
    reply: str
