from game_mechanics.card_structures.card_structure import CardStructure
from game_mechanics.game_supplies.base_card import BaseCard
from game_mechanics.game_supplies.card_type import CardType


class PlayArea(CardStructure):
    """
    The Dominion table.
    It stores all the cards that are currently "in-play"
    """

    def play(self, card: BaseCard):
        """
        Put a card here.
        Assuming the cars is no longer in other card structures.

        Params:
            card: a card to put.
        """
        self.append(card)

    def do_cleanup(self) -> list[BaseCard]:
        """
        Remove all cards but duration cards.

        Returns:
            All removed cards.
        """
        all_cards = self.remove_all()
        duration_cards = [card for card in all_cards if CardType.DURATION in card.types]
        non_duration_cards = [card for card in all_cards if CardType.DURATION not in card.types]
        self.extend(duration_cards)  # keep the duration cards
        return non_duration_cards
