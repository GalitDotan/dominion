# TODO: all those are effects
def play_card_from_hand(self, card: Card, turn_state: PlayerTurnState):
    """
    Play a card from _play_order hand and update state accordingly.

    :param card: the card.
    :param turn_state: current game_stages state.
    """
    if card not in self.state.hand:
        raise ValueError(f"{card} is not in {self.state.hand}")

    self.state.hand.remove(card)
    self.state.play_area.play(card)

    if isinstance(card, Treasure):
        turn_state.coins += card.coins
    if isinstance(card, Action):
        for cmd in card.actions:
            pass
    if isinstance(card, Attack):
        for cmd in card.attacks:
            pass
    if isinstance(card, Night):
        pass


def draw_card(self):
    """
    Get a card from the Draw pile and put it in the Hand.
    """
    if self.state.draw_pile.is_empty():
        self.shuffle_discard_to_draw_pile()
    return self.state.draw_pile.draw()


def draw_cards(self, amount: int):
    """
    Draw a card `amount` times.
    If the Draw and DiscardCard piles got emptied - it could return less than the desired `amount` of cards.
    """
    cards = [self.draw_card() for _ in range(amount)]
    return [card for card in cards if card]  # card could be None


def draw_hand(self, num: int = 5):
    return self.draw_cards(num)


def discard_hand(self):
    """
    Move all cards from hand to DiscardCard pile.
    """
    cards = self.state.hand.remove_all()
    self.state.discard_pile.put_all(cards)


def discard_play(self):
    """
    Move all non-Duration cards from the Play Area to the DiscardCard pile.
    """
    cards = self.state.play_area.do_cleanup()
    self.state.discard_pile.put_all(cards)


def shuffle_discard_to_draw_pile(self):
    """
    Shuffle all cards in the DiscardCard pile and put them on the bottom of the Draw pile.
    """
    cards = self.state.discard_pile.draw_all()
    shuffle(cards)
    self.state.discard_pile.put_all(cards)
