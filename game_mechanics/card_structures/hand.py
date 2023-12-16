from typing import Optional

from game_mechanics.card_structures._card_structure import CardStructure
from game_mechanics.game_supplies.card_types.base_card import BaseCard


class Hand(CardStructure):
    def __init__(self, cards: Optional[list[BaseCard]] = None):
        super().__init__(cards, name="Hand")
