class TurnState:
    def __init__(self, actions: int = 1, buys: int = 1, coins: int = 0):
        self.actions = actions
        self.buys = buys
        self.coins = coins

    def __repr__(self, long: bool = False):
        return f"Actions: {self.actions}, Buys: {self.buys}, Coins: {self.coins}"
