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

    @abstractmethod
    def __repr__(self, long: bool = False):
        raise NotImplementedError()

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
        types = [t for t in ALL_CARD_TYPES if isinstance(self, t)]
        if len(types) == 1:
            return str(types[0])
        return ' - '.join([str(t) for t in types])


class Action(Card):

    def __init__(self, name: str, cost: int, commands: list):
        super().__init__(name, cost)
        self.commands: list = commands

    def __repr__(self, long: bool = False):
        if long:
            return f"""
                    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    ### {self.name} ###
    
                    # Type: {self.card_type}
                    # Cost: {self.cost}
    
                    {self.description}
    
                    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    """
        else:
            return self.name

    @property
    def description(self):
        return "\n".join([str(c) for c in self.commands])


class Treasure(Card):

    def __init__(self, name: str, cost: int, coins: int, automatic_play: bool = True, *args, **kwargs):
        super().__init__(name, cost, *args, **kwargs)
        self.coins = coins
        self.automatic_play: bool = automatic_play

    def __repr__(self, long: bool = False):
        if long:
            return f"""
            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            ### {self.name} ###
    
            # Type: {self.card_type}
            # Cost: {self.cost}
    
            ~ {self.coins} ~
    
            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            """
        else:
            return self.name

    def play(self):
        return self.coins


class Curse(Card):
    def __init__(self, name: str = 'Curse', cost: int = 0):
        super().__init__(name, cost)
        self.vp = -1

    def __repr__(self, long: bool = False):
        if long:
            return f"""
            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            ### Curse ###
    
            # Type: {self.card_type}
            # Cost: {self.cost}
    
            ~ {self.vp} VP ~
    
            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            """
        else:
            return self.name


class Victory(Card):

    def __init__(self, name: str, cost: int, vp: int, *args, **kwargs):
        super().__init__(name=name, cost=cost, *args, **kwargs)
        self._vp: int = vp

    def __repr__(self, long: bool = False):
        if long:
            return f"""
            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            ### {self.name} ###
    
            # Type: {self.card_type}
            # Cost: {self.cost}
    
            ~ {self._vp} VP ~
    
            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            """
        else:
            return self.name

    @property
    def victory_points(self):
        return self._vp


class Reaction(Card):
    def __repr__(self, long: bool = False):
        pass


class AttackCommands:  # TODO: move someplace else
    pass


class Attack(Card):
    def __init__(self, name: str, cost: int, attacks: list[AttackCommands]):
        super().__init__(name, cost)
        self.attacks: list = []

    def __repr__(self, long: bool = False):
        pass


class Duration(Card):

    def __repr__(self, long: bool = False):
        pass


class Night(Card):

    def __repr__(self, long: bool = False):
        pass


ALL_CARD_TYPES = (Action, Treasure, Curse, Reaction, Attack, Duration, Night)
