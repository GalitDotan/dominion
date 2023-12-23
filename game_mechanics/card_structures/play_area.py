from game_mechanics.card_structures.card_structure import CardStructure
from game_mechanics.game_supplies.base_card import Card
from game_mechanics.game_supplies.card_type import CardType


class PlayArea(CardStructure):
    """
    The Dominion table.
    It stores all the cards that are currently "in-play"
    """

    def play(self, card: Card):
        """
        Put a card here.
        Assuming the cars is no longer in other card structures.

        Args:
            card: a card to put.
        """
        self.append(card)

    def do_cleanup(self) -> list[Card]:
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
