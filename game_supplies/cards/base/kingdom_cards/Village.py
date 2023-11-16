from OLD.game_conf.card import Action
from OLD.game_conf.command import Command


class Village(Action):
    def __init__(self):
        super().__init__(name='Village',
                         cost=3,
                         commands=[Command(plus_actions=2),
                                   Command(plus_cards=1)])
