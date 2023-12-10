from game_mechanics.game_supplies.card_types.card import Card


class AttackCommands:  # TODO: move someplace else
    pass


class Attack(Card):
    def __init__(self, name: str, cost: int, attacks: list[AttackCommands]):
        super().__init__(name, cost)
        self.attacks: list = attacks

    def detailed_repr(self):
        pass
