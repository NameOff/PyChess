import sys
from guiField import Board
from menu import Menu, Button
from mechanic import *
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QCursor, QIcon
from PyQt5.QtCore import Qt


class PyChess(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.set_initial_init()
        self.board = Board(self)
        self.menu = Menu(self)
        self.ok_button = Button('images/ok.png', self._ok, (265, 250), (65, 55), self)
        self.ok_button.close()
        self.back_to_menu_button = Button('images/back_to_menu', self._back_to_menu, (560, 0), (300, 55), self)
        self.back_to_menu_button.close()
        #self.close()
        self.setGeometry(200, 75, 860, 560)
        self.setWindowTitle('PyChess')
        self.setWindowIcon(QIcon('images/icon.png'))
        self.show()

    def set_initial_init(self):
        self.game_over = True
        self.pawn = None
        self.is_checkmate = False
        self.is_pat = False
        self.is_white_won = False
        self.is_black_won = False
        self.pawn_can_transform = False

    def _back_to_menu(self):
        self.back_to_menu_button.close()
        self.menu.is_active = True
        self.menu.start()

    def _ok(self):
        self.ok_button.close()
        self.is_white_won = False
        self.is_black_won = False
        self.is_pat = False
        self.repaint()

    def __transform_pawn__(self):
        self.pawn_can_transform = True
        img_start = 'images/w'
        if self.board.field.coords[self.pawn[0]][self.pawn[1]].color == Color.black:
            img_start = 'images/b'

        self.choose_queen_button = Button(img_start + 'Q.png',  self._choose_queen, (110, 220), (80, 80), self)
        self.choose_rook_button = Button(img_start + 'R.png', self._choose_rook, (210, 220), (80, 80), self)
        self.choose_bishop_button = Button(img_start + 'B.png', self._choose_bishop, (310, 220), (80, 80), self)
        self.choose_knight_button = Button(img_start + 'N.png', self._choose_knight, (410, 220), (80, 80), self)
        self.choose_queen_button.show()
        self.choose_rook_button.show()
        self.choose_bishop_button.show()
        self.choose_knight_button.show()

    def _choose_queen(self):
        self.board.field.coords[self.pawn[0]][self.pawn[1]] = Queen(self.board.field.coords[self.pawn[0]][self.pawn[1]].color, self.board.field)
        self.close_buttons()

    def _choose_rook(self):
        self.board.field.coords[self.pawn[0]][self.pawn[1]] = Rook(self.board.field.coords[self.pawn[0]][self.pawn[1]].color, self.board.field)
        self.close_buttons()

    def _choose_bishop(self):
        self.board.field.coords[self.pawn[0]][self.pawn[1]] = Bishop(self.board.field.coords[self.pawn[0]][self.pawn[1]].color, self.board.field)
        self.close_buttons()

    def _choose_knight(self):
        self.board.field.coords[self.pawn[0]][self.pawn[1]] = Knight(self.board.field.coords[self.pawn[0]][self.pawn[1]].color, self.board.field)
        self.close_buttons()

    def close_buttons(self):
        self.choose_bishop_button.close()
        self.choose_knight_button.close()
        self.choose_queen_button.close()
        self.choose_rook_button.close()
        self.pawn = None
        self.pawn_can_transform = False
        self.repaint()
        if not self.board.vs_player:
            self.board.computer.move()
            self.repaint()

    def mousePressEvent(self, e):
        if not self.menu.is_active and not self.game_over:
            if e.buttons() == Qt.LeftButton and QCursor.pos().x() - 200 < 560:
                square = int((QCursor.pos().x() - 200) / self.board.side_of_square), \
                           int((QCursor.pos().y() - 75) / self.board.side_of_square)
                if not self.board.button_pressed:
                    if self.board.field.coords[square[1]][square[0]] is not None and self.board.field.coords[square[1]][square[0]].color == self.board.info.color:
                        self.board.button_pressed = True
                        self.board.pressed_piece = square[1], square[0]
                        self.board.painted_squares = right_moves(square[1], square[0], self.board.field)
                        self.board.painted_squares.append((square[1], square[0]))
                else:
                    doing_move((self.board.pressed_piece[0], self.board.pressed_piece[1]),
                               (square[1], square[0]),
                               self.board.field, self.board.info)
                    self.board.button_pressed = False
                    self.board.painted_squares = []
                    self.board.pressed_piece = None
                    pawn = pawn_can_transform(self.board.field)
                    if pawn is not None:
                        self.pawn = pawn
                        self.__transform_pawn__()
                self.repaint()

            if not self.board.vs_player and self.board.computer.color == self.board.info.color:
                self.board.computer.move()
                self.repaint()

            if is_pat_now(self.board.field, Color.black) or is_pat_now(self.board.field, Color.white):
                self.is_pat = True
                self.game_over = True
                self.ok_button.show()

            if checkmate(Color.black, self.board.field):
                self.is_white_won = True
                self.ok_button.show()
                self.game_over = True

            if checkmate(Color.white, self.board.field):
                self.is_black_won = True
                self.ok_button.show()
                self.game_over = True
            self.repaint()


def main():
    app = QApplication(sys.argv)
    py_chess = PyChess()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()