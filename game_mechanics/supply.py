from tabulate import tabulate

from game_mechanics.card_structures.supply_pile import SupplyPile
from game_mechanics.consts import HeadlineFormats
from game_mechanics.game_supplies.card_types.card import Card


def buy(pile: SupplyPile) -> Card:
    return pile.draw()


class Supply:
    """
    Represents all the _other_piles on the table.
    """

    def __init__(self, kingdom_piles: list[SupplyPile], other_piles: list[SupplyPile]):
        self._kingdom_piles: list[SupplyPile] = sorted(kingdom_piles)
        self._other_piles: list[SupplyPile] = sorted(other_piles)

    def __repr__(self):
        kingdom_piles = '\r\n\t\t\t*  '.join([str(pile) for pile in self._kingdom_piles])
        other_piles = '\r\n\t\t\t*  '.join([str(pile) for pile in self._other_piles])
        table = [kingdom_piles, other_piles]
        return f"""
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
{HeadlineFormats.H1.format("The Supply")}
        
{tabulate({"Kingdom Cards": self._kingdom_piles, "Basic Cards": self._other_piles}, headers="keys", showindex="always", tablefmt="fancy_grid")}
        
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

    def get_piles_allowed_for_buy(self, max_cost: int = 1000) -> list[SupplyPile]:
        piles = []
        for pile in self.piles:
            if not pile.is_empty() and pile.cost <= max_cost:
                piles.append(pile)
        return piles
