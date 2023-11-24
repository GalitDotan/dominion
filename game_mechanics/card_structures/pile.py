from typing import Optional

from game_mechanics.card_structures._card_structure import CardStructure
from game_supplies.card_types.card import Card


class Pile(CardStructure):
    """
    A stack of _all_cards.
    """

    def __init__(self, cards: list[Card] = (), name: Optional[str] = None, is_visible: bool = True):
        super().__init__(cards, name, is_visible)

    def draw(self) -> Card:
        """
        Draw from the top of the pile.
        """
        return self._cards.pop()

    def draw_all(self) -> list[Card]:
        """
        Draw all the cards from the pile.
        """
        return self.remove_all()

    def put(self, card: Card):
        """
        Put a card on top of the pile.
        """
        self.append(card)

    def put_all(self, cards: list[Card]):
        """
        Put all given cards on top of the pile.
        Last card of the input would become the top card of the pile.
        """
        self.extend(cards)
