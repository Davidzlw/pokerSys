from enum import Enum

class Actions(Enum):

    Raise = 0


class PotManager:
    def __init__(self, game, init_money):
        self.game = game
        self.possession = {id: init_money for id in self.game.players}
        self.blind = 1
        self.pot = 0
        self.player_alive = set()

    def every_game_init(self):
        self.player_alive.clear()
        self.player_alive = {player.id for player in self.game.players}
        sb_id = (self.game.button + 1) % self.game.nplayer
        bb_id = (self.game.button + 2) % self.game.nplayer
        self.possession[sb_id] -= self.blind
        self.possession[bb_id] -= self.blind * 2

    def request(self):
        pass

    def round(self):
        print("round {{{}}}".format(self.game.rounds[self.game.round_id]))
        begin = (self.game.button + 1) % self.game.nplayer
        if self.game.round_id == 0:
            begin = (begin + 2) % self.game.nplayer
        for i in range(self.game.nplayer):
            if i in self.player_alive:
                response = self.request()

        self.game.round_id += 1
