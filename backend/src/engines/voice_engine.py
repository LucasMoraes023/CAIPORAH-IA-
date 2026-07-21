import io
import math
import struct
import wave
from typing import Optional
import tempfile
import os
import json
import requests

try:
    import pyttsx3
except Exception:
    pyttsx3 = None


class VoiceEngine:
    def __init__(self) -> None:
        self.active = False

    def start(self) -> None:
        self.active = True

    def stop(self) -> None:
        self.active = False

    def status(self) -> str:
        return 'active' if self.active else 'stopped'

    def transcribe(self, audio_data: bytes) -> str:
        if not audio_data:
            return ''

        # Prefer OpenAI Whisper via REST if API key is provided
        openai_key = os.environ.get('OPENAI_API_KEY')
        if openai_key:
            try:
                url = 'https://api.openai.com/v1/audio/transcriptions'
                files = {
                    'file': ('audio.wav', audio_data, 'audio/wav')
                }
                data = {'model': 'whisper-1'}
                headers = {'Authorization': f'Bearer {openai_key}'}
                resp = requests.post(url, headers=headers, data=data, files=files, timeout=30)
                if resp.status_code == 200:
                    j = resp.json()
                    return j.get('text', '')
            except Exception:
                # fallthrough to placeholder
                pass

        # fallback placeholder
        return 'Transcrição simulada do áudio enviado.'

    def synthesize(self, text: str) -> bytes:
        if not text:
            return b''
        # Prefer pyttsx3 if available for clearer TTS
        if pyttsx3:
            try:
                engine = pyttsx3.init()
                fd, path = tempfile.mkstemp(suffix='.wav')
                os.close(fd)
                engine.save_to_file(text, path)
                engine.runAndWait()
                with open(path, 'rb') as f:
                    data = f.read()
                try:
                    os.remove(path)
                except Exception:
                    pass
                return data
            except Exception:
                # fallthrough to internal generator
                pass

        return self._generate_wav(text)

    def _generate_wav(self, text: str, sample_rate: int = 22050) -> bytes:
        duration = max(1.0, min(len(text) * 0.1, 5.0))
        frequency = 440.0
        volume = 0.2
        num_samples = int(sample_rate * duration)

        buffer = io.BytesIO()
        with wave.open(buffer, 'wb') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)

            for i in range(num_samples):
                t = float(i) / sample_rate
                char_index = int((i / num_samples) * len(text))
                char_frequency = frequency + 20.0 * (ord(text[char_index]) % 10)
                sample = volume * math.sin(2.0 * math.pi * char_frequency * t)
                wav_file.writeframes(struct.pack('<h', int(sample * 32767)))

        return buffer.getvalue()
