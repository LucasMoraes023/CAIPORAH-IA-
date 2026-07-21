from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..schemas import ConversationCreate
from ..services.conversation_service import ConversationService
from ..routers.auth import get_current_user

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get('/')
async def list_conversations(user_id: int | None = None, db: Session = Depends(get_db), current_user: object = Depends(get_current_user)):
    service = ConversationService(db)
    return service.list_conversations(user_id)


@router.post('/')
async def create_conversation(payload: ConversationCreate, db: Session = Depends(get_db), current_user: object = Depends(get_current_user)):
    if payload.role not in ('user', 'assistant'):
        raise HTTPException(status_code=400, detail='Role deve ser user ou assistant')
    service = ConversationService(db)
    return service.create_message(payload.message, payload.role, payload.user_id, payload.game_id)
