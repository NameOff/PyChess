from field import *
from gameinfo import *


class Direction(Enum):
    up = 1
    down = 2


class Pawn:
    def __init__(self, color, field, direction):
        self.color = color
        self.field = field
        self.long_first_move = False
        self.direction = direction
        self.value = 1

    def __str__(self):
        if self.color == Color.black:
            return 'BP'
        return 'WP'


class Knight:
    def __init__(self, color, field):
        self.color = color
        self.field = field
        self.value = 2

    def __str__(self):
        if self.color == Color.black:
            return 'BN'
        return 'WN'


class Bishop:
    def __init__(self, color, field):
        self.color = color
        self.field = field
        self.value = 2

    def __str__(self):
        if self.color == Color.black:
            return 'BB'
        return 'WB'


class Rook:
    def __init__(self, color, field):
        self.color = color
        self.field = field
        self.did_not_go = True
        self.value = 3

    def __str__(self):
        if self.color == Color.black:
            return 'BR'
        return 'WR'


class Queen:
    def __init__(self, color, field):
        self.color = color
        self.field = field
        self.value = 4

    def __str__(self):
        if self.color == Color.black:
            return 'BQ'
        return 'WQ'


class King:
    def __init__(self, color, field):
        self.color = color
        self.field = field
        self.did_not_go = True

    def __str__(self):
        if self.color == Color.black:
            return 'BK'
        return 'WK'
