from pieces import *


def right_moves(x, y, field):
    self = field.coords[x][y]
    c = Color.black if self.color == Color.white else Color.white
    moves = correct_moves(x, y, field)
    right_moves = []
    piece1 = field.coords[x][y]
    if isinstance(self, King):
        b_places = all_possible_moves(c, field)
        left_castling(x, moves, b_places, field, self)
        right_castling(x, moves, b_places, field, self)
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


def correct_moves(x, y, field):
    moves = []
    if isinstance(field.coords[x][y], Pawn):
        moves = pawn_possible_moves(x, y, field)
    elif isinstance(field.coords[x][y], Rook):
        moves = rook_possible_moves(x, y, field)
    elif isinstance(field.coords[x][y], Bishop):
        moves = bishop_possible_moves(x, y, field)
    elif isinstance(field.coords[x][y], Queen):
        moves = queen_possible_moves(x, y, field)
    elif isinstance(field.coords[x][y], King):
        moves = king_possible_moves(x, y, field)
    elif isinstance(field.coords[x][y], Knight):
        moves = knight_possible_moves(x, y, field)
    return moves


def pawn_dangerous_moves(x, y, direction, moves):
    if direction == Direction.up:
        moves.append((x-1, y-1))
        moves.append((x-1, y+1))
    else:
        moves.append((x+1, y-1))
        moves.append((x+1, y+1))


def passant(x, y, moves, field):
    direction = field.coords[x][y].direction
    if direction == Direction.up:
        if x > 0 and y > 0 and isinstance(field.coords[x][y-1], Pawn) and \
                field.coords[x][y-1].long_first_move:
            moves.append((x-1, y-1))
        if x > 0 and y < 7 and isinstance(field.coords[x][y+1], Pawn) and \
                field.coords[x][y+1].long_first_move:
            moves.append((x-1, y+1))
    else:
        if x < 7 and y > 0 and isinstance(field.coords[x][y-1], Pawn) and \
                field.coords[x][y-1].long_first_move:
            moves.append((x+1, y-1))
        if x < 7 and y < 7 and isinstance(field.coords[x][y+1], Pawn) and \
                field.coords[x][y+1].long_first_move:
            moves.append((x+1, y+1))


def pawn_dangerous_moves(x, y, direction):
    moves = []
    if direction == Direction.down:
        moves.append((x+1, y+1))
        moves.append((x+1, y-1))
    else:
        moves.append((x-1, y-1))
        moves.append((x-1, y+1))
    return moves


def pawn_possible_moves(x, y, field):
    moves = []
    pawn = field.coords[x][y]
    direction = pawn.direction
    if direction == Direction.up:
        if x == 6 and field.coords[x-2][y] is None and \
                field.coords[x-1][y] is None:
            moves.append((4, y))
        if x > 0 and field.coords[x-1][y] is None:
            moves.append((x-1, y))
        if field.coords[x-1][y-1] is not None and \
                field.coords[x-1][y-1].color != pawn.color:
            moves.append((x-1, y-1))
        if x > 1 and y < 7 and field.coords[x-1][y+1] is not None \
                and field.coords[x-1][y+1].color != pawn.color:
            moves.append((x-1, y+1))
    else:
        if x == 1 and field.coords[x+2][y] is None and field.coords[x+1][y] is None:
            moves.append((3, y))
        if x < 7 and field.coords[x+1][y] is None:
            moves.append((x+1, y))
        if x < 7 and y > 0 and field.coords[x+1][y-1] is not None \
                and field.coords[x+1][y-1].color != pawn.color:
            moves.append((x+1, y-1))
        if x < 7 and y < 7 and field.coords[x+1][y+1] is not None \
                and field.coords[x+1][y+1].color != pawn.color:
            moves.append((x+1, y+1))
    passant(x, y, moves, field)
    return moves


def moves_of_rook_1(x, y, c, color, moves, field):
    end = field.width if c != -1 else c
    for i in range(y+c, end, c):
            if field.coords[x][i] is None:
                moves.append((x, i))
            elif field.coords[x][i].color == color:
                break
            elif field.coords[x][i].color != color:
                moves.append((x, i))
                break


def moves_of_rook_2(x, y, c, color, moves, field):
    end = field.height if c != -1 else c
    for i in range(x+c, end, c):
        if field.coords[i][y] is None:
            moves.append((i, y))
        elif field.coords[i][y].color == color:
            break
        elif field.coords[i][y].color != color:
            moves.append((i, y))
            break


def rook_possible_moves(x, y, field):
    moves = []
    self = field.coords[x][y]
    moves_of_rook_1(x, y, -1, self.color, moves, field)
    moves_of_rook_1(x, y, 1, self.color, moves, field)
    moves_of_rook_2(x, y, -1, self.color, moves, field)
    moves_of_rook_2(x, y, 1, self.color, moves, field)
    return moves


def moves_of_bishop(i, j, c1, c2, color, moves, field):
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


def bishop_possible_moves(x, y, field):
    moves = []
    self = field.coords[x][y]
    moves_of_bishop(x, y, -1, -1, self.color, moves, field)
    moves_of_bishop(x, y, -1, 1, self.color, moves, field)
    moves_of_bishop(x, y, 1, -1, self.color, moves, field)
    moves_of_bishop(x, y, 1, 1, self.color, moves, field)
    return moves


