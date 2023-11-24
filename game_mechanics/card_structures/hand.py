from game_mechanics.card_structures._card_structure import CardStructure
from game_supplies.card_types.card import Card


class Hand(CardStructure):
    def __init__(self, cards: list[Card]):
        super().__init__(cards, name="Hand")
