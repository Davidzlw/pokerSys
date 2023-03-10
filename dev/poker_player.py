from poker_base import *


class Player:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
        self.hand = []  # [card, card]
