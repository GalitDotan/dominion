from game_mechanics.card_structures._card_structure import CardStructure
from game_mechanics.game_supplies.card_types.card import Card
from game_mechanics.game_supplies.card_types.duration_card import Duration


class PlayArea(CardStructure):
    """
    The Dominion table.
    It stores all the cards that are currently "in-play"
    """

    def play(self, card: Card):
        """
        Put a card here.
        Assuming the cars is no longer in other card structures.

        Params:
            card: a card to put.
        """
        self.append(card)

    def resolve(self, card: Duration):
        """
        Remove a Duration card from here.

        Params:
            card: a card to put.
        """
        self.remove(card)
        # TODO: add functionality on resolve

    def do_cleanup(self) -> list[Card]:
        """
        Remove all cards but duration cards.

        Returns:
            All removed cards.
        """
        all_cards = self.remove_all()
        duration_cards = [card for card in all_cards if type(card) is Duration]
        non_duration_cards = [card for card in all_cards if type(card) is not Duration]
        self.extend(duration_cards)  # keep the duration cards
        return non_duration_cards
