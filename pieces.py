from field import *
from gameinfo import *
from functools import reduce


class VerticalDirection(Enum):
    up = 1
    down = -1


class HorizontalDirection(Enum):
    left = -1
    right = 1


class Pawn:
    def __init__(self, color, field, direction):
        self.color = color
        self.field = field
        self.long_first_move = False
        self.direction = direction
        self.value = 1
        self.blackColorImage = 'images/bP.png'
        self.whiteColorImage = 'images/wP.png'

    def possible_moves(self, x, y):
        moves = []
        if self.direction == VerticalDirection.up:
            if x == 6 and self.field.coords[x-2][y] is None and \
                    self.field.coords[x-1][y] is None:
                moves.append((4, y))
            if x > 0 and self.field.coords[x-1][y] is None:
                moves.append((x-1, y))
            if self.field.coords[x-1][y-1] is not None and \
                    self.field.coords[x-1][y-1].color != self.color:
                moves.append((x-1, y-1))
            if x > 0 and y < 7 and self.field.coords[x-1][y+1] is not None \
                    and self.field.coords[x-1][y+1].color != self.color:
                moves.append((x-1, y+1))
        else:
            if x == 1 and self.field.coords[x+2][y] is None and self.field.coords[x+1][y] is None:
                moves.append((3, y))
            if x < 7 and self.field.coords[x+1][y] is None:
                moves.append((x+1, y))
            if x < 7 and y > 0 and self.field.coords[x+1][y-1] is not None \
                    and self.field.coords[x+1][y-1].color != self.color:
                moves.append((x+1, y-1))
            if x < 7 and y < 7 and self.field.coords[x+1][y+1] is not None \
                    and self.field.coords[x+1][y+1].color != self.color:
                moves.append((x+1, y+1))
        passant = self.__passant__(x, y)
        for move in passant:
            moves.append(move)
        return moves

    def __passant__(self, x, y):
        moves = []
        if self.direction == VerticalDirection.up:
            if x == 3 and y > 0 and isinstance(self.field.coords[x][y-1], Pawn) and \
                    self.field.coords[x][y-1].long_first_move and self.field.coords[x][y-1].color != self.color:
                moves.append((x-1, y-1))
            if x == 3 and y < 7 and isinstance(self.field.coords[x][y+1], Pawn) and \
                    self.field.coords[x][y+1].long_first_move and self.field.coords[x][y+1].color != self.color:
                moves.append((x-1, y+1))
        else:
            if x == 4 and y > 0 and isinstance(self.field.coords[x][y-1], Pawn) and \
                    self.field.coords[x][y-1].long_first_move and self.field.coords[x][y-1].color != self.color:
                moves.append((x+1, y-1))
            if x == 4 and y < 7 and isinstance(self.field.coords[x][y+1], Pawn) and \
                    self.field.coords[x][y+1].long_first_move and self.field.coords[x][y+1].color != self.color:
                moves.append((x+1, y+1))
        return moves

    def __str__(self):
        if self.color == Color.black:
            return 'BP'
        return 'WP'


class Knight:
    def __init__(self, color, field):
        self.color = color
        self.field = field
        self.value = 2
        self.blackColorImage = 'images/bN.png'
        self.whiteColorImage = 'images/wN.png'

    def __moves_of_knight__(self, x, y, c1, c2):
        moves = []
        if 0 <= x+c1 < self.field.height and 0 <= y+c2 < self.field.width:
            if self.field.coords[x+c1][y+c2] is None:
                moves.append((x+c1, y+c2))
            elif self.field.coords[x+c1][y+c2].color != self.color:
                moves.append((x+c1, y+c2))
        return moves

    def possible_moves(self, x, y):
        moves = []
        for i in (-2, -1, 1, 2):
            j = 2
            if not i % 2:
                j = 1
            moves += self.__moves_of_knight__(x, y, i, j)
            moves += self.__moves_of_knight__(x, y, i, -j)
        return moves

    def __str__(self):
        if self.color == Color.black:
            return 'BN'
        return 'WN'


def moves_of_bishop(i, j, c1, c2, color, field):
    moves = []
    x = i + c1
    y = j + c2
    while 0 <= x < field.height and 0 <= y < field.height:
        if field.coords[x][y] is None:
            moves.append((x, y))
        elif field.coords[x][y].color == color:
            break
        elif field.coords[x][y].color != color:
            moves.append((x, y))
            break
        x = x + c1
        y = y + c2
    return moves


class Bishop:
    def __init__(self, color, field):
        self.color = color
        self.field = field
        self.value = 2
        self.blackColorImage = 'images/bB.png'
        self.whiteColorImage = 'images/wB.png'

    def possible_moves(self, x, y):
        moves = [moves_of_bishop(x, y, dx, dy, self.color, self.field) for dx in (-1, 1) for dy in (-1, 1)]
        return reduce(lambda x, y: x + y, moves)

    def __str__(self):
        if self.color == Color.black:
            return 'BB'
        return 'WB'


