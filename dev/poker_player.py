from poker_base import *
from actions import *


class Style(Enum):
    Reserved = 0
    Aggressive = 1
    Balanced = 2


class Player:
    def __init__(self, id: int, name: str, pos: int):
        self.id = id
        self.name = name
        self.pos = pos
        self.hand = []  # [card, card]
        self.strategy = Strategy.call_station

    def respond(self, game):
        return self.strategy(self.pos, game)

    def manual_respond(self, game):
        print("Type {}'s Action:".format(self.name))
        action = input().split()
        if action[0] == "Check":
            return Action(self.pos, ActionType.Check, 0)
        elif action[0] == "Bet":
            return Action(self.pos, ActionType.Bet, int(action[1]))
        elif action[0] == "Call":
            return Action(self.pos, ActionType.Call, int(action[1]))
        elif action[0] == "Raise":
            return Action(self.pos, ActionType.Raise, int(action[1]))
        elif action[0] == "Fold":
            return Action(self.pos, ActionType.Fold, 0)
        return Action(self.pos, ActionType.Allin, int(action[1]))

    def set_strategy(self, style: Style):
        if style == Style.Reserved:
            self.strategy = Strategy.call_station
        elif style == Style.Aggressive:
            self.strategy = Strategy.aggressive


class Strategy:
    @staticmethod
    def call_station(pos, game):
        if game.max_bet == 0:
            return Action(pos, ActionType.Check, 0)
        call_needed = game.max_bet - max(0, game.sys.manager.round_bet_map[pos])
        if game.sys.manager.possession[pos] > call_needed:
            return Action(pos, ActionType.Call, game.max_bet)
        return Action(pos, ActionType.Allin, game.sys.manager.possession[pos] + max(0, game.sys.manager.round_bet_map[pos]))

    @staticmethod
    def aggressive(pos, game):
        if game.max_bet == 0:
            return Action(pos, ActionType.Bet, 1)
        wanted_bet = 2 * game.max_bet
        if game.sys.manager.possession[pos] > wanted_bet - max(0, game.sys.manager.round_bet_map[pos]):
            return Action(pos, ActionType.Raise, wanted_bet)
        wanted_bet = game.sys.manager.possession[pos] + max(0, game.sys.manager.round_bet_map[pos])
        return Action(pos, ActionType.Allin, wanted_bet)

    @staticmethod
    def xx(pos, game):
        return Strategy.call_station(pos, game)
