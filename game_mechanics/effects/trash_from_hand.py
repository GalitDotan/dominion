from game_mechanics.effects.effect import Effect
from game_mechanics.game_options.name_options import CheckboxOptions


class TrashFromHand(Effect):
    def on_activation(self, game: CheckboxOptions, player):
        to_trash = decision.cards
        self.player.discard_hand()
