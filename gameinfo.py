from enum import Enum


class Color(Enum):
    white = 1
    black = 2


class GameInformation:
    def __init__(self):
        self.color = Color.white
        self.number_of_move = 1
        self.log = []
