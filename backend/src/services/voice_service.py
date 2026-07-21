from ..engines.voice_engine import VoiceEngine


class VoiceService:
    def __init__(self) -> None:
        self.engine = VoiceEngine()

    def status(self) -> str:
        return self.engine.status()

    def transcribe(self, audio_data: bytes) -> str:
        return self.engine.transcribe(audio_data)

    def synthesize(self, text: str) -> bytes:
        return self.engine.synthesize(text)
