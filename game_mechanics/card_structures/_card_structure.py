from abc import ABC
from typing import List, Optional, Callable
from collections import Counter

from game_supplies.card_types.card import Card


class CardStructure(ABC):
    def __init__(self, cards: List[Card] = (), name: Optional[str] = None, is_visible: bool = True):
        self.name: str = name if name else cards[0].name
        self._cards: List[Card] = cards
        self._is_visible: bool = is_visible

    def __repr__(self):
        basic_repr = f"{self.name}[{len(self)}]"
        if not self._is_visible:
            return basic_repr
        card_names = sorted([c.name for c in self._cards])
        counter = dict(Counter(card_names))
        if len(counter) <= 1:
            return basic_repr
        return f"{basic_repr}: {counter}"

    def __len__(self):
        return len(self._cards)

    def __iter__(self):
        return self._cards.__iter__()

    def __getitem__(self, item: int):
        return self._cards[item]

    @property
    def visible(self) -> bool:
        return self._is_visible

    @property
    def cards(self) -> List[Card]:
        return self._cards.copy()

    def is_empty(self) -> bool:
        return len(self._cards) == 0

    def pop(self, i: int):
        self._cards.pop(i)

    def sort(self, key: Optional[Callable] = None):
        if key is not None:
            self._cards.sort(key=key)
        else:
            self._cards.sort()
