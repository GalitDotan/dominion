from game_mechanics.effects.draw_num_cards import DrawNum
from game_mechanics.effects.trash_from_hand import TrashFromHand

CELLAR = (IncStateCounters(actions=1), DiscardThenDraw())
CHAPEL = (TrashFromHand(max_trash=4))
MOAT = (DrawNum(num=2))
