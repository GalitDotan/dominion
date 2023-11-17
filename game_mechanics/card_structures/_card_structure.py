from abc import ABC
from typing import List, Optional

from game_supplies.card_types.card import Card


class CardStructure(ABC):
    def __init__(self, cards: List[Card] = (), name: Optional[str] = None, is_visible: bool = True):
        self._name: str = name if name else cards[0].name
        self._cards: List[Card] = cards
        self._is_visible: bool = is_visible

    def __repr__(self):
        if not self._is_visible:
            return f"{self._name}[{self.size}]"
        card_names = sorted([c.name for c in self._cards])
        return f"{self._name}[{self.size}]: {card_names}"

    @property
    def size(self):
        return len(self._cards)

    @property
    def visible(self) -> bool:
        return self._is_visible

    def is_empty(self) -> bool:
        return len(self._cards) == 0
