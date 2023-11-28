from abc import ABC, abstractmethod


class Card(ABC):
    """
    A card in a game. Stats can be modified
    """

    def __init__(self, name: str, cost: int, default_pile_size: int = 10, is_reveled: bool = False):
        self.name: str = name
        self.cost: int = cost
        self.default_pile_size: int = default_pile_size
        self.is_reveled: bool = is_reveled

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other: 'Card'):
        if self.cost < other.cost:
            return True
        if self.cost > other.cost:
            return False
        return self.name < other.name

    def help(self):
        return str(self)

    @property
    def card_type(self):
        return type(self)  # TODO: show all inherited types

    @abstractmethod
    def detailed_repr(self):
        raise NotImplemented
