from sqlalchemy.orm import Session
from ..repositories.game_repository import GameRepository

class GameService:
    def __init__(self, db: Session) -> None:
        self.repository = GameRepository(db)

    def list_games(self) -> list:
        return self.repository.list_games()

    def create_game(self, name: str):
        return self.repository.create_game(name)
