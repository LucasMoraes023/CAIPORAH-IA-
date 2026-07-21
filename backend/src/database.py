from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_FILE = Path(__file__).resolve().parents[1] / 'gamecopilot.db'
DATABASE_URL = f'sqlite:///{DATABASE_FILE}'

engine = create_engine(
    DATABASE_URL,
    connect_args={'check_same_thread': False},
    future=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True,
)

Base = declarative_base()


def init_db() -> None:
    DATABASE_FILE.parent.mkdir(parents=True, exist_ok=True)
    Base.metadata.create_all(bind=engine)
