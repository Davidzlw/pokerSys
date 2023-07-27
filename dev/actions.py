from enum import Enum

class Actions(Enum):
    Check = 0
    Bet = 1
    Call = 2
    Raise = 3
    Fold = 4
    Allin = 5


class Action:
    def __init__(self, player_pos: int, act: Actions, amount: int):
        self.player_pos = player_pos
        self.act = act
        self.amount = amount


class PotManager:
    def __init__(self, sys):
        self.sys = sys
        self.possession = dict()  # {pos : money}
        self.blind = 1
        self.pot = 0
        self.round_bet_map = dict()
        self.fold_map = dict()
        self.allin_map = dict()

    def set_money(self, init_money):
        self.possession = {player.pos: init_money for player in self.sys.players}

    def every_game_init(self):
        self.round_bet_map = {player.pos: -1 for player in self.sys.players}
        sb_pos = (self.sys.button_pos + 1) % self.sys.nplayer
        bb_pos = (self.sys.button_pos + 2) % self.sys.nplayer
        self.possession[sb_pos] -= self.blind
        self.possession[bb_pos] -= self.blind * 2
        self.pot += 3 * self.blind
        self.round_bet_map[sb_pos] = self.blind
        self.round_bet_map[bb_pos] = self.blind * 2
        self.sys.game.max_bet = self.blind * 2

        self.fold_map = {player.pos: False for player in self.sys.players}
        self.allin_map = {player.pos: False for player in self.sys.players}

    def handle_bet(self, response):
        if response.act == Actions.Check:
            assert self.sys.game.max_bet == 0
            self.round_bet_map[response.player_pos] = 0
        elif response.act == Actions.Bet:
            assert self.sys.game.max_bet == 0
            assert self.possession[response.player_pos] >= response.amount
            self.possession[response.player_pos] -= response.amount
            self.round_bet_map[response.player_pos] = response.amount
            self.sys.game.max_bet = response.amount
            self.pot += response.amount
        elif response.act == Actions.Call:
            assert self.sys.game.max_bet != 0
            assert self.sys.game.max_bet == response.amount
            add = response.amount - max(0, self.round_bet_map[response.player_pos])
            assert self.possession[response.player_pos] >= add
            self.possession[response.player_pos] -= add
            self.round_bet_map[response.player_pos] = self.sys.game.max_bet
            self.pot += add
        elif response.act == Actions.Raise:
            assert self.sys.game.max_bet != 0
            assert response.amount >= 2 * self.sys.game.max_bet
            add = response.amount - max(0, self.round_bet_map[response.player_pos])
            assert self.possession[response.player_pos] >= add
            self.possession[response.player_pos] -= add
            self.round_bet_map[response.player_pos] = response.amount
            self.sys.game.max_bet = response.amount
            self.pot += add
        elif response.act == Actions.Fold:
            self.fold_map[response.player_pos] = True
        elif response.act == Actions.Allin:
            add = response.amount - max(0, self.round_bet_map[response.player_pos])
            assert add == self.possession[response.player_pos]
            self.allin_map[response.player_pos] = True
            self.possession[response.player_pos] = 0
            self.round_bet_map[response.player_pos] = response.amount
            self.sys.game.max_bet = max(response.amount, self.sys.game.max_bet)
            self.pot += add

    def game_settle(self, winners):
        if len(winners) == 1:
            winner = winners[0]
            self.possession[winner.player.pos] += self.pot
        else:
            for winner in winners:
                self.possession[winner.player.pos] += self.pot // len(winners)
        self.pot = 0
        need_print = True
        if need_print:
            print(self.possession)
