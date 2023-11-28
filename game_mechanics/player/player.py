from random import shuffle
from typing import Optional

from random_word import RandomWords

from game_mechanics.card_structures.hand import Hand
from game_mechanics.card_structures.pile import Pile
from game_mechanics.card_structures.play_area import PlayArea
from game_mechanics.player.turn_state import TurnState
from game_mechanics.utils.utils import shuffle_copy
from game_mechanics.game_supplies.card_types.action_card import Action
from game_mechanics.game_supplies.card_types.attack_card import Attack
from game_mechanics.game_supplies.card_types.card import Card
from game_mechanics.game_supplies.card_types.night_card import Night
from game_mechanics.game_supplies.card_types.treasure_card import Treasure
from game_mechanics.game_supplies.card_types.victory_card import Victory


def _generate_name():
    rw = RandomWords()
    first_name = str(rw.get_random_word()).capitalize()
    last_name = str(rw.get_random_word()).capitalize()
    return f"{first_name}{last_name}"


def _calc_vp(cards: list[Card]) -> int:
    """
    Calc the sum of victory points received by the given cards_packs.
    :param cards: a list of cards_packs.
    :return: sum of victory points.
    """
    vp = 0
    for card in cards:
        if isinstance(card, Victory):
            vp += card.victory_points
    return vp


class Player:
    """
    This class contains all the cards_packs the player currently has.
    """

    def __init__(self, cards: list[Card], name: Optional[str] = None):
        self.name = name if name else _generate_name()
        self._all_cards: list[Card] = cards.copy()  # all cards_packs the player has

        # player's card structures
        self.draw_pile: Pile = Pile(name='Draw Pile', is_visible=False, cards=shuffle_copy(cards))
        self.discard_pile = Pile(name='Discard Pile', is_visible=True)
        self.hand: Hand = Hand(self.draw_cards(5))
        self.play_area = PlayArea()

        # player's stats
        self.victory_points = _calc_vp(self._all_cards)
        self.turns_played = 0

    def __repr__(self):
        return f"{self.name}[{self.victory_points} VP]: {self.hand}, {self.draw_pile}, {self.discard_pile}"

    def __lt__(self, other: "Player"):  # is self losing to other
        return self.victory_points < other.victory_points or (
                self.victory_points == other.victory_points and self.turns_played >= other.turns_played)

    def __eq__(self, other: "Player"):
        return self.victory_points == other.victory_points

    def __gt__(self, other: "Player"):  # is self winning other
        return self.victory_points > other.victory_points or (
                self.victory_points == other.victory_points and self.turns_played < other.turns_played)

    def get_board_view(self) -> str:
        pass  # TODO: get view

    def detailed_repr(self):
        return f"{self.name}[{self.victory_points} VP]: {self.hand.detailed_repr()}, " \
               f"{self.draw_pile.detailed_repr()}, {self.discard_pile.detailed_repr()}"

    @property
    def cards_alphabetically(self) -> list[Card]:
        return sorted(self._all_cards, key=lambda x: x.name)

    def cards_by_value(self) -> list[Card]:
        return sorted(self._all_cards, key=lambda x: x.value)

    def play_card_from_hand(self, card: Card, turn_state: TurnState):
        """
        Play a card from _play_order hand and update state accordingly.

        :param card: the card.
        :param turn_state: current game_stages state.
        """
        if card not in self.hand:
            raise ValueError(f"{card} is not in {self.hand}")

        self.hand.remove(card)
        self.play_area.play(card)

        if isinstance(card, Treasure):
            turn_state.coins += card.coins
        if isinstance(card, Action):
            for cmd in card.commands:
                pass
        if isinstance(card, Attack):
            for cmd in card.attacks:
                pass
        if isinstance(card, Night):
            pass

    def draw_card(self):
        if self.draw_pile.is_empty():
            cards = self.discard_pile.draw_all()
            shuffle(cards)
            self.discard_pile.put_all(cards)
        return self.draw_pile.draw()

    def draw_cards(self, amount: int):
        return [self.draw_card() for _ in range(amount)]

    def discard_hand(self):
        cards = self.hand.remove_all()
        self.discard_pile.put_all(cards)

    def discard_play(self):
        cards = self.play_area.do_cleanup()
        self.discard_pile.put_all(cards)
