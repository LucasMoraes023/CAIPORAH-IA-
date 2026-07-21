from sqlalchemy.orm import Session
from ..engines.memory_engine import MemoryEngine
from ..repositories.memory_repository import MemoryRepository
from ..services.history_service import HistoryService


class MemoryService:
    def __init__(self, db: Session) -> None:
        self.repository = MemoryRepository(db)
        self.engine = MemoryEngine()
        self.history_service = HistoryService(db)

    def list_memory(self, user_id: int | None = None):
        return self.repository.list_memory(user_id)

    def create_memory(self, category: str, content: str, user_id: int | None = None):
        memory = self.repository.create_memory(category, content, user_id)
        self.history_service.create_event(
            'memory_created',
            f'{category}: {content}',
            user_id,
        )
        return memory

    def summarize_memory(self, user_id: int | None = None):
        records = self.repository.list_memory(user_id)
        return self.engine.summarize(records)
