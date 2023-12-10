from game_mechanics.effects.effect import Effect
from game_mechanics.game_options.game_options import CardsOptions
from game_mechanics.player.player import Player
from game_mechanics.states.game_state import GameState


class PlayCard(Effect):
    def on_activation(self, game_state: GameState, options: CardsOptions, player: Player):
        for card in options.chosen_cards:
            player.state.play_area.play(card)
