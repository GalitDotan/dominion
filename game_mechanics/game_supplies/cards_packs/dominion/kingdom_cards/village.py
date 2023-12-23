from game_mechanics.effects.draw_cards import DrawCards
from game_mechanics.effects.increase_stats import IncStats
from game_mechanics.game_supplies.base_card import Card
from game_mechanics.game_supplies.card_type import CardType


class Village(Card):
    def __init__(self):
        super().__init__(name='Village',
                         cost=3,
                         types=CardType.ACTION,
                         action_effects=[DrawCards(amount=1),
                                         IncStats(actions=2)])
