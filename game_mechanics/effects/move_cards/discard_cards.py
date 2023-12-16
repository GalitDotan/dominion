from game_mechanics.effects.effect import Effect
from game_mechanics.player.game import Game
from options import Options


class DiscardCard(Effect):
    def on_activation(self, game: Game, options: Options, player: Player):
        pass


class DiscardCards(Effect):
    def on_activation(self, game: Game, options: Options, player: Player):
        pass


class DiscardHand(Effect):
    def on_activation(self, game: Game, options: Options, player: Player):
        pass
