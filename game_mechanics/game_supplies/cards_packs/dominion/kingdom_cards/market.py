from game_mechanics.effects.increase_stats import IncStats
from game_mechanics.effects.move_cards.draw_num_cards import DrawNum
from game_mechanics.game_supplies.base_card import BaseCard
from game_mechanics.game_supplies.card_type import CardType


class Market(BaseCard):
    """
    +1 Card
    +1 Action
    +1 Buy
    +1 Coin
    """

    def __init__(self):
        super().__init__(name='Market',
                         cost=5,
                         types=CardType.ACTION,
                         action_effects=[DrawNum(num=1),
                                         IncStats(coins=1, actions=1, buys=1)])
