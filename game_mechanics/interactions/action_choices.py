from typing import Any, List

from game_mechanics.interactions.general_choices import CommonChoices, get_player_choice, choose_cards_from_hand, \
    display_choices_from_hand
from game_mechanics.phases.phases import Phase
from game_mechanics.player.player import Player
from game_mechanics.player.turn_state import TurnState


def do_action_choice(player: Player, turn_state: TurnState):
    playable_cards, message = display_choices_from_hand(player, phase=Phase.ActionPhase)
    playable_cards_keys = list(playable_cards.keys())
    valid_choices = [CommonChoices.NONE_CHOICE.name] + [str(card) for card in playable_cards_keys]
    answer = get_player_choice(valid_choices, message)

    if answer is not CommonChoices.NONE_CHOICE:
        choice = int(answer)
        chosen_card = playable_cards_keys[choice - 1]
        player.play_card_from_hand(chosen_card, turn_state)


def choose_cards_to_discard(player: Player):
    removed_cards = choose_cards_from_hand(player)
    player.discard_pile.put_all(removed_cards)