def queen_possible_moves(x, y, field):
    moves = []
    self = field.coords[x][y]
    moves_of_bishop(x, y, -1, -1, self.color, moves, field)
    moves_of_bishop(x, y, -1, 1, self.color, moves, field)
    moves_of_bishop(x, y, 1, -1, self.color, moves, field)
    moves_of_bishop(x, y, 1, 1, self.color, moves, field)
    moves_of_rook_1(x, y, -1, self.color, moves, field)
    moves_of_rook_1(x, y, 1, self.color, moves, field)
    moves_of_rook_2(x, y, -1, self.color, moves, field)
    moves_of_rook_2(x, y, 1, self.color, moves, field)
    return moves


def moves_of_king(i, j, moves, field, color):
    if field.coords[i][j] is None or field.coords[i][j].color != color:
        moves.append((i, j))


def right_castling(i, moves, bad_places, field, king):
    if king.did_not_go:
        if isinstance(field.coords[i][7], Rook) and field.coords[i][7].did_not_go:
            if (i, 4) in bad_places \
                    or (i, 5) in bad_places or (i, 6) in bad_places \
                    or (i, 7) in bad_places:
                return
            if field.coords[i][5] is not None or field.coords[i][6] is not None:
                return
            moves.append((i, 6))
    return


def left_castling(i, moves, bad_places, field, king):
    if king.did_not_go:
        if isinstance(field.coords[i][0], Rook) and \
                field.coords[i][0].did_not_go:
            if (i, 0) in bad_places \
                    or (i, 1) in bad_places or (i, 2) in bad_places \
                    or (i, 3) in bad_places or (i, 4) in bad_places:
                return
            if field.coords[i][1] is not None or \
                            field.coords[i][2] is not None\
                    or field.coords[i][3] is not None:
                return
            moves.append((i, 2))
    else:
        return


def king_possible_moves(x, y, field):
    moves = []
    self = field.coords[x][y]
    if x > 0 and y > 0:
        moves_of_king(x-1, y-1, moves, field, self.color)
    if x > 0:
        moves_of_king(x-1, y, moves, field, self.color)
    if x > 0 and y < 7:
        moves_of_king(x-1, y+1, moves, field, self.color)
    if y < 7:
        moves_of_king(x, y+1, moves, field, self.color)
    if y > 0:
        moves_of_king(x, y-1, moves, field, self.color)
    if y > 0 and x < 7:
        moves_of_king(x+1, y-1, moves, field, self.color)
    if x < 7:
        moves_of_king(x+1, y, moves, field, self.color)
    if y < 7 and x < 7:
        moves_of_king(x+1, y+1, moves, field, self.color)
    return moves



def moves_of_knight(x, y, c1, c2, color, moves, field):
    if 0 <= x+c1 < field.height and 0 <= y+c2 < field.width:
        if field.coords[x+c1][y+c2] is None:
                moves.append((x+c1, y+c2))
        elif field.coords[x+c1][y+c2].color != color:
            moves.append((x+c1, y+c2))


def knight_possible_moves(x, y, field):
    moves = []
    self = field.coords[x][y]
    moves_of_knight(x, y, -2, 1, self.color, moves, field)
    moves_of_knight(x, y, -1, 2, self.color, moves, field)
    moves_of_knight(x, y, 1, 2, self.color, moves, field)
    moves_of_knight(x, y, 2, 1, self.color, moves, field)
    moves_of_knight(x, y, 2, -1, self.color, moves, field)
    moves_of_knight(x, y, 1, -2, self.color, moves, field)
    moves_of_knight(x, y, -1, -2, self.color, moves, field)
    moves_of_knight(x, y, -2, -1, self.color, moves, field)
    return moves


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
                        and field.coords[piece2_ind1 + 1][piece2_ind2].direction == Direction.down:
                    field.coords[piece2_ind1 + 1][piece2_ind2] = None
            elif piece2_ind1 > 0 and \
                    isinstance(field.coords[piece2_ind1 - 1][piece2_ind2], Pawn):
                if field.coords[piece2_ind1 - 1][piece2_ind2].long_first_move \
                        and field.coords[piece2_ind1 - 1][piece2_ind2].direction == Direction.up:
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
                for z in correct_moves(i, j, field):
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
        print('Choose piece: R, N, B, Q')
        while True:
            piece = input()
            pawn = field.coords[coords[0]][coords[1]]
            if piece == 'R':
                field.coords[coords[0]][coords[1]] = Rook(pawn.color, field)
                break
            elif piece == 'N':
                field.coords[coords[0]][coords[1]] = Knight(pawn.color, field)
                break
            elif piece == 'B':
                field.coords[coords[0]][coords[1]] = Bishop(pawn.color, field)
                break
            elif piece == 'Q':
                field.coords[coords[0]][coords[1]] = Queen(pawn.color, field)
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
        f = open(name, 'x')
        for i in info.log:
            f.write(i + '\n')
        f.close()
        print('Game saved')
    except:
        print('File already exists')


def input_is_correct(move, field, info):
    if len(move) != 5 or len(move.split(' ')) != 2:
        return False
    inf = move.split(' ')
    flag1 = flag2 = flag3 = flag4 = False
    for i in range(field.height):
        if move[0] == chr(ord('A') + i):
            flag1 = True
        if move[3] == chr(ord('A') + i):
            flag2 = True
    for i in range(1, field.width + 1):
        if int(move[1]) == i:
            flag3 = True
        if int(move[4]) == i:
            flag4 = True
    return flag1 and flag2 and flag3 and flag4


def is_pat_now(field):
    all_white_moves = all_possible_moves(Color.white, field)
    all_black_moves = all_possible_moves(Color.black, field)
    white_king = find_king(Color.white, field)
    black_king = find_king(Color.black, field)
    if not all_white_moves or not all_black_moves:
        if white_king not in all_black_moves and \
                black_king not in all_white_moves:
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