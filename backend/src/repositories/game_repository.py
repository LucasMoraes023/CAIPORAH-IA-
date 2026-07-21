from sqlalchemy.orm import Session
from ..models import Game

class GameRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_games(self) -> list[Game]:
        return self.db.query(Game).all()

    def get_game(self, game_id: int) -> Game | None:
        return self.db.query(Game).filter(Game.id == game_id).first()

    def create_game(self, name: str) -> Game:
        game = Game(name=name)
        self.db.add(game)
        self.db.commit()
        self.db.refresh(game)
        return game
