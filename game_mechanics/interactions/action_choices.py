from game_mechanics.interactions.general_choices import CommonChoices, get_player_choice, choose_cards_from_hand
from game_mechanics.phases.phases import Phase
from game_mechanics.player.player import Player


def do_action_choice(player: Player):
    all_cards = player.cards_alphabetically
    playable_cards = player.get_playable_cards(Phase.ActionPhase)
    print(f"Your hard: {all_cards}")
    print(f"Playable cards: {playable_cards}")
    message = f"Choose the card to play, or type '{CommonChoices.NONE_CHOICE}' for none"
    valid_choices = [str(i) for i in range(1, len(playable_cards) + 1)] + [CommonChoices.NONE_CHOICE.name]
    answer = get_player_choice(valid_choices, message)

    if answer is not CommonChoices.NONE_CHOICE:
        choice = int(answer)
        chosen_card = playable_cards[choice]
        player.play_card(chosen_card)
        player.hand.pop(choice)
        player.play_card(chosen_card)


def choose_cards_to_discard(player: Player):
    removed_cards = choose_cards_from_hand(player)
    player.discard_pile.put_all(removed_cards)
