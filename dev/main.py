import random
from poker_base import *
from position import Position
from actions import *
from poker_player import *


class Dealer:
    def __init__(self, game):
        self.game = game
        self.piles = []
        self.board = []

    def init(self):
        self.board = []

    def shuffle(self):
        self.piles.clear()
        for suit in Suit:
            for pt in Point:
                self.piles.append(Card(suit, pt))
        random.shuffle(self.piles)

    def choose_n(self, n):
        board = []
        temp = self.piles.copy()
        random.shuffle(temp)
        for i in range(n):
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

    def preflop(self):
        pass

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
        for i in range(self.game.sys.nplayer):
            print(i, "th player:", self.game.sys.players[i].name)
            hand = self.game.sys.players[i].hand
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
        self.rounds = {"preflop": self.dealer.preflop, "flop": self.dealer.flop,
                        "turn": self.dealer.turn, "river": self.dealer.river}
        self.round_id = 0
        self.max_bet = 0
        self.game_finished = False

    def request(self, player_pos):
        return self.sys.players[player_pos].respond(self)
        # return self.sys.players[player_pos].manual_respond(self)

    def is_round_finished(self):
        act_cnt = 0
        uneven_cnt = 0
        for i, p in enumerate(self.sys.players):
            if not self.sys.manager.fold_map[p.pos] and not self.sys.manager.allin_map[p.pos]:
                act_cnt += 1
                if self.sys.manager.round_bet_map[p.pos] != self.max_bet:
                    uneven_cnt += 1
        if act_cnt <= 1:
            self.game_finished = True
        if uneven_cnt > 0:
            return False
        if self.round_id == 0 and not self.sys.manager.bb_act:
            return False
        return True

    def round(self):
        print("round {{{}}}".format(list(self.rounds.keys())[self.round_id]))
        nplayer = self.sys.nplayer
        begin = sb_pos = (self.sys.button_pos + 1) % nplayer
        bb_pos = (self.sys.button_pos + 2) % nplayer
        if self.round_id == 0:
            self.sys.manager.pre_blind_bet()
            begin = (begin + 2) % nplayer

        player_pos = begin
        while not self.is_round_finished() and not self.game_finished:
            if player_pos == bb_pos:
                self.sys.manager.bb_act = True
            if not self.sys.manager.fold_map[player_pos] and not self.sys.manager.allin_map[player_pos]:
                response = self.request(player_pos)
                assert response.player_pos == player_pos
                self.sys.manager.handle_action(response)
                print("{} th player {}\t {:13} {}, remain: {:4}, pot: {}".format(player_pos, self.sys.players[player_pos].name,
                      response.act, response.amount, self.sys.manager.possession[response.player_pos], self.sys.manager.pot))
            player_pos = (player_pos + 1) % nplayer

        self.sys.manager.round_bet_map = {player.pos: -1 for player in self.sys.players}
        self.max_bet = 0
        self.round_id += 1

    def run(self):
        self.dealer.shuffle()
        self.dealer.deliver_to_all()
        self.sys.manager.every_game_init()

        self.dealer.show_hands()
        for r in self.rounds:
            self.rounds[r]()  # dealer draw cards
            self.dealer.show_board()
            self.round()  # player act
        print("game finished!\n")
        print(len(self.dealer.piles), " cards left")

        unfold_pos = [1 for pos in self.sys.manager.fold_map.keys() if self.sys.manager.fold_map[pos]]
        if len(unfold_pos) == 1:
            self.sys.manager.game_settle(unfold_pos)
            print("winner is {}\n".format(self.sys.players[unfold_pos[0]].id))
        else:
            judge = Judge()
            results = judge.judge(self.dealer.board, self.sys.players, True)
            winner_poses = [result.player.pos for result in results]
            self.sys.manager.game_settle(winner_poses)
        print("=============== end of game ===============\n")

    def hand_run(self, hands):
        self.dealer.shuffle()
        for i, hand in enumerate(hands):
            self.dealer.deliver_specific_to_player(i, hand)

        judge = Judge()

        cnts, chop = [0] * len(hands), 0
        n = 10000
        # board_cards = [Card(Suit.Heart, Point.Jack), Card(Suit.Heart, Point.Ten), Card(Suit.Spade, Point.Three), Card(Suit.Spade, Point.Two)]
        # print("{} | {} | {} | {} | * ".format(board_cards[0], board_cards[1], board_cards[2], board_cards[3]))
        board_cards = []
        [self.dealer.draw_spec(card) for card in board_cards]
        for i in range(n):
            rest_cards = self.dealer.choose_n(5 - len(board_cards))
            board = board_cards + rest_cards
            # msg = ""
            # for card in board:
            #     msg += card.__str__() + ' | '
            # print(msg)
            winners = judge.judge(board, self.sys.players)
            if len(winners) > 1:
                chop += 1
            else:
                cnts[winners[0].player.pos] += 1

        for i, hand in enumerate(hands):
            print("{} | {} winning rate: {}".format(hand[0], hand[1], 1.0 * cnts[i] / n))
        print("chop: {}".format(1.0 * chop / n))


