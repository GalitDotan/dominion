from enum import Enum
from typing import List, Tuple

from game_mechanics.phases.phases import Phase
from game_mechanics.player.player import Player
from game_supplies.card_types.card import Card


class CommonChoices(Enum):
    NONE_CHOICE = 'x'
    UNDO = 'undo'
    HELP_CHOICE = '--help'


def get_player_choice(valid_choices: List[str], message: str):
    print(message)
    for i, card_name in enumerate(valid_choices):
        print(f'{i}. {card_name}')
    answer = input("Your choice: ")

    help_choice = CommonChoices.HELP_CHOICE.name
    if answer.endswith(help_choice):
        help_request = answer.replace(help_choice, '')
        try:
            eval(f'{help_request}.help()')
        except Exception:
            print(f"I cannot help you with {help_request}")
        return get_player_choice(valid_choices, message)
    elif answer not in valid_choices:
        print(f'{answer} is not a valid choice. Please choose one of: {valid_choices}')
        return get_player_choice(valid_choices, message)
    else:
        return answer


def get_player_multy_choice(valid_choices: List[str], message: str) -> List[str]:
    print(message)
    for i, card_name in enumerate(valid_choices):
        print(f'{i}. {card_name}')
    answers = input("Your choices: ")
    if answers is CommonChoices.NONE_CHOICE:
        return [CommonChoices.NONE_CHOICE.name]
    return answers.split()


def choose_cards_from_hand(player: Player) -> List[Card]:
    cards = player.hand.cards
    hand_cards = [card.name for card in cards]
    answer = get_player_multy_choice(hand_cards, "Choose which cards to ")
    removed_cards = []
    for i in answer:
        card = cards[int(i)]
        player.hand.remove(card)
        removed_cards.append(card)
    return removed_cards


def display_choices_from_hand(player: Player, phase: Phase) -> Tuple[List[Card], List[str], str]:
    all_cards = player.cards_alphabetically
    playable_cards = player.get_playable_cards(phase)
    print(f"Your hard: {all_cards}")
    print(f"Playable cards: {playable_cards}")
    message = f"Choose the card to play, or type '{CommonChoices.NONE_CHOICE}' for none"
    valid_choices = [str(i) for i in range(1, len(playable_cards) + 1)] + [CommonChoices.NONE_CHOICE.name]
    return playable_cards, valid_choices, message
