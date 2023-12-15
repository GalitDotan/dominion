from game_mechanics.effects.effect import Effect
from game_mechanics.game_options.name_options import CheckboxOptions
from game_mechanics.states.game import Game


class PlayCard(Effect):
    def on_activation(self, game: Game, options: CheckboxOptions, player: Player):
        for card in options.chosen_cards:
            player.state.play_area.play(card)
