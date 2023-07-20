from poker_base import *
from actions import *


class Player:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
        self.hand = []  # [card, card]

    def respond(self, game):
        if game.max_bet == 0:
            return Action(self.id, Actions.Bet, 1)
        if 2 * game.max_bet < game.sys.manager.possession[self.id]:
            return Action(self.id, Actions.Raise, 2 * game.max_bet)
        return Action(self.id, Actions.Allin, game.sys.manager.possession[self.id])
