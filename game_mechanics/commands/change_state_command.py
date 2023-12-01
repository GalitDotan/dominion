from game_mechanics.commands.command import Command
from game_mechanics.states.player_turn_state import PlayerTurnState


class ChangeStateCommand(Command):
    def __init__(self, plus_actions: int = 0, plus_buys: int = 0, plus_coins: int = 0):
        self.plus_actions = plus_actions
        self.plus_buys = plus_buys
        self.plus_coins = plus_coins

    def activate(self, state: PlayerTurnState, *args, **kwargs):
        """
        Increase state parameters.

        :param state: game_stages's state
        """
        state.actions += self.plus_actions
        state.buys += self.plus_buys
        state.coins += self.plus_coins
