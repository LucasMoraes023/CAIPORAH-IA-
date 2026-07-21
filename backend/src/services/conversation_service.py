from sqlalchemy.orm import Session
from ..engines.llm_engine import LLMEngine
from ..repositories.conversation_repository import ConversationRepository
from ..services.history_service import HistoryService
from ..services.memory_service import MemoryService


class ConversationService:
    def __init__(self, db: Session) -> None:
        self.repository = ConversationRepository(db)
        self.engine = LLMEngine()
        self.memory_service = MemoryService(db)
        self.history_service = HistoryService(db)

    def list_conversations(self, user_id: int | None = None):
        return self.repository.list_conversations(user_id)

    def create_message(self, message: str, role: str, user_id: int | None = None, game_id: int | None = None):
        if role == 'user':
            user_record = self.repository.create_message(message, role, user_id, game_id)
            memory_summary = None

            if user_id is not None:
                summary_data = self.memory_service.summarize_memory(user_id)
                memory_summary = summary_data.get('summary')

            assistant_text = self.engine.generate_response(message, memory_summary)
            assistant_record = self.repository.create_message(assistant_text, 'assistant', user_id, game_id)

            self.history_service.create_event(
                'conversation',
                f'Usuário: {message}',
                user_id,
                game_id,
            )
            self.history_service.create_event(
                'assistant_response',
                assistant_text,
                user_id,
                game_id,
            )

            return {'user': user_record, 'assistant': assistant_record}

        return self.repository.create_message(message, role, user_id, game_id)
