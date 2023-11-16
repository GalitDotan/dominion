from random import shuffle
from typing import List

from game_mechanics.pile import Pile
from game_mechanics.utils.utils import shuffle_copy
from game_supplies.card_types.card import Card, Victory


class Player:
    def __init__(self, cards: List[Card]):
        self._cards: List[Card] = cards  # all cards the player has
        self._draw_pile: Pile = Pile(name='Draw Pile', is_visible=False, cards=shuffle_copy(cards))
        self._discard_pile = Pile(name='Discard Pile', is_visible=True)
        self._hand: List[Card] = self.draw_cards(5)

    @property
    def victory_points(self) -> int:
        return sum([card.victory_points for card in self._cards if type(card) is Victory])

    @property
    def cards_alphabetically(self) -> List[Card]:
        return sorted(self._cards, key=lambda x: x.name)

    def cards_by_value(self) -> List[Card]:
        return sorted(self._cards, key=lambda x: x.value)

    def draw_card(self):
        if self._draw_pile.is_empty():
            cards = self._discard_pile.draw_all()
            shuffle(cards)
            self._discard_pile.put_all(cards)
        return self._draw_pile.draw()

    def draw_cards(self, amount: int):
        return [self.draw_card() for _ in range(amount)]
