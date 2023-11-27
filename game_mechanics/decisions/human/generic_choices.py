from game_mechanics.decisions.player_decision import CommonChoices
from game_mechanics.player.human_player import HumanPlayer
from game_supplies.card_types.card import Card


def get_human_player_choice(valid_choices: list[str]):
    for i, choice in enumerate(valid_choices):
        print(f'{i}. {choice}')
    answer = input("Your choice: ")

    help_choice = CommonChoices.HELP_CHOICE.name
    if answer.endswith(help_choice):
        help_request = answer.replace(help_choice, '')
        try:
            eval(f'{help_request}.help()')
        except Exception:
            print(f"I cannot help you with {help_request}")
        return get_human_player_choice(valid_choices)
    if answer in valid_choices:
        return valid_choices.index(answer)

    i = int(answer)  # TODO: error handling for non int inputs
    return i

    # print(f'{answer} is not a valid choice. Please choose one of: {valid_choices}')
    # return get_player_choice(valid_choices, headline)


def get_human_player_multy_choice(valid_choices: list[str], message: str) -> list[str]:
    print(message)
    for i, card_name in enumerate(valid_choices):
        print(f'{i}. {card_name}')
    answers = input("Your decisions: ")
    if answers is CommonChoices.NONE_CHOICE:
        return [CommonChoices.NONE_CHOICE.name]
    return answers.split()


def choose_cards_from_human_hand(player: HumanPlayer) -> list[Card]:
    cards = player.hand.cards
    hand_cards = [card.name for card in cards]
    answer = get_human_player_multy_choice(hand_cards, "Choose which cards to ")
    removed_cards = []
    for i in answer:
        card = cards[int(i)]
        player.hand.remove(card)
        removed_cards.append(card)
    return removed_cards
