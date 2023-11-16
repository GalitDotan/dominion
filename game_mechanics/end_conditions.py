from typing import Tuple

from game_mechanics.supply import Supply
from game_supplies.card_types.card import Card
from game_supplies.cards.base.basic_supply_cards.Province import Province

DEFAULT_FINISH_PILES = (Province().name,)

EMPTY_PILES_FOR_FINISH_BY_NUM_PLAYERS = {
    2: 3,
    3: 3,
    4: 3,
    5: 4,
    6: 4
}


def _is_enough_empty_piles(supply: Supply, compare_to: int = 3) -> bool:
    return supply.get_num_of_empty() >= compare_to


def _is_any_of_finishing_piles_empty(supply: Supply, finishing_piles: Tuple[str] = DEFAULT_FINISH_PILES) -> bool:
    empty_pile_names = [pile._name for pile in supply.empty_piles]
    for pile in finishing_piles:
        if pile in empty_pile_names:
            return True
    return False


def game_over(supply: Supply, num_players: int, finishing_piles: Tuple[str] = DEFAULT_FINISH_PILES) -> bool:
    empty_piles_for_finish = EMPTY_PILES_FOR_FINISH_BY_NUM_PLAYERS[num_players]
    return _is_enough_empty_piles(supply, empty_piles_for_finish) or \
        _is_any_of_finishing_piles_empty(supply, finishing_piles)
