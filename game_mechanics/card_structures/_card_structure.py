from abc import ABC
from collections import Counter
from random import shuffle
from typing import Optional, Callable

from game_mechanics.game_supplies.card_types.base_card import BaseCard


class CardStructure(ABC):
    def __init__(self, cards: Optional[list[BaseCard]] = None, name: Optional[str] = None, is_visible: bool = True):
        default_name = cards[0].name if cards and len(cards) > 0 else self.__class__.__name__
        self.name: str = name if name else default_name
        self._cards: list[BaseCard] = cards if cards else []
        self._is_visible: bool = is_visible

    def __hash__(self):
        return self.name

    def __repr__(self):
        return f"{self.name}[{len(self)}]"

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
    def cards(self) -> list[BaseCard]:
        return self._cards.copy()

    @property
    def cards_dict(self) -> dict[BaseCard, int]:
        # card_names = sorted([c.name for c in self._cards]) # TODO: make sure this is not necessary, then remove
        return dict(Counter(self))

    def detailed_repr(self):
        basic_repr = repr(self)
        if not self._is_visible or len(self.cards_dict) <= 1:
            return basic_repr
        return f"{basic_repr}: {self.cards_dict}"

    def is_empty(self) -> bool:
        return len(self._cards) == 0

    def pop(self, i: int):
        self._cards.pop(i)

    def sort(self, key: Optional[Callable] = None):
        if key is not None:
            self._cards.sort(key=key)
        else:
            self._cards.sort()

    def remove_all(self) -> list[BaseCard]:
        """
        Remove all the cards from the structure.
        """
        cards = self._cards
        self._cards = []
        return cards

    def remove(self, card: BaseCard):
        self._cards.remove(card)

    def append(self, card: BaseCard):
        self._cards.append(card)

    def extend(self, cards: list[BaseCard]):
        self._cards.extend(cards)

    def shuffle(self):
        """
        Shuffle the cards in the structure.
        """
        shuffle(self._cards)
