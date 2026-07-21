from fastapi import APIRouter
from ..plugins.loader import discover_plugins

router = APIRouter()

@router.get('/')
async def list_plugins():
    return discover_plugins()
