# src/services/chatgpt.py
import os
import logging
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ChatGPTService:
    @staticmethod
    def ask(message: str) -> str:
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Você é um atendente de suporte simpático e prestativo."},
                    {"role": "user", "content": message}
                ],
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logging.error("Erro ao consultar o ChatGPT: %s", str(e))
            raise RuntimeError(f"Erro ao consultar o ChatGPT: {str(e)}")
