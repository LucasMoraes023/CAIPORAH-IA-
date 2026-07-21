from typing import Optional
from pydantic import BaseModel


class MemoryCreate(BaseModel):
    user_id: Optional[int]
    category: str
    content: str


class MemoryRead(BaseModel):
    id: int
    user_id: Optional[int]
    category: str
    content: str
    created_at: str

    class Config:
        orm_mode = True


class GameCreate(BaseModel):
    name: str


class GameRead(BaseModel):
    id: int
    name: str
    last_played_at: Optional[str]
    total_play_time: int
    installed: bool

    class Config:
        orm_mode = True


class ConversationCreate(BaseModel):
    user_id: Optional[int]
    game_id: Optional[int]
    message: str
    role: str


class AuthRegister(BaseModel):
    username: str
    password: str
    display_name: Optional[str]


class AuthLogin(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'
