import random
from poker_base import *
from position import Position
from actions import *
from poker_player import Player


class Dealer:
    def __init__(self, game):
        self.game = game
        self.piles = []
        self.board = []

    def shuffle(self):
        self.piles.clear()
        for suit in Suit:
            for pt in Point:
                self.piles.append(Card(suit, pt))
        random.shuffle(self.piles)

    def choose_5(self):
        board = []
        temp = self.piles.copy()
        random.shuffle(temp)
        for i in range(5):
            board.append(temp.pop())
        return board

    def draw(self):
        return self.piles.pop()

    def draw_spec(self, card: Card):
        assert card in self.piles
        self.piles.remove(card)
        return card

    def deliver_to_player(self, i):
        self.game.sys.players[i].hand = [self.draw(), self.draw()]

    def deliver_specific_to_player(self, i, hand: [Card]):
        assert len(hand) == 2
        self.game.sys.players[i].hand = [self.draw_spec(hand[0]), self.draw_spec(hand[1])]

    def deliver_to_all(self):
        for i in range(len(self.game.sys.players)):
            self.deliver_to_player(i)

    def flop(self):
        assert len(self.board) == 0
        self.board.append(self.draw())
        self.board.append(self.draw())
        self.board.append(self.draw())

    def turn(self):
        assert len(self.board) == 3
        self.board.append(self.draw())

    def river(self):
        assert len(self.board) == 4
        self.board.append(self.draw())

    def show_hands(self):
        for i in range(self.game.nplayer):
            print(i, "th player:", self.game.players[i].name)
            hand = self.game.players[i].hand
            print(hand[0], '|', hand[1])

    def show_board(self):
        print("board:")
        msg = ""
        for card in self.board:
            msg += card.__str__() + ' | '
        print(msg)


class Game:
    def __init__(self, sys):
        self.sys = sys
        self.dealer = Dealer(self)
        self.judger = Judge()
        self.rounds = ["preflop", "flop", "turn", "river"]
        self.round_id = 0
        self.max_bet = 0
        self.game_finished = False

    def request(self, player_id):
        return self.sys.players[player_id].respond(self)

    def is_round_finished(self):
        # to do someone allin
        if list(self.sys.manager.fold_map.values()).count(False) == 1:
            self.game_finished = True
            return True
        for i, p in enumerate(self.sys.players):
            if not self.sys.manager.fold_map[p.id]:
                if self.sys.manager.round_bet_map != self.max_bet:
                    return False
        return True

    def round(self):
        print("round {{{}}}".format(self.rounds[self.round_id]))
        self.sys.manager.round_bet_map = {player.id: -1 for player in self.sys.players}
        nplayer = self.sys.nplayer
        begin = (self.sys.button_id + 1) % nplayer
        if self.round_id == 0:
            begin = (begin + 2) % nplayer
        player_id = begin
        self.max_bet = 0
        while not self.is_round_finished():
            if not self.sys.manager.fold_map[player_id]:
                response = self.request(player_id)
                print("player {} {} {}".format(response.player_id, response.act, response.amount))
                assert response.player_id == player_id
                self.sys.manager.handle_bet(response)
            player_id = (player_id + 1) % nplayer
        if self.game_finished:
            print("game finished! winner is")
        self.round_id += 1

    def run(self):
        self.dealer.shuffle()
        self.dealer.deliver_to_all()
        self.sys.manager.every_game_init()
        # TO do circle
        self.round()
        self.dealer.flop()
        self.round()
        self.dealer.turn()
        self.round()
        self.dealer.river()
        self.round()
        self.dealer.show_hands()
        self.dealer.show_board()
        print(len(self.dealer.piles), " cards left")

        judge = Judge()
        judge.judge(self.dealer.board, self.sys.players)
        self.button_id = (self.button_id + 1) % self.nplayer

    def hand_run(self, hand0, hand1):
        self.dealer.shuffle()
        self.dealer.deliver_specific_to_player(0, hand0)
        self.dealer.deliver_specific_to_player(1, hand1)
        judge = Judge()

        cnt0, cnt1, deuce = 0, 0, 0
        n = 1000
        for i in range(n):
            board = self.dealer.choose_5()
            # msg = ""
            # for card in board:
            #     msg += card.__str__() + ' | '
            # print(msg)
            winner = judge.judge(board, self.sys.players)
            if winner == 0:
                cnt0 += 1
            elif winner == 1:
                cnt1 += 1
            else:
                deuce += 1
        print("{} | {} winning rate: {}, {} | {} winning rate: {}, deuce: {}".format(hand0[0], hand0[1], 1.0*cnt0/n,
                                                                         hand1[0], hand1[1], 1.0*cnt1/n, 1.0*deuce/n))


class System:
    def __init__(self):
        self.game = Game(self)
        self.manager = PotManager(self)
        self.nplayer = 0
        self.players = []
        self.button_id = 0

    def add_player(self, id_, name):
        self.players.append(Player(id_, name))
        self.nplayer += 1

    def add_players(self, n: int):
        assert 2 <= n <= 10
        for i in range(n):
            self.add_player(self.nplayer, "player_" + str(self.nplayer))

    def solo(self):
        self.add_players(2)
        self.manager.set_money(1000)
        self.game.run()




if __name__ == "__main__":
    # random.seed(1)
    system = System()
    system.solo()

    hand0 = [Card(Suit.Spade, Point.Nine), Card(Suit.Spade, Point.Ten)]
    hand1 = [Card(Suit.Diamond, Point.King), Card(Suit.Diamond, Point.Queen)]
    # for suit in Suit:
    #     for pt in Point:
    #         if Card(suit, pt) == hand0[0] or Card(suit, pt) == hand0[1]:
    #             continue
    #         for suit1 in Suit:
    #             for pt1 in Point:
    #                 if Card(suit1, pt1) == hand0[0] or Card(suit1, pt1) == hand0[1] or Card(suit, pt) == Card(suit1, pt1):
    #                     continue
    #                 hand1 = [Card(suit1, pt1), Card(suit, pt)]
    #                 system.hand_run(hand0, hand1)
    # system.game.hand_run(hand0, hand1)

