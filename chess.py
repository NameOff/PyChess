from mechanic import *
from stupidAI import *


def arrange_pieces(field, down_color):
    up_color = Color.black
    if down_color == Color.black:
        up_color = Color.white

    pieces = (Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook)
    if down_color == Color.black:
        pieces = (Rook, Knight, Bishop, King, Queen, Bishop, Knight, Rook)
    for (i, x) in enumerate(pieces):
        field.coords[0][i] = x(up_color, field)
        field.coords[7][i] = x(down_color, field)
    field.coords[1] = [Pawn(up_color, field, VerticalDirection.down)] * 8
    field.coords[6] = [Pawn(down_color, field, VerticalDirection.up)] * 8


def input_is_correct(move, field, info):
    if len(move) != 5 or len(move.split(' ')) != 2:
        return False
    flag1 = flag2 = flag3 = flag4 = False
    for i in range(field.height):
        if move[0] != chr(ord('A') + i):
            flag1 = True
        if move[3] != chr(ord('A') + i):
            flag2 = True
    for i in range(1, field.width + 1):
        if int(move[1]) != i:
            flag3 = True
        if int(move[4]) != i:
            flag4 = True
    return flag1 and flag2 and flag3 and flag4


def determine_index(piece):
    return 'ABCDEFGH'.index(piece[0])


def main():
    field = Field(8, 8)
    info = GameInformation()
    print('Select mode: player vs player, player vs AI or AI vs AI. Enter 1, 2 or 3')
    mode = input()
    pl_vs_pl = (mode == '1')
    pl_vs_ai = (mode == '2')
    ai_vs_ai = (mode == '3')
    color = None
    if pl_vs_ai:
        print('Choose the color.', end=' ')
        while color not in ('white', 'black'):
            color = input('Enter "white" or "black": ')
    computer = StupidAI(Color.black, field, info)
    comp2 = StupidAI(Color.white, field, info)
    down_color = Color.white
    if color == 'black':
        down_color = Color.black
        computer.color = Color.white
    arrange_pieces(field, down_color)
    while True:
        pawn_can_transform(field)
        field.print_field()
        if is_pat_now(field):
            print('Pat!')
            print(info.number_of_move)
            break
        if checkmate(Color.white, field):
            print('Black won!')
            print(info.number_of_move)
            break
        if checkmate(Color.black, field):
            print('White won!')
            print(info.number_of_move)
            break
        if check(Color.white, field):
            print('Check for white!')
        if check(Color.black, field):
            print('Check for black!')
        if draw(field):
            print('Draw!')
            print(info.number_of_move)
            break
        if info.color == Color.white:
            print('White move:')
        else:
            print('Black move:')
        if pl_vs_ai or ai_vs_ai:
            if computer.color == info.color:
                computer.move()
                continue
        if ai_vs_ai:
            if comp2.color == info.color:
                comp2.move()
                continue
        input_move = input()
        move = input_move.split()
        if move[0] == 'save':
            save_game(move[1], info)
            continue
        while True:
            if not input_is_correct(input_move, field, info):
                print('Incorrect input')
            else:
                break
            input_move = input()
        move = input_move.split()
        piece1_ind1 = determine_index(move[0][0])
        piece1_ind2 = int(move[0][1])-1
        piece2_ind1 = determine_index(move[1][0])
        piece2_ind2 = int(move[1][1])-1
        first_piece = (piece1_ind1, piece1_ind2)
        second_piece = (piece2_ind1, piece2_ind2)
        doing_move(first_piece, second_piece, field, info)


if __name__ == '__main__':
    main()