from typing import List

from game_mechanics.pile import Pile


class Supply:
    """
    Represents all the piles on the table.
    """
    def __init__(self, piles: List[Pile]):
        self.piles: List[Pile] = piles

    def get_num_of_empty(self):
        return len(self.empty_piles)

    @property
    def empty_piles(self):
        return [pile for pile in self.piles if pile.is_empty()]
