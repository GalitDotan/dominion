from game_mechanics.effects.effect import Effect
from game_mechanics.game_options.game_options import CardsOptions


class TrashFromHand(Effect):
    def on_activation(self, game_state: CardsOptions, player):
        to_trash = decision.cards
        self.player.discard_hand()
