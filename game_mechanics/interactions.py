from enum import Enum
from typing import List

from game_mechanics.phases.phases import Phase
from game_mechanics.player.player import Player


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


def do_action_choice(player: Player):
    all_cards = player.cards_alphabetically
    playable_cards = player.get_playable_cards(Phase.ActionPhase)
    print(f"Your hard: {all_cards}")
    print(f"Playable cards: {playable_cards}")
    print(f"Choose the card to play, or type '{CommonChoices.NONE_CHOICE}' for none")
    for i, card in enumerate(playable_cards):
        print(f'{i}. {card.name}')
    valid_choices = [str(i) for i in range(1, len(playable_cards) + 1)] + [CommonChoices.NONE_CHOICE.name]
    answer = _get_player_choice(valid_choices)

    if answer is not CommonChoices.NONE_CHOICE:
        choice = int(answer)
        chosen_card = playable_cards[choice]
        player.play_card(chosen_card)
        self._hand.pop(choice)
        self.play_card(chosen_card)


def play_buy_phase(self):
    print(f'You have {self.coins} coins')
    print()
