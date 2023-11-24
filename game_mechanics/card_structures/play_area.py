from game_mechanics.card_structures._card_structure import CardStructure
from game_supplies.card_types import Duration
from game_supplies.card_types.card import Card


class PlayArea(CardStructure):
    def play(self, card: Card):
        self.append(card)

    def resolve(self, card: Duration):
        self.remove(card)

    def do_cleanup(self) -> list[Card]:
        """
        Remove all cards but duration cards.

        :return: all removed cards.
        """
        all_cards = self.remove_all()
        duration_cards = [card for card in all_cards if type(card) is Duration]
        non_duration_cards = [card for card in all_cards if type(card) is not Duration]
        self.extend(duration_cards)
        return non_duration_cards
