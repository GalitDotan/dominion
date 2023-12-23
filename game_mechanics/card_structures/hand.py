from typing import Optional

from game_mechanics.card_structures.card_structure import CardStructure
from game_mechanics.game_supplies.base_card import Card


class Hand(CardStructure):
    def __init__(self, cards: Optional[list[Card]] = None):
        super().__init__(cards, name="Hand")
