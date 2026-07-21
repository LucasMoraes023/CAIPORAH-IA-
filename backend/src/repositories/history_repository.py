from sqlalchemy.orm import Session
from ..models import History


class HistoryRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_history(self, user_id: int | None = None) -> list[History]:
        query = self.db.query(History)
        if user_id is not None:
            query = query.filter(History.user_id == user_id)
        return query.order_by(History.occurred_at.desc()).all()

    def create_event(self, action: str, details: str, user_id: int | None = None, game_id: int | None = None) -> History:
        record = History(action=action, details=details, user_id=user_id, game_id=game_id)
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record
