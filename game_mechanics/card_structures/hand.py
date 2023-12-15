from typing import Optional

from game_mechanics.card_structures._card_structure import CardStructure
from game_mechanics.game_supplies.card_types.card_type import CardType


class Hand(CardStructure):
    def __init__(self, cards: Optional[list[CardType]] = None):
        super().__init__(cards, name="Hand")
