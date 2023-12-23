from typing import Any

from game_mechanics.effects.effect import Effect
from game_mechanics.effects.move_cards.play_card import PlayCard
from game_mechanics.effects.player_decision import PlayerBooleanDecision
from game_mechanics.game_supplies.card_type import CardType


class AutoplayTreasures(Effect):
    async def apply(self, game, player=None, *args, **kwargs) -> Any:
        do_autoplay: bool = game.apply_effect(PlayerBooleanDecision(), player)
        if do_autoplay:
            for card in player.hand.cards:
                if CardType.TREASURE in card.types and card.should_autoplay():
                    game.apply_effect(PlayCard(card), player)
