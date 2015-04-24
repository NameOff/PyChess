from pieces import *


def right_moves(x, y, field):
    self = field.coords[x][y]
    c = Color.black if self.color == Color.white else Color.white
    moves = field.coords[x][y].possible_moves(x, y)
    right_moves = []
    piece1 = field.coords[x][y]
    if isinstance(self, King):
        b_places = all_possible_moves(c, field)
        cast1 = self.left_castling(x, b_places)
        cast2 = self.right_castling(x, b_places)
        if cast1:
            moves += cast1
        if cast2:
            moves += cast2
    for place2 in moves:
        piece2 = field.coords[place2[0]][place2[1]]
        field.coords[x][y] = None
        field.coords[place2[0]][place2[1]] = piece1
        king = find_king(self.color, field)
        bad_places = all_possible_moves(c, field)
        if king not in bad_places:
            right_moves.append((place2[0], place2[1]))
        field.coords[x][y] = piece1
        field.coords[place2[0]][place2[1]] = piece2
    return right_moves


def find_king(color, field):
    for i in range(field.height):
        for j in range(field.width):
            if isinstance(field.coords[i][j], King) \
                    and field.coords[i][j].color == color:
                return i, j


def move_is_correct(piece1_ind1, piece1_ind2, piece2_ind1, piece2_ind2, field, info):
    piece = field.coords[piece1_ind1][piece1_ind2]
    if piece is None or piece.color != info.color:
        return False
    possible_moves = right_moves(piece1_ind1, piece1_ind2, field)
    if (piece2_ind1, piece2_ind2) not in possible_moves:
        return False
    return True


def doing_move(piece1, piece2, field, info):
    piece1_ind1 = piece1[0]
    piece1_ind2 = piece1[1]
    piece2_ind1 = piece2[0]
    piece2_ind2 = piece2[1]
    piece = field.coords[piece1_ind1][piece1_ind2]
    if move_is_correct(piece1_ind1, piece1_ind2, piece2_ind1, piece2_ind2, field, info):
        field.coords[piece1_ind1][piece1_ind2] = None
        field.coords[piece2_ind1][piece2_ind2] = piece
        if (piece2_ind2 == 6 or piece2_ind2 == 2) and \
                isinstance(piece, King) and piece.did_not_go:
            if piece2_ind2 > 3:
                field.coords[piece2_ind1][7] = None
                field.coords[piece2_ind1][5] = Rook(info.color, field)
            else:
                field.coords[piece2_ind1][0] = None
                field.coords[piece2_ind1][3] = Rook(info.color, field)

        if isinstance(piece, Pawn):
            if piece2_ind1 < 7 and \
                    isinstance(field.coords[piece2_ind1 + 1][piece2_ind2], Pawn):
                if field.coords[piece2_ind1 + 1][piece2_ind2].long_first_move \
                        and field.coords[piece2_ind1 + 1][piece2_ind2].direction == VerticalDirection.down:
                    field.coords[piece2_ind1 + 1][piece2_ind2] = None
            elif piece2_ind1 > 0 and \
                    isinstance(field.coords[piece2_ind1 - 1][piece2_ind2], Pawn):
                if field.coords[piece2_ind1 - 1][piece2_ind2].long_first_move \
                        and field.coords[piece2_ind1 - 1][piece2_ind2].direction == VerticalDirection.up:
                    field.coords[piece2_ind1 - 1][piece2_ind2] = None

        for i in range(field.width):
            if isinstance(field.coords[3][i], Pawn):
                field.coords[3][i].long_first_move = False
            if isinstance(field.coords[4][i], Pawn):
                field.coords[4][i].long_first_move = False

        if isinstance(piece, Pawn):
            if piece2_ind1 - piece1_ind1 == 2 or piece1_ind1 - piece2_ind1 == 2:
                piece.long_first_move = True

        if info.color == Color.white:
            info.color = Color.black
        else:
            info.color = Color.white
        if isinstance(piece, Rook):
            piece.did_not_go = False
        if isinstance(piece, King):
            piece.did_not_go = False
        info.log.append('%s %s %s %s' % (piece1_ind1, piece1_ind2,
                    piece2_ind1, piece2_ind2))
        info.number_of_move += 1
    else:
        print('Incorrect move!')


