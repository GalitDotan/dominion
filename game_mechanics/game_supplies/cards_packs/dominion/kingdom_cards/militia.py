from game_mechanics.effects.attack_effect import AttackEffect
from game_mechanics.effects.increase_stats import IncStats
from game_mechanics.effects.move_cards.discard_cards import DiscardCards
from game_mechanics.game_supplies.base_card import Card
from game_mechanics.game_supplies.card_type import CardType


class Militia(Card):
    """
    +2 Coins
    Each player discards down to 2.
    """

    def __init__(self):
        super().__init__(name='Militia',
                         cost=4,
                         types=CardType.ACTION,
                         action_effects=[IncStats(coins=2),
                                         AttackEffect(attack_type=DiscardCards, attack_conf={'cards_amount': 2})])
