from typing import Callable

from tabulate import tabulate

from consts import HeadlineFormats
from game_mechanics.card_structures.supply_pile import SupplyPile


class Supply:
    """
    Represents all the _standard_piles on the table.
    """

    def __init__(self, kingdom_piles: list[SupplyPile], standard_piles: list[SupplyPile]):
        self._kingdom_piles: list[SupplyPile] = kingdom_piles
        self._standard_piles: list[SupplyPile] = standard_piles
        self._all_piles = {pile.name: pile for pile in self._kingdom_piles + self._standard_piles}

    def __repr__(self):
        return f"""
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
{HeadlineFormats.H1.format("The Supply")}
        
{tabulate({"Kingdom Cards": self._kingdom_piles, "Basic Cards": self._standard_piles},
          headers="keys", showindex="always", tablefmt="fancy_grid")}
        
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        """

    @property
    def piles(self):
        return sorted(self._kingdom_piles + self._standard_piles)

    def get_num_of_empty(self):
        return len(self.empty_piles)

    @property
    def empty_piles(self):
        return [pile for pile in self.piles if pile.is_empty()]

    def get_pile_names_by_condition(self, card_condition: Callable) -> list[str]:
        piles = []
        for pile in self.piles:
            if not pile.is_empty() and card_condition(pile.peak()):
                piles.append(pile.name)
        return piles

    def get_card(self, pile_name: str):
        pile: SupplyPile = self._all_piles[pile_name]
        return pile.draw()
