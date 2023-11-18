from random import shuffle
from typing import List

from game_mechanics.card_structures.hand import Hand
from game_mechanics.card_structures.pile import Pile
from game_mechanics.phases.phases import Phase
from game_mechanics.utils.utils import shuffle_copy
from game_supplies.card_types.card import Card, Duration, Treasure, Action, Attack, Night


class Player:
    def __init__(self, cards: List[Card]):
        self._all_cards: List[Card] = cards  # all cards the player has

        # player's card structures
        self.draw_pile: Pile = Pile(name='Draw Pile', is_visible=False, cards=shuffle_copy(cards))
        self.discard_pile = Pile(name='Discard Pile', is_visible=True)
        self.hand: Hand = Hand(self.draw_cards(5))
        self.played_cards: List[Card] = []

        # player's stats
        self.victory_points = 0

    @property
    def cards_alphabetically(self) -> List[Card]:
        return sorted(self._all_cards, key=lambda x: x.name)

    def cards_by_value(self) -> List[Card]:
        return sorted(self._all_cards, key=lambda x: x.value)

    def play_card(self, card: Card):
        if card not in self.hand:
            raise ValueError(f"{card} is not it {self.hand}")

        self.hand.remove(card)

        if type(card) is Treasure:
            self.coins += card.coins
        if type(card) is Action:
            for cmd in card.commands:
                pass
        if type(card) is Attack:
            for cmd in card.attacks:
                pass
        if type(Card) is Night:
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
        self.discard_pile.put_all(self.hand.cards)
        self.hand = []

    def discard_play(self):
        self.discard_pile.put_all(self.played_cards)
        for card in self.played_cards:
            if type(Card) is not Duration:
                self.played_cards.remove(card)
                self.discard_pile.put(card)

    def get_playable_cards(self, phase: Phase) -> List[Card]:
        """
        Of all the cards in hand - get all the cards that can be played in the given phase.

        :param phase: The phase
        :return: The playable cards.
        """
        playable = []
        if phase is Phase.ActionPhase:
            playable_types = (Action,)
        elif phase is Phase.BuyPhase:
            playable_types = (Treasure,)
        elif phase is Phase.NightPhase:
            playable_types = (Night,)
        else:
            playable_types = ()

        for card in self.hand:
            for playable_type in playable_types:
                if type(card) is playable_type:
                    playable.append(card)
                    break  # so we'll add each card only once

        return playable
