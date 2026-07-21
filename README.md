# CAIPORAH-IA-

GameCopilot AI — companion app para jogadores com visão em tempo real, conversa por voz, memória e plugins.

## Como executar localmente (desenvolvimento)

Backend (Python / Poetry):

```bash
cd backend
poetry install
poetry run uvicorn src.app:app --reload --host 127.0.0.1 --port 8000
```

Frontend (React / Vite):

```bash
cd frontend
npm install
npm run dev
```

Abra `http://localhost:5173` para a interface.

## Recursos implementados
- Captura de tela e análise simples (`/vision/analyze`)
- Chat com LLM opcional (usa OpenAI se `OPENAI_API_KEY` estiver presente)
- TTS local via `pyttsx3` (fallback para gerador interno WAV)
- Memória e histórico persistidos em SQLite
- Sistema de plugins (descoberta básica)

## O que falta para produção
- STT de qualidade (Whisper ou serviço cloud)
- Análise de HUD mais robusta (templates por jogo)
- Empacotamento Electron/Windows
- Autenticação e permissões
- Testes e CI

## Testes rápidos
- Verifique rotas:
	- `GET http://127.0.0.1:8000/vision/analyze`
	- `GET http://127.0.0.1:8000/voice/status`
	- `POST http://127.0.0.1:8000/voice/synthesize` (JSON `{ "text": "Olá" }`)
	- `POST http://127.0.0.1:8000/auth/register` (JSON `{ "username": "user", "password": "pass" }`)
	- `POST http://127.0.0.1:8000/auth/login` (JSON `{ "username": "user", "password": "pass" }`)


## Próximos passos sugeridos
1. Integrar STT (Whisper local ou API)
2. Criar fluxo de empacotamento Electron + instalador Windows
3. Melhorar `VisionEngine` com modelos treinados ou templates
