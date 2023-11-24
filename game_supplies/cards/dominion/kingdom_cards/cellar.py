from game_mechanics.commands.change_state_command import ChangeStateCommand
from game_supplies.card_types.action_card import Action


class Cellar(Action):
    def __init__(self):
        super().__init__(name='Cellar',
                         cost=2,
                         commands=[ChangeStateCommand(plus_actions=1),
                                   ])
