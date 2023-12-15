from typing import Optional

from game_mechanics.card_structures.supply_pile.supply_pile import SupplyPile
from game_mechanics.game_consts import DEFAULT_PILE_SIZE


# TODO: change input to list[tuple(Card, int]]
def generate_supply_piles(supply_card_types: tuple,
                          supply_pile_sizes: Optional[tuple[int, ...]] = None) -> list[SupplyPile]:
    """
    Receives a list of card types and the size of each pile.

    Returns:
        A list of supply piles.
    """
    supply_pile_sizes = supply_pile_sizes if supply_pile_sizes else [DEFAULT_PILE_SIZE for _ in
                                                                     range(len(supply_card_types))]
    return [SupplyPile(cards=[card_type() for _ in range(pile_size)]) for card_type, pile_size in
            zip(supply_card_types, supply_pile_sizes)]
