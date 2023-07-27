import random
from enum import Enum
from enum import IntEnum
from poker_player import Player


class Suit(Enum):
    Heart = 0
    Diamond = 1
    Spade = 2
    Club = 3

    def short(self):
        if self == Suit.Heart:
            return "♡"
        elif self == Suit.Diamond:
            return "♢"
        elif self == Suit.Spade:
            return "♤"
        elif self == Suit.Club:
            return "♧"

    def __str__(self):
        return "{}".format(self.short())


class Point(IntEnum):
    Two = 2
    Three = 3
    Four = 4
    Five = 5
    Six = 6
    Seven = 7
    Eight = 8
    Nine = 9
    Ten = 10
    Jack = 11
    Queen = 12
    King = 13
    Ace = 14

    def short(self):
        if int(self) == 11:
            return "J"
        elif int(self) == 12:
            return "Q"
        elif int(self) == 13:
            return "K"
        elif int(self) == 14:
            return "A"
        return str(int(self))

    def __str__(self):
        return "{}".format(self.short())


class Card:
    def __init__(self, suit: Suit, point: Point):
        self.suit = suit
        self.point = point

    def __str__(self):
        return "{} {}".format(self.suit, self.point)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False


class Categories:
    def __init__(self):
        self.cat_name = ""

    def print(self):
        print(self.info())

class HighCard(Categories):
    def __init__(self, points: [int]):
        super().__init__()
        self.cat_name = "HighCard"
        self.rank = 1
        self.points = points

    def info(self):
        return "points: {}".format(self.points)


class Pair(Categories):
    def __init__(self, pair: int, kickers: [int]):
        super().__init__()
        self.cat_name = "Pair"
        self.rank = 2
        self.pair = pair
        self.kickers = kickers

    def info(self):
        return "pair: {}, kickers: {} {} {}".format(self.pair, self.kickers[0], self.kickers[1], self.kickers[2])

class TwoPair(Categories):
    def __init__(self, tpair: int, npair: int, kicker: int):
        super().__init__()
        self.cat_name = "TwoPair"
        self.rank = 3
        self.tpair = tpair
        self.npair = npair
        self.kicker = kicker

    def info(self):
        return "tpair: {}, npair: {}, kicker: {}".format(self.tpair, self.npair, self.kicker)

class Set(Categories):
    def __init__(self, set: int, kickers: [int]):
        super().__init__()
        self.cat_name = "Set"
        self.rank = 4
        self.set = set
        self.kickers = kickers

    def info(self):
        return "set: {}, kickers: {} {}".format(self.set, self.kickers[0], self.kickers[1])

class Straight(Categories):
    def __init__(self, high: int):
        super().__init__()
        self.cat_name = "Straight"
        self.rank = 5
        self.high = high

    def info(self):
        return "high: {}".format(self.high)

class Flush(Categories):
    def __init__(self, suit: Suit, points: [int]):
        super().__init__()
        self.cat_name = "Flush"
        self.rank = 6
        self.suit = suit
        self.points = points

    def info(self):
        return "suit: {}, points: {} {} {} {} {}".format(self.suit, self.points[0], self.points[1],
                                                         self.points[2], self.points[3], self.points[4])

class FullHouse(Categories):
    def __init__(self, set: int, pair: int):
        super().__init__()
        self.cat_name = "FullHouse"
        self.rank = 7
        self.set = set
        self.pair = pair

    def info(self):
        return "set: {}, pair: {}".format(self.set, self.pair)

class Quart(Categories):
    def __init__(self, quart: int, kicker: int):
        super().__init__()
        self.cat_name = "Quart"
        self.rank = 8
        self.quart = quart
        self.kicker = kicker

    def info(self):
        return "quart: {}, kicker: {}".format(self.quart, self.kicker)

class StraightFlush(Categories):
    def __init__(self, suit: Suit, high: int):
        super().__init__()
        self.cat_name = "StraightFlush"
        self.rank = 9
        self.suit = suit
        self.high = high

    def info(self):
        return "suit: {}, high: {}".format(self.suit, self.high)


class Result:
    def __init__(self, player: Player, cat: Categories):
        self.player = player
        self.cat = cat


