from poker_base import *
from actions import *


class Style(Enum):
    Reserved = 0
    Aggressive = 1
    Balanced = 2


class Player:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
        self.hand = []  # [card, card]
        self.strategy = Strategy.call_station

    def respond(self, game):
        return self.strategy(self.id, game)

    def set_strategy(self, style: Style):
        if style == Style.Reserved:
            self.strategy = Strategy.call_station
        elif style == Style.Aggressive:
            self.strategy = Strategy.aggressive


class Strategy:
    @staticmethod
    def call_station(id, game):
        if game.max_bet == 0:
            return Action(id, Actions.Check, 0)
        call_needed = game.max_bet - max(0, game.sys.manager.round_bet_map[id])
        if game.sys.manager.possession[id] > call_needed:
            return Action(id, Actions.Call, game.max_bet)
        return Action(id, Actions.Allin, game.sys.manager.possession[id] + max(0, game.sys.manager.round_bet_map[id]))

    @staticmethod
    def aggressive(id, game):
        if game.max_bet == 0:
            return Action(id, Actions.Bet, 1)
        wanted_bet = 2 * game.max_bet
        if game.sys.manager.possession[id] > wanted_bet - max(0, game.sys.manager.round_bet_map[id]):
            return Action(id, Actions.Raise, wanted_bet)
        wanted_bet = game.sys.manager.possession[id] + max(0, game.sys.manager.round_bet_map[id])
        return Action(id, Actions.Allin, wanted_bet)

    @staticmethod
    def xx(id, game):
        return Strategy.call_station(id, game)
