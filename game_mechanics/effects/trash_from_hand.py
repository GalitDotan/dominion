from game_mechanics.effects.effect import Effect
from game_mechanics.game_options.game_decisions import CardsOptions


class TrashFromHand(Effect):
    def on_activation(self, decision: CardsOptions):
        to_trash = decision.cards
        self.player.discard_hand()
