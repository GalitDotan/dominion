from game_mechanics.player.bot_player import BotPlayer
from game_mechanics.game_supplies.card_types.card import Card


def get_bot_player_choice(player: BotPlayer, playable_cards: dict[Card]):
    return max(playable_cards)
