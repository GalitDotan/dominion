from game_mechanics.effects.draw_cards import Draw
from game_mechanics.effects.effect import Effect
from game_mechanics.game_options.name_options import CheckboxOptions
from game_mechanics.game_options.range_options import RangeOptions
from game_mechanics.states.game_state import GameState


class DiscardThenDraw(Effect):
    """
    DiscardCard cards by decision, then draw as many.
    """

    def __init__(self):
        super().__init__(followup_effect=Draw())

    def on_activation(self, game_state: GameState, decision: CheckboxOptions, player):
        to_discard = decision.cards
        game_state.curr_player.discard(to_discard)
        return RangeOptions(len(to_discard))
