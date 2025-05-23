import logging

import openai
import os
from openai import OpenAI


class ChatGPTService:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    @staticmethod
    def ask(message: str) -> str:
        try:
            response = ChatGPTService.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Você é um atendente de suporte simpático e prestativo."},
                    {"role": "user", "content": message}
                ]
            )

            return response.choices[0].message.content

        except Exception as e:
            logging.error("Erro ao consultar o ChatGPT: %s", str(e))
            raise Exception("Erro ao consultar o ChatGPT: \n" + str(e))

