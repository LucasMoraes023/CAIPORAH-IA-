from fastapi import APIRouter, Depends
from ..services.vision_service import VisionService
from ..routers.auth import get_current_user

router = APIRouter()
service = VisionService()

@router.get('/status')
async def status(current_user: object = Depends(get_current_user)):
    return {'vision': service.status()}

@router.get('/analyze')
async def analyze(current_user: object = Depends(get_current_user)):
    return service.analyze()
