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
        self.game.players[i].hand = [self.draw(), self.draw()]

    def deliver_specific_to_player(self, i, hand: [Card]):
        assert len(hand) == 2
        self.game.players[i].hand = [self.draw_spec(hand[0]), self.draw_spec(hand[1])]

    def deliver_to_all(self):
        for i in range(self.game.nplayer):
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


class System:
    def __init__(self, n):
        assert 2 <= n <= 10
        self.dealer = Dealer(self)
        self.manager = PotManager(self, 1000)
        self.judger = Judge()
        self.rounds = ["preflop", "flop", "turn", "river"]
        self.round_id = 0
        self.nplayer = n
        self.players = []
        for i in range(n):
            self.players.append(Player(i, "player_" + str(i)))
        self.button_id = 0

    def run(self):
        self.dealer.shuffle()
        self.dealer.deliver_to_all()
        self.manager.init()
        self.manager.round()
        self.dealer.flop()
        self.manager.round()
        self.dealer.turn()
        self.manager.round()
        self.dealer.river()
        self.manager.round()
        self.dealer.show_hands()
        self.dealer.show_board()
        print(len(self.dealer.piles), " cards left")

        judge = Judge()
        judge.judge(self.dealer.board, self.players)
        self.button_id = (self.button_id + 1) % self.nplayer

    def test1(self):
        self.dealer.shuffle()
        hand0 = [Card(Suit.Heart, Point.Three), Card(Suit.Heart, Point.Four)]
        hand1 = [Card(Suit.Diamond, Point.Ace), Card(Suit.Spade, Point.King)]
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
            winner = judge.judge(board, self.players)
            if winner == 0:
                cnt0 += 1
            elif winner == 1:
                cnt1 += 1
            else:
                deuce += 1
        print("{} | {} winning rate: {}, {} | {} winning rate: {}, deuce: {}".format(hand0[0], hand0[1], 1.0*cnt0/n,
                                                                         hand1[0], hand1[1], 1.0*cnt1/n, 1.0*deuce/n))


if __name__ == "__main__":
    # random.seed(1)
    system = System(2)
    system.run()
    # system.test1()
