from random import randint
from mechanic import *


class StupidAI:
    def __init__(self, color, field, info):
        self.color = color
        self.field = field
        self.info = info

    def move(self):
        pieces = []
        for i in range(self.field.height):
            for j in range(self.field.width):
                if self.field.coords[i][j] is not None and\
                    self.field.coords[i][j].color == self.color\
                        and right_moves(i, j, self.field):
                    pieces.append((i, j))
        num1 = randint(0, len(pieces) - 1)
        piece = pieces[num1]
        moves = right_moves(piece[0], piece[1], self.field)
        num2 = randint(0, len(moves) - 1)
        move = moves[num2]
        doing_move((piece[0], piece[1]), (move[0], move[1]), self.field, self.info)
        pawn_can_transform_ai(self.field)