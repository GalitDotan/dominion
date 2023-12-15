from collections import Counter
from typing import Optional

from game_mechanics.card_structures.pile import Pile
from game_mechanics.game_supplies.card_types.card_type import CardType


class SupplyPile(Pile):
    def __init__(self, cards: list[CardType] = (), name: Optional[str] = None, is_visible: bool = True):
        super().__init__(cards, name, is_visible)
        if len(self) == 0:
            raise ValueError("Supply pile cannot be initiated empty")
        self.initial_cost = self.cards[0].cost

    def __repr__(self):
        basic_repr = f"{self.name}[{len(self)}]"
        if not self._is_visible:
            return basic_repr
        counter = dict(Counter(self._cards))
        card_names_counts = {card.name: (f'amount: {cnt}', f'cost: {card.cost}') for card, cnt in counter.items()}
        if len(counter) == 0:
            return basic_repr
        elif len(counter) == 1:
            return f"{basic_repr}: cost: {self.cards[0].cost}"
        return f"{basic_repr}: {card_names_counts}"

    def __lt__(self, other):
        return self.initial_cost < other.initial_cost or (
                self.initial_cost == other.initial_cost and self.name < other.name)

    @property
    def cost(self):
        return self.cards[-1].cost
