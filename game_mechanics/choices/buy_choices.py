from game_mechanics.choices.common_choices import CommonChoices
from game_mechanics.choices.human.generic_choices import display_choices_from_human_hand, \
    get_human_player_multy_choice, get_human_player_choice
from game_mechanics.phases.phases import Phase
from game_mechanics.player.bot_player import BotPlayer
from game_mechanics.player.human_player import HumanPlayer
from game_mechanics.player.player import Player
from game_mechanics.player.turn_state import TurnState
from game_mechanics.supply import Supply
from game_supplies.card_types.card import Treasure


def autoplay_treasures(player: Player, turn_state: TurnState):
    """
    Play all treasures that are defined for automatic play
    """
    if isinstance(player, BotPlayer):
        answer = "Y"
    else:
        answer = input("Autoplay treasures? y/n: ").upper()
    if not answer or answer == "Y":
        playable_cards = player.get_playable_cards(Phase.BuyPhase)
        for card, cnt in playable_cards.items():
            card: Treasure
            if card.automatic_play:
                for _ in range(cnt):
                    player.play_card_from_hand(card, turn_state)


def play_treasures_by_choice(player: Player, turn_state: TurnState) -> bool:
    """
    Allow player to choose treasure cards from his hand.
    """
    playable_cards = player.get_playable_cards(Phase.BuyPhase)
    playable_cards_keys = list(playable_cards.keys())
    valid_choices = [CommonChoices.NONE_CHOICE.name]
    valid_choices.extend([card.name for card in playable_cards_keys])
    if isinstance(player, BotPlayer):
        choices = list(range(1, len(valid_choices)))
    else:
        player: HumanPlayer
        message = display_choices_from_human_hand(player, Phase.BuyPhase)
        choices = get_human_player_multy_choice(valid_choices, message)

    if choices[0] is CommonChoices.NONE_CHOICE:
        return False
    chosen_cards = [playable_cards_keys[int(i) - 1] for i in choices]
    for card in chosen_cards:
        for _ in range(playable_cards[card]):
            player.play_card_from_hand(card, turn_state)
    return True


def buy_card_by_choice(player: Player, turn_state: TurnState, supply: Supply) -> bool:
    """
    Allow player to buy a card.
    Update state accordingly.
    :param player: the player
    :param turn_state: the state
    :param supply: the supply
    :return: did the player buy a card
    """
    piles_to_buy_from = supply.get_piles_allowed_for_buy(max_cost=turn_state.coins)
    valid_choices = [CommonChoices.NONE_CHOICE.name]
    valid_choices.extend([pile.name for pile in piles_to_buy_from])
    if isinstance(player, BotPlayer):
        best_pile = max(piles_to_buy_from)
        choice = valid_choices.index(best_pile.name)
    else:
        player: HumanPlayer
        print(f"* Number of buys left {turn_state.buys}")
        print(f"* Number of coins left {turn_state.coins}")
        choice = get_human_player_choice(valid_choices)

    if choice is CommonChoices.NONE_CHOICE:
        return False

    chosen_pile = piles_to_buy_from[int(choice) - 1]
    card = chosen_pile.draw()  # remove top card from the pile
    turn_state.buys -= 1
    turn_state.coins -= card.cost
    player.discard_pile.put(card)
    return True
