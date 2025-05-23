# src/services/chatgpt.py

import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


class ChatGPTService:
    @staticmethod
    def ask(message: str) -> str:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Você é um atendente de suporte simpático e prestativo."},
                    {"role": "user", "content": message}
                ],
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message["content"].strip()
        except Exception as e:
            raise RuntimeError(f"Erro ao consultar o ChatGPT: {str(e)}")
