from game_mechanics.player.bot_player import BotPlayer
from game_mechanics.player.turn_state import TurnState
from game_supplies.card_types.card import Card


def get_bot_player_choice(player: BotPlayer, turn_state: TurnState, playable_cards: dict[Card]):
    return max(playable_cards)
