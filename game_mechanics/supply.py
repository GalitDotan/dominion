from typing import List

from game_mechanics.card_structures.pile import Pile
from game_mechanics.card_structures.supply_pile import SupplyPile


class Supply:
    """
    Represents all the _other_piles on the table.
    """

    def __init__(self, kingdom_piles: List[SupplyPile], other_piles: List[SupplyPile]):
        self._kingdom_piles: List[SupplyPile] = sorted(kingdom_piles)
        self._other_piles: List[SupplyPile] = sorted(other_piles)

    def __repr__(self):
        kingdom_piles = '\r\n\t\t\t*  '.join([str(pile) for pile in self._kingdom_piles])
        other_piles = '\r\n\t\t\t*  '.join([str(pile) for pile in self._other_piles])
        return f"""
        $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        $$$$$$$$$$$$$$$$$$$$$$$  The Supply  $$$$$$$$$$$$$$$$$$$$$$
        
            *  {kingdom_piles}
            
            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            
            *  {other_piles}
        
        $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        """

    @property
    def piles(self):
        return sorted(self._kingdom_piles + self._other_piles)

    def get_num_of_empty(self):
        return len(self.empty_piles)

    @property
    def empty_piles(self):
        return [pile for pile in self.piles if pile.is_empty()]
