import os
from typing import Optional

try:
    import openai
except Exception:
    openai = None

from .conversation_engine import ConversationEngine


class LLMEngine:
    def __init__(self) -> None:
        self.active = False
        self.fallback = ConversationEngine()
        self.api_key = os.environ.get('OPENAI_API_KEY')
        if self.api_key and openai:
            openai.api_key = self.api_key

    def start(self) -> None:
        self.active = True

    def stop(self) -> None:
        self.active = False

    def status(self) -> str:
        return 'active' if self.active else 'stopped'

    def generate_response(self, message: str, memory_summary: Optional[str] = None) -> str:
        if self.api_key and openai:
            try:
                prompt = f"Resumo de memória: {memory_summary}\nUsuário: {message}" if memory_summary else f"Usuário: {message}"
                resp = openai.ChatCompletion.create(
                    model=os.environ.get('OPENAI_MODEL', 'gpt-3.5-turbo'),
                    messages=[{'role': 'user', 'content': prompt}],
                    max_tokens=300,
                )
                text = resp.choices[0].message.content.strip()
                return text
            except Exception:
                return self.fallback.generate_response(message, memory_summary)

        return self.fallback.generate_response(message, memory_summary)
