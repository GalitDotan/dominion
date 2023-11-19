from game_mechanics.interactions.general_choices import CommonChoices, get_player_multy_choice, \
    display_choices_from_hand
from game_mechanics.phases.phases import Phase
from game_mechanics.player.player import Player


def play_treasures_by_choice(player: Player) -> bool:
    playable_cards, valid_choices, message = display_choices_from_hand(player, Phase.BuyPhase)
    choices = get_player_multy_choice(valid_choices, message)

    if choices[0] is not CommonChoices.NONE_CHOICE:
        chosen_cards = [playable_cards[int(i)] for i in choices]
        for card in chosen_cards:
            player.hand.remove(card)
            player.play_card(card)
        return True
    return False
