from typing import Optional

from game_mechanics.card_structures.supply_pile import SupplyPile
from game_mechanics.card_structures.trash import Trash
from game_mechanics.game_options.old.player_decision import CommonChoices
from game_mechanics.game_options.old.human.generic_choices import get_human_player_choice
from game_mechanics.game_stages.game_stage import GameStage
from game_mechanics.player.bot_player import BotPlayer
from game_mechanics.player.human_player import HumanPlayer
from game_mechanics.player.player import Player
from game_mechanics.states.player_turn_state import PlayerTurnState
from game_mechanics.supply import Supply, buy


class BuyingStage(GameStage):
    """
    A stage in which buying cards from the supply is allowed.
    The current state of the coins is updated accordingly.
    """

    def __init__(self, player: Player, turn_state: PlayerTurnState, supply: Supply, opponents: list[Player], trash: Trash,
                 name: Optional[str] = None):
        super().__init__(player, opponents, supply, trash, name)
        self.continue_buying = True
        self.turn_state = turn_state

    def __repr__(self):
        pass

    def play(self):
        buyable_cards = self.get_buyable_cards()
        if not buyable_cards:
            self.print("There aren't cards you can buy.")
            return
        self.before_run_iterations()
        while self.continue_buying:
            self.run_stage_iteration()

    def before_run_iterations(self):
        """
        Autoplay treasures, if any exists in hand.
        """
        self.print("Now, let's buy some cards")
        self.print(str(self.supply))

    def run_stage_iteration(self):
        """
        Play one action card by choice.
        """
        piles_to_buy_from = self.supply.get_piles_allowed_for_buy(max_cost=self.turn_state.coins)
        if self.turn_state.buys == 0 or len(piles_to_buy_from) == 0:
            return False
        self.continue_buying = self.buy_card_by_choice()

    def get_buyable_cards(self) -> list[SupplyPile]:
        """
        Of all the piles in the supply - get all piles that there is enough money to buy from.

        :return: the piles.
        """
        return self.supply.get_piles_allowed_for_buy(max_cost=self.turn_state.coins)

    def buy_card_by_choice(self) -> bool:
        """
        Allow curr_player to buy a card.
        If a card is bought:
            1. It is removed from the supply
            2. It is added to the curr_player's discard pile
        :return: did the curr_player buy a card
        """
        piles_to_buy_from = self.supply.get_piles_allowed_for_buy(max_cost=self.turn_state.coins)
        valid_choices = [CommonChoices.NONE_CHOICE.name]
        valid_choices.extend([pile.name for pile in piles_to_buy_from])
        if isinstance(self.player, BotPlayer):
            best_pile = max(piles_to_buy_from)
            choice = valid_choices.index(best_pile.name)
        else:
            player: HumanPlayer
            print(f"* Number of buys left {self.turn_state.buys}")
            print(f"* Number of coins left {self.turn_state.coins}")
            choice = get_human_player_choice(valid_choices)

        if choice is CommonChoices.NONE_CHOICE:
            return False

        chosen_pile = piles_to_buy_from[int(choice) - 1]
        self._buy_from_pile(chosen_pile)

        return True

    def _buy_from_pile(self, pile: SupplyPile):
        # this 4 lines should be relocated to someplace more natural (maybe inside 'turn state')
        card = buy(pile)
        self.turn_state.buys -= 1
        self.turn_state.coins -= card.cost
        self.player.discard_pile.put(card)
