from game_mechanics.interactions.general_choices import CommonChoices, get_player_multy_choice, \
    display_choices_from_hand, get_player_choice
from game_mechanics.phases.phases import Phase
from game_mechanics.player.player import Player
from game_mechanics.player.turn_state import TurnState
from game_mechanics.supply import Supply


def _autoplay_treasures(player: Player, turn_state: TurnState):
    """
    Play all treasures that are defined for automatic play
    """
    playable_cards = player.get_playable_cards(Phase.BuyPhase)
    for card, cnt in playable_cards.items():
        if card.automatic_play:
            for _ in range(cnt):
                player.play_card_from_hand(card, turn_state)


def play_treasures_by_choice(player: Player, turn_state: TurnState) -> bool:
    answer = input("Autoplay treasures? Y/n: ").upper()
    if not answer or answer == "Y":
        _autoplay_treasures(player, turn_state)
        return True  # maybe player wants to play non-automatic treasures
    playable_cards, message = display_choices_from_hand(player, Phase.BuyPhase)
    playable_cards_keys = list(playable_cards.keys())
    valid_choices = [CommonChoices.NONE_CHOICE.name]
    valid_choices.extend([card.name for card in playable_cards_keys])
    choices = get_player_multy_choice(valid_choices, message)

    if choices[0] is CommonChoices.NONE_CHOICE:
        return False
    chosen_cards = [playable_cards_keys[int(i) - 1] for i in choices]
    for card in chosen_cards:
        for _ in range(playable_cards[card]):
            player.play_card_from_hand(card, turn_state)
    return True


def buy_card_by_choice(player: Player, turn_state: TurnState, supply: Supply) -> bool:
    piles_to_buy_from = supply.get_piles_allowed_for_buy(max_cost=turn_state.coins)
    pile_names = [pile.name for pile in piles_to_buy_from]
    print(f"* Number of buys left {turn_state.buys}")
    print(f"* Number of coins left {turn_state.coins}")
    choice = get_player_choice(pile_names, "Choose a card to buy")
    if choice is CommonChoices.NONE_CHOICE:
        return False
    chosen_pile = piles_to_buy_from[int(choice)]
    card = chosen_pile.draw()  # remove top card from the pile
    turn_state.buys -= 1
    turn_state.coins -= card.cost
    player.discard_pile.put(card)
    return True
