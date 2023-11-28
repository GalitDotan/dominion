from typing import Optional

from consts import DEFAULT_PILE_SIZE, FIRST_GAME_CARDS, STANDARD_CARDS
from game_mechanics.card_structures.supply_pile import SupplyPile
from game_mechanics.card_structures.trash import Trash
from game_mechanics.supply import Supply


class GameState:
    def __init__(self, kingdom_piles: list[SupplyPile], standard_piles: list[SupplyPile]):
        self.supply = Supply(kingdom_piles, standard_piles)
        self.trash = Trash(name="Trash")


class PlayerState:
    pass
