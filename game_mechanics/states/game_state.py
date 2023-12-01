from game_mechanics.card_structures.supply_pile import SupplyPile
from game_mechanics.card_structures.trash import Trash
from game_mechanics.states.base_state import BasePublicState
from game_mechanics.supply import Supply


class GameState(BasePublicState):
    """
    The current state of the public elements of the game:
        1. The supply
        2. The trash
        3. Public mats
    """

    def __init__(self, kingdom_piles: list[SupplyPile], standard_piles: list[SupplyPile]):
        self.supply = Supply(kingdom_piles, standard_piles)
        self.trash = Trash(name="Trash")