class Judge:
    def __init__(self):
        self.board = []

    def count_suit(self, combine: []):
        cnt = {}
        for suit in Suit:
            cnt[suit] = 0
        for card in combine:
            cnt[card.suit] += 1
        return cnt

    def count_point(self, combine: []):
        cnt = {}
        for point in Point:
            cnt[point] = 0
        for card in combine:
            cnt[card.point] += 1
        return cnt

    # 2 3 4 5 6 7, highest_straight is 3
    def highest_straight(self, combine: []):
        cnt = self.count_point(combine)
        cnt[1] = cnt[14]
        highest = 0
        for i in range(2, 11):
            ok = 1
            for j in range(5):
                if cnt[i + j] < 1:
                    ok = 0
                    break
            if ok:
                highest = i
        return highest

    # return a Category
    def rank(self, combine: []):
        assert len(combine) == 7
        # combine.sort(key=lambda x: x.point)
        points_cnt = self.count_point(combine)
        suit_cnt = self.count_suit(combine)
        is_suited = False
        if max(suit_cnt.values()) >= 5:
            is_suited = True
            suit = next(key for key in suit_cnt.keys() if suit_cnt[key] >= 5)
            flush_cards = [card for card in combine if card.suit == suit]
            if self.highest_straight(flush_cards) > 0:
                return StraightFlush(suit, self.highest_straight(flush_cards))

        if max(points_cnt.values()) == 4:
            quart = max([key for key in points_cnt.keys() if points_cnt[key] == 4])
            kicker = max(key for key in points_cnt.keys() if points_cnt[key] >= 1 and key != quart)
            return Quart(quart, kicker)

        if max(points_cnt.values()) == 3:
            set = max([key for key in points_cnt.keys() if points_cnt[key] == 3])
            pairs = [key for key in points_cnt.keys() if points_cnt[key] >= 2 and key != set]
            if pairs:
                return FullHouse(set, max(pairs))

        if is_suited:
            suit = next(key for key in suit_cnt.keys() if suit_cnt[key] >= 5)
            points = sorted([card.point for card in combine if card.suit == suit], reverse=True)
            return Flush(suit, points)

        if self.highest_straight(combine) > 0:
            return Straight(self.highest_straight(combine))

        if max(points_cnt.values()) == 3:
            set = max([key for key in points_cnt.keys() if points_cnt[key] == 3])
            rest = sorted([key for key in points_cnt.keys() if points_cnt[key] >= 1 and key != set], reverse=True)
            kickers = rest[:2]
            return Set(set, kickers)

        if max(points_cnt.values()) == 2:
            tpair = max(key for key in points_cnt.keys() if points_cnt[key] == 2)
            rest_pairs = [key for key in points_cnt.keys() if points_cnt[key] == 2 and key != tpair]
            if rest_pairs:
                npair = max(rest_pairs)
                kicker = max(key for key in points_cnt.keys() if points_cnt[key] >= 1 and key != tpair and key != npair)
                return TwoPair(tpair, npair, kicker)
            rest_points = sorted([key for key in points_cnt.keys() if points_cnt[key] >= 1 and key != tpair], reverse=True)
            return Pair(tpair, rest_points[:3])

        return HighCard(list(points_cnt.keys())[:5])

    # return a list of Result that wins
    def pk(self, results):
        highest_rank = max(result.cat.rank for result in results)
        highest_results = [result for result in results if result.cat.rank == highest_rank]
        if len(highest_results) == 1:
            return [highest_results[0]]
        if highest_rank == 9:  # StraightFlush
            high = max(res.cat.high for res in highest_results)
            return [res for res in highest_results if res.cat.high == high]
        elif highest_rank == 8:  # Quart
            highest_results.sort(key=lambda x: x.cat.quart * 20 + x.cat.kicker, reverse=True)
            quart = highest_results[0].cat.quart
            kicker = highest_results[0].cat.kicker
            return [res for res in highest_results if res.cat.quart == quart and res.cat.kicker == kicker]
        elif highest_rank == 7:  # FullHouse
            highest_results.sort(key=lambda x: x.cat.set * 20 + x.cat.pair, reverse=True)
            set = highest_results[0].cat.set
            pair = highest_results[0].cat.pair
            return [res for res in highest_results if res.cat.set == set and res.cat.pair == pair]
        elif highest_rank == 6:  # Flush
            highest_results.sort(key=lambda x: x.cat.points, reverse=True)
            points = highest_results[0].cat.points
            return [res for res in highest_results if res.cat.points == points]
        elif highest_rank == 5:  # Straight
            high = max(res.cat.high for res in highest_results)
            return [res for res in highest_results if res.cat.high == high]
        elif highest_rank == 4:  # Set
            set = max(res.cat.set for res in highest_results)
            candidate = [res for res in highest_results if res.cat.set == set]
            candidate.sort(key=lambda x: x.cat.kickers, reverse=True)
            return [res for res in candidate if res.cat.kickers == candidate[0].cat.kickers]
        elif highest_rank == 3:  # TwoPair
            highest_results.sort(key=lambda x: x.cat.tpair * 400 + x.cat.npair * 20 + x.cat.kicker, reverse=True)
            tpair = highest_results[0].cat.tpair
            npair = highest_results[0].cat.npair
            kicker = highest_results[0].cat.kicker
            return [res for res in highest_results if res.cat.tpair == tpair and res.cat.npair == npair and res.cat.kicker == kicker]
        elif highest_rank == 2:  # Pair
            pair = max(res.cat.pair for res in highest_results)
            candidate = [res for res in highest_results if res.cat.pair == pair]
            candidate.sort(key=lambda x: x.cat.kickers, reverse=True)
            return [res for res in candidate if res.cat.kickers == candidate[0].cat.kickers]
        else:  # HighCard
            highest_results.sort(key=lambda x: x.cat.points, reverse=True)
            return [res for res in highest_results if res.cat.points == highest_results[0].cat.points]

    def judge(self, board: [Card], players: []):
        self.board = board.copy()
        assert len(self.board) == 5
        # print("judge result:")
        results = []
        for player in players:
            hand = player.hand
            res = self.rank(self.board + hand)
            results.append(Result(player, res))
            # print(player.name, res.cat_name)
        winners = self.pk(results)
        for winner in winners:
            need_print = True
            if need_print:
                print("winner(s) is {} with {}, {}\n".format(winner.player.id,
                                                             winner.cat.cat_name, winner.cat.info()))
        return winners

