from fastapi import APIRouter
from ..database import init_db

router = APIRouter()

@router.on_event('startup')
async def on_startup():
    init_db()

@router.get('/ping')
async def ping():
    return {'status': 'ok', 'message': 'GameCopilot AI backend está ativo'}
