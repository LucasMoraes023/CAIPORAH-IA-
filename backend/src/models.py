from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text, func
from .database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(128), unique=True, nullable=False)
    display_name = Column(String(128), nullable=True)
    password_hash = Column(String(256), nullable=True)
    role = Column(String(64), nullable=False, default='user')
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Setting(Base):
    __tablename__ = 'settings'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    key = Column(String(128), nullable=False)
    value = Column(Text, nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=False)
    last_played_at = Column(DateTime(timezone=True), nullable=True)
    total_play_time = Column(Integer, nullable=False, default=0)
    installed = Column(Boolean, nullable=False, default=False)


class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey('games.id'), nullable=True)
    event_type = Column(String(128), nullable=False)
    description = Column(Text, nullable=True)
    detected_at = Column(DateTime(timezone=True), server_default=func.now())


class Conversation(Base):
    __tablename__ = 'conversations'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    game_id = Column(Integer, ForeignKey('games.id'), nullable=True)
    message = Column(Text, nullable=False)
    role = Column(String(32), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class History(Base):
    __tablename__ = 'history'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    game_id = Column(Integer, ForeignKey('games.id'), nullable=True)
    action = Column(String(256), nullable=False)
    details = Column(Text, nullable=True)
    occurred_at = Column(DateTime(timezone=True), server_default=func.now())


class Plugin(Base):
    __tablename__ = 'plugins'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=False)
    version = Column(String(64), nullable=False)
    enabled = Column(Boolean, nullable=False, default=True)
    installed_at = Column(DateTime(timezone=True), server_default=func.now())


class MemoryItem(Base):
    __tablename__ = 'memory'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    category = Column(String(128), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Statistic(Base):
    __tablename__ = 'statistics'

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey('games.id'), nullable=True)
    metric = Column(String(128), nullable=False)
    value = Column(Float, nullable=False)
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())
