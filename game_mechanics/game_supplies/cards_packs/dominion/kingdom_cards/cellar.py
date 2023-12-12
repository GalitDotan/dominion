from game_mechanics.effects.increase_player_turn_state_counters import IncStateCounter
from game_mechanics.game_supplies.card_types.action_card import Action


class Cellar(Action):
    def __init__(self):
        super().__init__(name='Cellar',
                         cost=2,
                         actions=[IncStateCounter(actions=1)])
