from sqlalchemy.orm import Session
from ..repositories.history_repository import HistoryRepository


class HistoryService:
    def __init__(self, db: Session) -> None:
        self.repository = HistoryRepository(db)

    def list_history(self, user_id: int | None = None):
        return self.repository.list_history(user_id)

    def create_event(self, action: str, details: str, user_id: int | None = None, game_id: int | None = None):
        return self.repository.create_event(action, details, user_id, game_id)
