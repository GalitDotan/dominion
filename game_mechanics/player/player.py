from random import shuffle
from typing import Optional

from random_word import RandomWords

from game_mechanics.card_structures.hand import Hand
from game_mechanics.card_structures.pile import Pile
from game_mechanics.phases.phases import Phase
from game_mechanics.player.turn_state import TurnState
from game_mechanics.utils.utils import shuffle_copy
from game_supplies.card_types.card import Card
from game_supplies.card_types.night_card import Night
from game_supplies.card_types.duration_card import Duration
from game_supplies.card_types.attack_card import Attack
from game_supplies.card_types.victory_card import Victory
from game_supplies.card_types.treasure_card import Treasure
from game_supplies.card_types.action_card import Action


def _generate_name():
    rw = RandomWords()
    first_name = str(rw.get_random_word()).capitalize()
    last_name = str(rw.get_random_word()).capitalize()
    return f"{first_name}{last_name}"


def _calc_vp(cards: list[Card]) -> int:
    """
    Calc the sum of victory points received by the given cards.
    :param cards: a list of cards.
    :return: sum of victory points.
    """
    vp = 0
    for card in cards:
        if isinstance(card, Victory):
            vp += card.victory_points
    return vp


class Player:
    def __init__(self, cards: list[Card], name: Optional[str] = None):
        self.name = name if name else _generate_name()
        self._all_cards: list[Card] = cards  # all cards the player has

        # player's card structures
        self.draw_pile: Pile = Pile(name='Draw Pile', is_visible=False, cards=shuffle_copy(cards))
        self.discard_pile = Pile(name='Discard Pile', is_visible=True)
        self.hand: Hand = Hand(self.draw_cards(5))
        self.played_cards: list[Card] = []

        # player's stats
        self.victory_points = _calc_vp(cards)
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
        Play a card from players hand and update state accordingly.

        :param card: the card.
        :param turn_state: current turn state.
        """
        if card not in self.hand:
            raise ValueError(f"{card} is not in {self.hand}")

        self.hand.remove(card)

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
        self.discard_pile.put_all(self.played_cards)
        for card in self.played_cards:
            if not isinstance(card, Duration):
                self.played_cards.remove(card)
                self.discard_pile.put(card)

    def get_playable_cards(self, phase: Phase) -> dict[Card, int]:
        """
        Of all the cards in hand - get all the cards that can be played in the given phase.

        :param phase: The phase
        :return: The playable cards.
        """
        playable = {}
        if phase is Phase.ActionPhase:
            playable_types = (Action,)
        elif phase is Phase.BuyPhase:
            playable_types = (Treasure,)
        elif phase is Phase.NightPhase:
            playable_types = (Night,)
        else:
            playable_types = ()

        for card, cnt in self.hand.cards_dict.items():
            for playable_type in playable_types:
                if isinstance(card, playable_type):
                    playable[card] = cnt

        return playable
