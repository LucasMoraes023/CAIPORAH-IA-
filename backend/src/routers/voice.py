import base64
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from ..services.voice_service import VoiceService
from ..routers.auth import get_current_user

router = APIRouter()
service = VoiceService()

class VoiceTranscribeRequest(BaseModel):
    audio_data: str

class VoiceSynthesizeRequest(BaseModel):
    text: str

@router.get('/status')
async def status(current_user: object = Depends(get_current_user)):
    return {'voice': service.status()}

@router.post('/transcribe')
async def transcribe(payload: VoiceTranscribeRequest, current_user: object = Depends(get_current_user)):
    try:
        data = base64.b64decode(payload.audio_data)
    except Exception:
        raise HTTPException(status_code=400, detail='audio_data deve ser base64 válido')

    text = service.transcribe(data)
    return {'transcription': text}

@router.post('/synthesize')
async def synthesize(payload: VoiceSynthesizeRequest, current_user: object = Depends(get_current_user)):
    audio_bytes = service.synthesize(payload.text)
    return {'audio_base64': base64.b64encode(audio_bytes).decode('utf-8')}
