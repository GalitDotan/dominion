from game_mechanics.decisions.game_decisions import TrashDecision
from game_mechanics.effects.effect import Effect


class TrashFromHand(Effect):
    def on_activation(self, decision: TrashDecision):
        to_trash = decision.cards
        self.
        self.player.discard_hand()
