from typing import List

from game_mechanics.card_structures.pile import Pile


class Supply:
    """
    Represents all the _other_piles on the table.
    """

    def __init__(self, kingdom_piles: List[Pile], other_piles: List[Pile]):
        self._kingdom_piles: List[Pile] = kingdom_piles
        self._other_piles: List[Pile] = other_piles

    @property
    def piles(self):
        return self._kingdom_piles + self._other_piles

    def get_num_of_empty(self):
        return len(self.empty_piles)

    @property
    def empty_piles(self):
        return [pile for pile in self.piles if pile.is_empty()]
