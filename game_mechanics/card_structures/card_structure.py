from abc import ABC
from collections import Counter
from random import shuffle
from typing import Optional, Callable

from game_mechanics.effects.game_stages.phase.phase import Phase
from game_mechanics.game_supplies.base_card import CardObject


class CardStructure(ABC):
    def __init__(self, cards: Optional[list[CardObject]] = None, name: Optional[str] = None, is_visible: bool = True):
        default_name = cards[0].name if cards and len(cards) > 0 else self.__class__.__name__
        self.name: str = name if name else default_name
        self.cards: list[CardObject] = cards if cards else []
        self.is_visible: bool = is_visible

    def __hash__(self):
        return self.name

    def __repr__(self):
        return f"{self.name}[{len(self)}]"

    def __len__(self):
        return len(self.cards)

    def __iter__(self):
        return self.cards.__iter__()

    def __getitem__(self, item: int):
        return self.cards[item]

    @property
    def visible(self) -> bool:
        return self.is_visible

    @property
    def cards_dict(self) -> dict[CardObject, int]:
        return dict(Counter(self))

    def detailed_repr(self):
        basic_repr = repr(self)
        if not self.is_visible or len(self.cards_dict) <= 1:
            return basic_repr
        return f"{basic_repr}: {self.cards_dict}"

    def is_empty(self) -> bool:
        return len(self.cards) == 0

    def pop(self, i: int):
        self.cards.pop(i)

    def sort(self, key: Optional[Callable] = None):
        if key is not None:
            self.cards.sort(key=key)
        else:
            self.cards.sort()

    def remove_all(self) -> list[CardObject]:
        """
        Remove all the cards from the structure.
        """
        cards = self.cards
        self.cards = []
        return cards

    def remove(self, card: CardObject):
        self.cards.remove(card)

    def remove_cards(self, cards: list[CardObject]):
        for card in cards:
            self.remove(card)

    def append(self, card: CardObject):
        self.cards.append(card)

    def extend(self, cards: list[CardObject]):
        self.cards.extend(cards)

    def shuffle(self):
        """
        Shuffle the cards in the structure.
        """
        shuffle(self.cards)

    def get_cards_for_phase(self, phase: Optional[Phase] = None) -> list[CardObject]:
        """
        Receives a card structure and returns all cards from it that can be played in the given phase.
        Default phase - current.
        """
        return [card for card in self.cards if card.is_playable(phase)]
