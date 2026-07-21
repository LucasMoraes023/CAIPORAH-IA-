from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..schemas import MemoryCreate
from ..services.memory_service import MemoryService
from ..routers.auth import get_current_user

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get('/status')
async def status(current_user: object = Depends(get_current_user)):
    return {'memory': 'ready'}


@router.get('/')
async def list_memory(user_id: int | None = None, db: Session = Depends(get_db), current_user: object = Depends(get_current_user)):
    service = MemoryService(db)
    return service.list_memory(user_id)


@router.get('/summary')
async def memory_summary(user_id: int | None = None, db: Session = Depends(get_db), current_user: object = Depends(get_current_user)):
    service = MemoryService(db)
    return service.summarize_memory(user_id)


@router.post('/')
async def create_memory(payload: MemoryCreate, db: Session = Depends(get_db), current_user: object = Depends(get_current_user)):
    service = MemoryService(db)
    return service.create_memory(payload.category, payload.content, payload.user_id)
