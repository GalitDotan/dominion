from config import HeadlineFormats
from game_mechanics.game_options.old.player_decision import PlayerDecision, CommonChoices


class PlayerPlayDecision(PlayerDecision):
    """
    PlayerDecision of what to play from hand
    """
    def __repr__(self):
        """
        Print all the options.
        """
        print()
        print(f"Your hand: {self.player.hand.cards_dict}")
        print(f"Playable cards: {self.options}")
        message = f"Choose the card to play, or type '{CommonChoices.NONE_CHOICE}' for none"
        print(HeadlineFormats.H3.format(message))

    def play_cards_by_choice(self) -> bool:
        """
        Choose an action to play

        :param curr_player: current curr_player
        :param playable_cards: all options to play
        :return: Was a change made?
        """
        playable_cards_keys = list(playable_cards.keys())
        valid_choices = [CommonChoices.NONE_CHOICE.name] + [str(card) for card in playable_cards_keys]
        if isinstance(player, BotPlayer):
            chosen_card = get_bot_player_choice(player, playable_cards)
        else:
            player: HumanPlayer
            display_choices_from_human_hand(player, playable_cards)
            answer = get_human_player_choice(valid_choices)

            if answer is CommonChoices.NONE_CHOICE:
                return False
            choice = int(answer)
            chosen_card = playable_cards_keys[choice - 1]
        player.play_card_from_hand(chosen_card, turn_state)
        return True
