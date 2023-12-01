from uuid import uuid4

from pydantic import BaseModel, Field

from consts import MIN_PLAYERS, MAX_PLAYERS
from game_mechanics.game import Game
from game_mechanics.game_supplies.card_types.card import Card
from game_mechanics.game_supplies.cards_packs.dominion.standard_cards.Copper import Copper
from game_mechanics.game_supplies.cards_packs.dominion.standard_cards.Estate import Estate
from game_mechanics.player.player import Player


def get_default_player_cards() -> list[Card]:
    """
    Get default cards: 7 Coppers and 3 Estates.
    """
    coppers: list[Card] = [Copper() for _ in range(7)]
    estates: list[Card] = [Estate() for _ in range(3)]
    return coppers + estates


class GameInitiator(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    game_id: str = Field(default_factory=lambda: uuid4())
    num_players: int = Field(ge=MIN_PLAYERS, le=MAX_PLAYERS, exclude=True)
    start_cards: list[Card] = Field(default_factory=lambda: get_default_player_cards())
    players: list[Player] = Field(default=())

    def __hash__(self):
        return self.id

    def __eq__(self, other):
        return self.id == other.id

    @property
    def ready(self) -> bool:
        """
        Returns if the game is ready to start.
        """
        return self._num_players == len(self.players)

    def add_player(self, name: str):
        """
        Adding a new player to the game.

        :param name: the player's name
        """
        if self.num_players == MAX_PLAYERS:
            raise ValueError('This game is already full')
        self.players.append(Player(cards=self.start_cards, name=name))

    def init_game(self) -> Game:
        if not self.ready:
            raise AttributeError(
                f'Not enough players in the game. Expected {self.num_players} players, but has {len(self.players)}')
        return Game(**dict(self))
