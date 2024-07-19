from enum import Enum


class ActionType(Enum):
    Check = 0
    Bet = 1
    Call = 2
    Raise = 3
    Fold = 4
    Allin = 5


class Action:
    def __init__(self, player_pos: int, act: ActionType, amount: int):
        self.player_pos = player_pos
        self.act = act
        self.amount = amount


class PotManager:
    def __init__(self, sys):
        self.sys = sys
        self.possession = dict()  # {pos : money}
        self.blind = 1
        self.pot = 0
        self.bb_act = False
        self.round_bet_map = dict()
        self.fold_map = dict()
        self.allin_map = dict()

    def set_same_money(self, init_money):
        self.possession = {player.pos: init_money for player in self.sys.players}

    def set_money(self, pos, init_money):
        self.possession[pos] = init_money

    def every_game_init(self):
        self.bb_act = False
        self.round_bet_map = {player.pos: -1 for player in self.sys.players}
        self.fold_map = {player.pos: False for player in self.sys.players}
        self.allin_map = {player.pos: False for player in self.sys.players}

    def try_bet(self, pos, amount):
        actual_cost = min(self.possession[pos], amount)
        self.possession[pos] -= actual_cost
        if self.possession[pos] == 0:
            self.allin_map[pos] = True
        self.round_bet_map[pos] = max(self.round_bet_map[pos], 0) + actual_cost
        self.pot += actual_cost
        return actual_cost

    def pre_blind_bet(self):
        sb_pos = (self.sys.button_pos + 1) % self.sys.nplayer
        bb_pos = (self.sys.button_pos + 2) % self.sys.nplayer
        sb = self.try_bet(sb_pos, self.blind)
        bb = self.try_bet(bb_pos, self.blind * 2)
        self.sys.game.max_bet = self.blind * 2
        print("{} th player {}\t {:13} {}, remain: {:4}".format(sb_pos, self.sys.players[sb_pos].name,
              "Blind", sb, self.possession[sb_pos]))
        print("{} th player {}\t {:13} {}, remain: {:4}".format(bb_pos, self.sys.players[bb_pos].name,
              "Blind", bb, self.possession[bb_pos]))

    def handle_action(self, response):
        if response.act == ActionType.Check:
            if self.round_bet_map[response.player_pos] == self.sys.game.max_bet:
                return
            assert self.sys.game.max_bet == 0
            self.round_bet_map[response.player_pos] = 0
        elif response.act == ActionType.Bet:
            assert self.sys.game.max_bet == 0
            assert self.possession[response.player_pos] >= response.amount
            self.try_bet(response.player_pos, response.amount)
            self.sys.game.max_bet = response.amount
        elif response.act == ActionType.Call:
            assert self.sys.game.max_bet != 0
            assert self.sys.game.max_bet == response.amount
            add = response.amount - max(0, self.round_bet_map[response.player_pos])
            assert self.possession[response.player_pos] >= add
            self.try_bet(response.player_pos, add)
        elif response.act == ActionType.Raise:
            assert self.sys.game.max_bet != 0
            assert response.amount >= 2 * self.sys.game.max_bet
            add = response.amount - max(0, self.round_bet_map[response.player_pos])
            assert self.possession[response.player_pos] >= add
            self.try_bet(response.player_pos, add)
            self.sys.game.max_bet = response.amount
        elif response.act == ActionType.Fold:
            self.fold_map[response.player_pos] = True
        elif response.act == ActionType.Allin:
            add = response.amount - max(0, self.round_bet_map[response.player_pos])
            assert add == self.possession[response.player_pos]
            self.try_bet(response.player_pos, add)
            self.sys.game.max_bet = max(response.amount, self.sys.game.max_bet)

    def game_settle(self, winner_poses):
        if len(winner_poses) == 1:
            winner_pos = winner_poses[0]
            self.possession[winner_pos] += self.pot
        else:
            for winner_pos in winner_poses:
                self.possession[winner_pos] += self.pot // len(winner_poses)
        self.pot = 0
        need_print = True

        if need_print:
            print(self.possession)
