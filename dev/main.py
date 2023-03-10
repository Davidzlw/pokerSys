import random
from poker_base import *
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

    def choose(self):
        suit_list = list(Suit)
        point_list = list(Point)
        st = random.choice(suit_list)
        pt = random.choice(point_list)
        return Card(st, pt)

    def draw(self):
        return self.piles.pop()

    def deliver_to_player(self, i):
        self.game.players[i].hand = [self.draw(), self.draw()]

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
            hand[0].print()
            hand[1].print()
            print()

    def show_board(self):
        print("board:")
        for card in self.board:
            card.print()
        print()


class System:
    def __init__(self, n):
        self.dealer = Dealer(self)
        self.judger = Judge()
        self.nplayer = n
        self.players = []
        for i in range(n):
            self.players.append(Player(i, "player_" + str(i)))

    def run(self):
        self.dealer.shuffle()
        self.dealer.deliver_to_all()
        self.dealer.flop()
        self.dealer.turn()
        self.dealer.river()
        self.dealer.show_hands()
        self.dealer.show_board()
        print(len(self.dealer.piles), " cards left")

        judge = Judge()
        judge.judge(self.dealer.board, self.players)


if __name__ == "__main__":
    system = System(2)
    system.run()
