from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..schemas import GameCreate
from ..services.game_service import GameService

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get('/')
async def list_games(db: Session = Depends(get_db)):
    service = GameService(db)
    return service.list_games()


@router.post('/')
async def create_game(payload: GameCreate, db: Session = Depends(get_db)):
    service = GameService(db)
    return service.create_game(payload.name)