def horizontal_moves_of_rook(x, y, direction, color, field):
    moves = []
    c = 1
    if direction == HorizontalDirection.right:
        c = -1
    end = field.width if c != -1 else c
    for i in range(y+c, end, c):
        if field.coords[x][i] is None:
            moves.append((x, i))
        elif field.coords[x][i].color == color:
            break
        elif field.coords[x][i].color != color:
            moves.append((x, i))
            break
    return moves


def vertical_moves_of_rook(x, y, direction, color, field):
    moves = []
    c = 1
    if direction == VerticalDirection.down:
        c = -1
    end = field.height if c != -1 else c
    for i in range(x+c, end, c):
        if field.coords[i][y] is None:
            moves.append((i, y))
        elif field.coords[i][y].color == color:
            break
        elif field.coords[i][y].color != color:
            moves.append((i, y))
            break
    return moves


class Rook:
    def __init__(self, color, field):
        self.color = color
        self.field = field
        self.did_not_go = True
        self.value = 3
        self.blackColorImage = 'images/bR.png'
        self.whiteColorImage = 'images/wR.png'

    def possible_moves(self, x, y):
        possible_moves = []
        for direction in (VerticalDirection.up, VerticalDirection.down):
            possible_moves += vertical_moves_of_rook(x, y, direction, self.color, self.field)
        for direction in (HorizontalDirection.left, HorizontalDirection.right):
            possible_moves += horizontal_moves_of_rook(x, y, direction, self.color, self.field)
        return possible_moves

    def __str__(self):
        if self.color == Color.black:
            return 'BR'
        return 'WR'


class Queen:
    def __init__(self, color, field):
        self.color = color
        self.field = field
        self.value = 4
        self.blackColorImage = 'images/bQ.png'
        self.whiteColorImage = 'images/wQ.png'

    def possible_moves(self, x, y):
        possible_moves = []
        for direction in (VerticalDirection.up, VerticalDirection.down):
            possible_moves += vertical_moves_of_rook(x, y, direction, self.color, self.field)
        for direction in (HorizontalDirection.left, HorizontalDirection.right):
            possible_moves += horizontal_moves_of_rook(x, y, direction, self.color, self.field)
        moves = [moves_of_bishop(x, y, dx, dy, self.color, self.field) for dx in (-1, 1) for dy in (-1, 1)]
        possible_moves += reduce(lambda x, y: x + y, moves)
        return possible_moves

    def __str__(self):
        if self.color == Color.black:
            return 'BQ'
        return 'WQ'


class King:
    def __init__(self, color, field):
        self.color = color
        self.field = field
        self.did_not_go = True
        self.blackColorImage = 'images/bK.png'
        self.whiteColorImage = 'images/wK.png'

    def right_castling(self, i, bad_places):
        moves = []
        if self.did_not_go:
            if isinstance(self.field.coords[i][7], Rook) and self.field.coords[i][7].did_not_go:
                if (i, 4) in bad_places \
                        or (i, 5) in bad_places or (i, 6) in bad_places \
                        or (i, 7) in bad_places:
                    return
                if self.field.coords[i][5] is not None or self.field.coords[i][6] is not None:
                    return
                moves.append((i, 6))
        return moves

    def left_castling(self, i, bad_places):
        moves = []
        if self.did_not_go:
            if isinstance(self.field.coords[i][0], Rook) and \
                    self.field.coords[i][0].did_not_go:
                if (i, 0) in bad_places \
                        or (i, 1) in bad_places or (i, 2) in bad_places \
                        or (i, 3) in bad_places or (i, 4) in bad_places:
                    return
                if self.field.coords[i][1] is not None or \
                                self.field.coords[i][2] is not None\
                        or self.field.coords[i][3] is not None:
                    return
                moves.append((i, 2))
        return moves

    def __moves_of_king__(self, i, j):
        moves = []
        if self.field.coords[i][j] is None or self.field.coords[i][j].color != self.color:
            moves.append((i, j))
        return moves

    def possible_moves(self, x, y):
        possible_moves = []
        for dx in (0, -1, 1):
            for dy in (-1, 1):
                if 0 <= x + dx < self.field.width and 0 <= y + dy < self.field.height:
                    possible_moves.append((x + dx, y + dy))
        for dx in (-1, 1):
            if 0 <= x + dx < self.field.width:
                possible_moves.append((x + dx, y))

        return possible_moves

    def __str__(self):
        if self.color == Color.black:
            return 'BK'
        return 'WK'
