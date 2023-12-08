from game_mechanics.effects.effect import Effect
from game_mechanics.game_options.game_options import EmptyOptions
from game_mechanics.player.player import Player
from game_mechanics.states.game_state import GameState


class ShuffleDiscardToDrawPile(Effect):
    def __init__(self):
        super().__init__()

    def on_activation(self, game_state: GameState, decision: EmptyOptions, player: Player):
        """
        Shuffle the discard pile into the draw pile.
        """
        discard_pile = player.state.discard_pile
        draw_pile = player.state.draw_pile
        discard_pile.shuffle()
        cards = discard_pile.draw_all()
        draw_pile.put_all(cards)