def all_possible_moves(color, field):
    moves = []
    for i in range(field.height):
        for j in range(field.width):
            if field.coords[i][j] is not None and field.coords[i][j].color == color:
                for z in field.coords[i][j].possible_moves(i, j):
                    moves.append(z)
    return moves


def checkmate(color, field):
    king = find_king(color, field)
    king1 = king
    for i in range(field.height):
        for j in range(field.width):
            if field.coords[i][j] is not None and field.coords[i][j].color == color:
                for z in right_moves(i, j, field):
                    king = king1
                    if isinstance(field.coords[i][j], King):
                        king = (i, j)
                    piece1 = field.coords[i][j]
                    piece2 = field.coords[z[0]][z[1]]
                    field.coords[z[0]][z[1]] = piece1
                    if isinstance(piece1, King):
                        king = (z[0], z[1])
                    field.coords[i][j] = None
                    moves = all_possible_moves(color, field)
                    if king not in moves:
                        field.coords[i][j] = piece1
                        field.coords[z[0]][z[1]] = piece2
                        return False
                    field.coords[i][j] = piece1
                    field.coords[z[0]][z[1]] = piece2
    return True


def pawn_can_transform(field):
    flag = False
    for i in range(field.width):
        if isinstance(field.coords[0][i], Pawn):
            coords = (0, i)
            flag = True
            break
        elif isinstance(field.coords[7][i], Pawn):
            coords = (7, i)
            flag = True
            break
    if flag:
        pawn = field.coords[coords[0]][coords[1]]
        print('Choose piece: R, N, B, Q')
        pieces = {'R': Rook(pawn.color, field),
                  'N': Knight(pawn.color, field),
                  'B': Bishop(pawn.color, field),
                  'Q': Queen(pawn.color, field)}
        while True:
            piece = input()
            if piece in ['R', 'N', 'B', 'Q']:
                field.coords[coords[0]][coords[1]] = pieces[piece]
                break
            else:
                print('Incorrect input')


def pawn_can_transform_ai(field):
    flag = False
    for i in range(field.width):
        if isinstance(field.coords[0][i], Pawn):
            coords = (0, i)
            flag = True
            break
        elif isinstance(field.coords[7][i], Pawn):
            coords = (7, i)
            flag = True
            break
    if flag:
        pawn = field.coords[coords[0]][coords[1]]
        field.coords[coords[0]][coords[1]] = Queen(pawn.color, field)


def save_game(name, info):
    try:
        with open(name, 'x') as f:
            for i in info.log:
                f.write(i + '\n')
        f.close()
        print('Game saved')
    except:
        print('File already exists')


def is_pat_now(field):
    white_moves = []
    black_moves = []
    for i in range(field.height):
        for j in range(field.width):
            piece = field.coords[i][j]
            if piece is not None and piece.color == Color.white:
                for move in right_moves(i, j, field):
                    white_moves.append(move)
            if piece is not None and piece.color == Color.black:
                for move in right_moves(i, j, field):
                    black_moves.append(move)
    white_king = find_king(Color.white, field)
    black_king = find_king(Color.black, field)
    if len(white_moves) == 0 or len(black_moves) == 0:
        if white_king not in black_moves and \
                black_king not in white_moves:
            return True
    return False


def check(color, field):
    c = Color.white if color == Color.black else Color.black
    bad_places = all_possible_moves(c, field)
    king = find_king(color, field)
    if king in bad_places:
        return True
    return False


def draw(field):
    white_pieces = 0
    black_pieces = 0
    for i in range(field.height):
        for j in range(field.width):
            if field.coords[i][j] is not None:
                if field.coords[i][j].color == Color.white:
                    white_pieces += 1
                else:
                    black_pieces += 1
    if white_pieces == black_pieces == 1:
        return True
    return False
