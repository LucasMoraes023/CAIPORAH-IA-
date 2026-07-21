from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import health, vision, voice, memory, game, plugins, conversation, history, auth

app = FastAPI(
    title='GameCopilot AI Backend',
    description='Serviços de visão, voz, memória e IA para o GameCopilot AI.',
    version='0.1.0'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(health.router)
app.include_router(vision.router, prefix='/vision')
app.include_router(voice.router, prefix='/voice')
app.include_router(memory.router, prefix='/memory')
app.include_router(game.router, prefix='/games')
app.include_router(plugins.router, prefix='/plugins')
app.include_router(conversation.router, prefix='/conversation')
app.include_router(history.router, prefix='/history')
app.include_router(auth.router, prefix='/auth')
