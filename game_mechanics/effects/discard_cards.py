from base_decision import BaseDecision
from game_mechanics.effects.effect import Effect
from game_mechanics.states.game_state import GameState


class DiscardCard(Effect):
    def on_activation(self, game_state: GameState, decision: BaseDecision):
        pass


class DiscardCards(Effect):
    def on_activation(self, game_state: GameState, decision: BaseDecision):
        pass


class DiscardHand(Effect):
    def on_activation(self, game_state: GameState, decision=None):
        pass
