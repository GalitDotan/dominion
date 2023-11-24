from game_mechanics.choices.bot.generic_choices import get_bot_player_choice
from game_mechanics.choices.common_choices import CommonChoices
from game_mechanics.choices.human.generic_choices import display_choices_from_human_hand, get_human_player_choice

from game_mechanics.phases.phases import PhaseName
from game_mechanics.player.bot_player import BotPlayer
from game_mechanics.player.human_player import HumanPlayer
from game_mechanics.player.player import Player
from game_mechanics.player.turn_state import TurnState


def play_action_by_choice(player: Player, turn_state: TurnState) -> bool:
    """
    Choose an action to play

    :param player: current player
    :param turn_state: current state
    :return: Was a change made?
    """
    playable_cards = player.get_playable_cards(PhaseName.ActionPhase)
    playable_cards_keys = list(playable_cards.keys())
    valid_choices = [CommonChoices.NONE_CHOICE.name] + [str(card) for card in playable_cards_keys]
    if isinstance(player, BotPlayer):
        chosen_card = get_bot_player_choice(player, turn_state, playable_cards)
    else:
        player: HumanPlayer
        display_choices_from_human_hand(player, phase=PhaseName.ActionPhase)
        answer = get_human_player_choice(valid_choices)

        if answer is CommonChoices.NONE_CHOICE:
            return False
        choice = int(answer)
        chosen_card = playable_cards_keys[choice - 1]
    player.play_card_from_hand(chosen_card, turn_state)
    return True
