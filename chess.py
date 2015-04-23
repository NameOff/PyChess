from mechanic import *
from stupidAI import *


def arrange_pieces(field, down_color):
    up_color = Color.black
    if down_color == Color.black:
        up_color = Color.white
    for i in range(field.height):
        for j in range(field.width):
            field.coords[i].append(None)
    pieces = (Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook)
    if down_color == Color.black:
        pieces = (Rook, Knight, Bishop, King, Queen, Bishop, Knight, Rook)
    for (i, x) in enumerate(pieces):
        field.coords[0][i] = x(up_color, field)
        field.coords[7][i] = x(down_color, field)
    for i in range(8):
        field.coords[1][i] = Pawn(up_color, field, Direction.down)

    for i in range(8):
        field.coords[6][i] = Pawn(down_color, field, Direction.up)


def determine_index(piece):
    return 'ABCDEFGH'.index(piece[0])


def main():
    field = Field(8, 8)
    info = GameInformation()
    print('Select mode: player vs player, player vs AI or AI vs AI. Enter 1, 2 or 3')
    mode = input()
    pl_vs_pl = False
    pl_vs_ai = False
    ai_vs_ai = False
    if mode == '1' or mode == '2' or mode == '3':
        if mode == '1':
            pl_vs_pl = True
        if mode == '2':
            pl_vs_ai = True
        if mode == '3':
            ai_vs_ai = True
    color = 'white'
    if pl_vs_ai:
        print('Choose your color. Enter white or black')
        color = input()
        while color != 'white' and color != 'black':
            print('Enter white or black')
            color = input()
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