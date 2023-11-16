from abc import ABC, abstractmethod
from copy import deepcopy


class Card(ABC):
    """
    A card in a game. Stats can be modified
    """

    def __init__(self, name: str, cost: int, default_pile_size: int = 10, is_reveled: bool = False):
        self.name: str = name
        self.cost: int = cost
        self.default_pile_size: int = default_pile_size
        self.is_reveled: bool = is_reveled

    @abstractmethod
    def __repr__(self):
        raise NotImplementedError()

    def __eq__(self, other):
        return self.name == other._name

    def __lt__(self, other: 'Card'):
        if self.cost < other.cost:
            return True
        if self.cost > other.cost:
            return False
        return self.name < other.name

    @property
    def type(self):
        types = [t for t in ALL_CARD_TYPES if type(self) is t]
        if len(types) == 1:
            return str(types[0])
        return ' - '.join([str(t) for t in types])


class Action(Card):

    def __init__(self, name: str, cost: int, commands: list):
        super().__init__(name, cost)
        self.commands: list = commands

    def __repr__(self):
        return f"""
                ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                ### {self.name} ###

                # Type: {self.type}
                # Cost: {self.cost}

                {self.description}

                ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                """

    @property
    def description(self):
        return "\n".join([str(c) for c in self.commands])


class Treasure(Card):

    def __init__(self, name: str, cost: int, coins: int):
        super().__init__(name, cost)
        self.coins = coins

    def __repr__(self):
        return f"""
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        ### {self.name} ###

        # Type: {self.type}
        # Cost: {self.cost}

        ~ {self.coins} ~

        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        """

    def play(self):
        return self.coins


class Curse(Card):
    def __init__(self, name: str = 'Curse', cost: int = 0):
        super().__init__(name, cost)
        self.vp = -1

    def __repr__(self):
        return f"""
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        ### Curse ###

        # Type: {self.type}
        # Cost: {self.cost}

        ~ {self.vp} VP ~

        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        """


class Victory(Card):

    def __init__(self, name, cost, vp, *args, **kwargs):
        super().__init__(name=name, cost=cost, *args, **kwargs)
        self._vp = vp

    def __repr__(self):
        return f"""
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        ### {self.name} ###

        # Type: {self.type}
        # Cost: {self.cost}

        ~ {self._vp} VP ~

        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        """

    @property
    def victory_points(self):
        return self._vp


class Reaction(Card):
    def __repr__(self):
        pass


class Attack(Card):
    def __repr__(self):
        pass


ALL_CARD_TYPES = (Action, Treasure, Curse, Reaction, Attack)
