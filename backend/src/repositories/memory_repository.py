from sqlalchemy.orm import Session
from ..models import MemoryItem


class MemoryRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_memory(self, user_id: int | None = None) -> list[MemoryItem]:
        query = self.db.query(MemoryItem)
        if user_id is not None:
            query = query.filter(MemoryItem.user_id == user_id)
        return query.order_by(MemoryItem.created_at.desc()).all()

    def create_memory(self, category: str, content: str, user_id: int | None = None) -> MemoryItem:
        memory = MemoryItem(category=category, content=content, user_id=user_id)
        self.db.add(memory)
        self.db.commit()
        self.db.refresh(memory)
        return memory
