import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class GeminiChat:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.configure()
        self.model_name = 'gemini-2.0-flash'  # Modelo mais recente
        self.model = genai.GenerativeModel(self.model_name)
        self.chat = None
        self.start_new_chat()

    def configure(self):
        """Configura a API do Gemini"""
        if not self.api_key:
            raise ValueError("Chave da API Gemini não encontrada no .env")
        genai.configure(api_key=self.api_key)

    def start_new_chat(self):
        """Inicia uma nova conversa"""
        self.chat = self.model.start_chat(history=[])

    def send_message(self, message):
        """Envia mensagem e recebe resposta"""
        try:
            response = self.chat.send_message(
                message,
                generation_config={
                    "temperature": 0.7,
                    "top_p": 0.9
                }
            )
            return response.text
        except Exception as e:
            return f"Erro ao processar: {str(e)}"