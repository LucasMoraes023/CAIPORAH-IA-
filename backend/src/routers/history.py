from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..services.history_service import HistoryService
from ..routers.auth import get_current_user

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get('/')
async def list_history(user_id: int | None = None, db: Session = Depends(get_db), current_user: object = Depends(get_current_user)):
    service = HistoryService(db)
    return service.list_history(user_id)
