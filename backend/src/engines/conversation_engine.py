from typing import Optional

class ConversationEngine:
    def __init__(self) -> None:
        self.active = False

    def start(self) -> None:
        self.active = True

    def stop(self) -> None:
        self.active = False

    def status(self) -> str:
        return 'active' if self.active else 'stopped'

    def generate_response(self, message: str, memory_summary: Optional[str] = None) -> str:
        context = f"Resumo de memória: {memory_summary}\n" if memory_summary else ''
        snippet = message if len(message) <= 120 else f"{message[:117]}..."
        return f"{context}Resposta assistente simulada para: {snippet}"
