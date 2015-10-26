from enum import Enum


class Color(Enum):
    white = 1
    black = 2


class GameInformation:
    def __init__(self, downColor=None):
        self.downColor = downColor
        self.upColor = Color.white
        if self.downColor == self.upColor:
            self.upColor = color.black
        self.color = Color.white
        self.number_of_move = 1
        self.log = []
