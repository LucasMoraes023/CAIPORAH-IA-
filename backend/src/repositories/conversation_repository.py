from sqlalchemy.orm import Session
from ..models import Conversation


class ConversationRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_conversations(self, user_id: int | None = None) -> list[Conversation]:
        query = self.db.query(Conversation)
        if user_id is not None:
            query = query.filter(Conversation.user_id == user_id)
        return query.order_by(Conversation.created_at.asc()).all()

    def create_message(self, message: str, role: str, user_id: int | None = None, game_id: int | None = None) -> Conversation:
        record = Conversation(message=message, role=role, user_id=user_id, game_id=game_id)
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record
