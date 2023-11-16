from typing import List, Optional

from game_supplies.card_types.card import Card


class Pile:
    """
    A stack of _cards.
    """

    def __init__(self, cards: List[Card] = (), name: Optional[str] = None, is_visible: bool = True):
        self._name: str = name if name else cards[0].name
        self._cards: List[Card] = cards
        self._is_visible: bool = is_visible

    def is_empty(self) -> bool:
        return len(self._cards) == 0

    def draw(self) -> Card:
        return self._cards.pop()

    def draw_all(self) -> List[Card]:
        cards = self._cards
        self._cards = []
        return cards

    def put(self, card: Card):
        self._cards.append(card)

    def put_all(self, cards: List[Card]):
        self._cards.extend(cards)

    @property
    def visible(self) -> bool:
        return self._is_visible
