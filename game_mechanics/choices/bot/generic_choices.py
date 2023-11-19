from game_mechanics.choices.common_choices import CommonChoices
from game_mechanics.consts import HeadlineFormats
from game_mechanics.player.bot_player import BotPlayer
from game_mechanics.player.human_player import HumanPlayer
from game_mechanics.player.turn_state import TurnState
from game_supplies.card_types.card import Card


def get_bot_player_choice(player: BotPlayer, turn_state: TurnState, playable_cards: dict[Card]):
    return max(playable_cards)
