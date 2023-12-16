from game_mechanics.game_supplies.card_types.base_card import BaseCard


class AttackCommands:  # TODO: move someplace else
    pass


class AttackCard(BaseCard):

    def __init__(self, name: str, cost: int, attacks: list[AttackCommands]):
        super().__init__(name, cost)
        self.attacks: list = attacks

    def detailed_repr(self):
        pass
