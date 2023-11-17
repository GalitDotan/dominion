from enum import Enum
from random import shuffle
from typing import List

from game_mechanics.card_structures.hand import Hand
from game_mechanics.phases.phases import Phase
from game_mechanics.card_structures.pile import Pile
from game_mechanics.utils.utils import shuffle_copy
from game_supplies.card_types.card import Card, Duration, Treasure, Action, Attack, Night


class CommonChoices(Enum):
    NONE_CHOICE = 'x'
    UNDO = 'undo'
    HELP_CHOICE = '--help'


def _get_player_choice(valid_choices: List[str]):
    answer = input("Your choice: ")

    help_choice = CommonChoices.HELP_CHOICE.name
    if answer.endswith(help_choice):
        help_request = answer.replace(help_choice, '')
        try:
            eval(f'{help_request}.help()')
        except Exception:
            print(f"I cannot help you with {help_request}")
        return _get_player_choice(valid_choices)
    elif answer not in valid_choices:
        print(f'{answer} is not a valid choice. Please choose one of: {valid_choices}')
        return _get_player_choice(valid_choices)
    else:
        return answer


class Player:
    def __init__(self, cards: List[Card]):
        self._all_cards: List[Card] = cards  # all cards the player has
        self._draw_pile: Pile = Pile(name='Draw Pile', is_visible=False, cards=shuffle_copy(cards))
        self._discard_pile = Pile(name='Discard Pile', is_visible=True)
        self._hand: Hand = Hand(self.draw_cards(5))
        self._played_cards: List[Card] = []
        self._actions = 0
        self._buys = 0
        self._coins = 0
        self._victory_points = 0

    @property
    def cards_alphabetically(self) -> List[Card]:
        return sorted(self._all_cards, key=lambda x: x.name)

    def cards_by_value(self) -> List[Card]:
        return sorted(self._all_cards, key=lambda x: x.value)

    def play_card(self, card: Card):
        if card not in self._hand:
            raise ValueError(f"{card} is not it {self._hand}")
        if type(card) is Treasure:
            self._coins += card.coins
        if type(card) is Action:
            for cmd in card.commands:
                pass
        if type(card) is Attack:
            for cmd in card.attacks:
                pass
        if type(Card) is Night:
            pass

    def draw_card(self):
        if self._draw_pile.is_empty():
            cards = self._discard_pile.draw_all()
            shuffle(cards)
            self._discard_pile.put_all(cards)
        return self._draw_pile.draw()

    def draw_cards(self, amount: int):
        return [self.draw_card() for _ in range(amount)]

    def discard_hand(self):
        self._discard_pile.put_all(self._hand)
        self._hand = []

    def discard_play(self):
        self._discard_pile.put_all(self._played_cards)
        for card in self._played_cards:
            if type(Card) is not Duration:
                self._played_cards.remove(card)
                self._discard_pile.put(card)

    def play_action_phase(self):
        self._hand.sort(key=lambda x: x.name)
        continue_phase = True
        while continue_phase and len(self._hand) > 0:
            self._do_action_choice()

    def _get_playable_cards(self, phase: Phase) -> List[Card]:
        playable = []
        if phase is Phase.ActionPhase:
            playable_types = (Action,)
        elif phase is Phase.BuyPhase:
            playable_types = (Treasure,)
        elif phase is Phase.NightPhase:
            playable_types = (Night,)
        else:
            playable_types = ()

        for card in self._hand:
            for playable_type in playable_types:
                if type(card) is playable_type:
                    playable.append(card)
                    break  # so we'll add each card only once

        return playable

    def _do_action_choice(self):
        print(f"Choose the card to play, or type '{CommonChoices.NONE_CHOICE}' for none")
        for i, card in enumerate(self._hand):
            print(f'{i}. {card.name}')
        print(f'Your hand: {str(self._hand)}')
        valid_choices = [str(i) for i in range(1, len(self._hand) + 1)] + [CommonChoices.NONE_CHOICE.name]
        answer = _get_player_choice(valid_choices)

        if answer is not CommonChoices.NONE_CHOICE:
            choice = int(answer)
            chosen_card = self._hand[choice]
            self._hand.pop(choice)
            self.play_card(chosen_card)

    def play_buy_phase(self):
        print(f'You have {self._coins} coins')
