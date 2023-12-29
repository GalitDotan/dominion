from typing import Any

from game_mechanics.effects.draw_cards import DrawHand
from game_mechanics.effects.gain_cards import GainCardToDiscard
from game_mechanics.effects.game_stages.phase.phase import Phase
from game_mechanics.game_config.game_conf_consts import ESTATES_AMOUNT_SETUP, COPPERS_AMOUNT_SETUP
from game_mechanics.game_supplies.all_cards import CardInitiator


class SetupPhase(Phase):
    """
    This phase sets up the game.
    """
    DEFAULT_START_CARDS = ((CardInitiator.ESTATE, ESTATES_AMOUNT_SETUP),
                           (CardInitiator.COPPER, COPPERS_AMOUNT_SETUP))

    def __init__(self, cards_to_draw: int = 5, cards_to_gain: tuple[tuple[CardInitiator, int]] = DEFAULT_START_CARDS):
        super().__init__()
        self.cards_to_draw = cards_to_draw
        self.cards_to_gain: tuple[tuple[CardInitiator, int]] = cards_to_gain

    async def apply(self, game, player=None, **kwargs) -> Any:
        """
        Each player gains the start cards and draws cards.
        """
        for player in game.players.values():
            for card, amount in self.cards_to_gain:
                for _ in range(amount):
                    await game.apply_effect(GainCardToDiscard(pile_name=card.name), player)
            await game.apply_effect(DrawHand(self.cards_to_draw), player)