class System:
    def __init__(self):
        self.game = Game(self)
        self.manager = PotManager(self)
        self.nplayer = 0
        self.players = []
        self.button_pos = 0

    def add_player(self, id_, name):
        pos = self.nplayer
        self.players.append(Player(id_, name, pos))
        self.nplayer += 1

    def add_players(self, n: int):
        assert 2 <= n <= 10
        for i in range(n):
            id = self.nplayer
            self.add_player(id, "player_" + str(id))

    # sim a solo game
    def solo(self):
        self.add_players(2)
        self.players[0].set_strategy(Style.Aggressive)
        self.manager.set_same_money(1000)
        self.game.run()

    def test(self):
        hand0 = [Card(Suit.Heart, Point.King), Card(Suit.Club, Point.King)]
        hand1 = [Card(Suit.Diamond, Point.Ace), Card(Suit.Spade, Point.Ace)]
        # hand2 = [Card(Suit.Club, Point.King), Card(Suit.Club, Point.Queen)]
        # hand3 = [Card(Suit.Spade, Point.Five), Card(Suit.Spade, Point.Six)]
        # all_hands = [hand0, hand1, hand2, hand3]
        all_hands = [hand0, hand1]
        self.add_players(len(all_hands))

        self.game.hand_run(all_hands)

    def test_every_enemy(self):
        hand0 = [Card(Suit.Heart, Point.Nine), Card(Suit.Heart, Point.Ten)]
        for suit in Suit:
            for pt in Point:
                if Card(suit, pt) == hand0[0] or Card(suit, pt) == hand0[1]:
                    continue
                for suit1 in Suit:
                    for pt1 in Point:
                        if Card(suit1, pt1) == hand0[0] or Card(suit1, pt1) == hand0[1] or Card(suit, pt) == Card(suit1, pt1):
                            continue
                        hand1 = [Card(suit1, pt1), Card(suit, pt)]
                        self.game.hand_run([hand0, hand1])


class Tester:
    def __init__(self):
        pass

    def case0_test_2p_solo_game(self):
        system = System()
        system.solo()

    def case1_test_preflop_allin_blind(self):
        random.seed(1)
        system = System()
        system.add_players(2)
        system.players[0].set_strategy(Style.Aggressive)
        system.manager.set_money(0, 1000)
        system.manager.set_money(1, 1)
        system.game.run()
        assert system.manager.possession[1] == 3

    def case2_test_2p_aggressive(self):
        random.seed(1)
        system = System()
        system.add_players(2)
        system.players[0].set_strategy(Style.Aggressive)
        system.players[1].set_strategy(Style.Aggressive)
        system.manager.set_same_money(1000)
        system.game.run()


if __name__ == "__main__":
    random.seed(1)
    # system.test()
    t = Tester()
    # t.case0_test_2p_solo_game()
    # t.case1_test_preflop_allin_blind()
    t.case2_test_2p_aggressive()



