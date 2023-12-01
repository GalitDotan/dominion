from game_mechanics.states.base_state import BasePlayerState


class PlayerTurnState(BasePlayerState):
    """
    The current state of all curr_player's elements that would be discarded/ rebooted at the end of the turn.
    """

    def __init__(self, actions: int = 1, buys: int = 1, coins: int = 0):
        self.actions = actions
        self.buys = buys
        self.coins = coins

    def __repr__(self):
        return f"Actions: {self.actions}, Buys: {self.buys}, Coins: {self.coins}"
