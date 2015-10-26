from PyQt5.QtGui import QImage, QColor, QPainter, QBrush
from PyQt5.QtWidgets import QWidget
from stupidAI import StupidAI
from mechanic import *


class Board(QWidget):
    height = 8
    width = 8
    side_of_square = 70

    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.field = Field(self.height, self.width)
        self.arrange_pieces(self.field, Color.white)
        self.button_pressed = False
        self.painted_squares = []
        self.pressed_piece = None
        self.vs_player = False
        #self.game_is_active = True
        self.info = GameInformation()
        self.setGeometry(0, 0, 560, 560)
        self.show()

    def create_computer(self, color):
        self.computer = StupidAI(color, self.field, self.info)
        if self.computer.color == self.info.color:
            self.computer.move()

    def arrange_pieces(self, field, down_color):
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

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.draw_squares(qp)
        self.draw_pieces(qp)
        if self.parent.pawn_can_transform:
            qp.drawImage(100, 160, QImage('images/choose_piece.png'))
        elif self.parent.is_pat:
            qp.drawImage(100, 150, QImage('images/pat.png'))
        elif self.parent.is_white_won:
            qp.drawImage(100, 150, QImage('images/white_win.png'))
        elif self.parent.is_black_won:
            qp.drawImage(100, 150, QImage('images/black_win.png'))
        qp.end()

    def draw_squares(self, qp):
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    qp.setBrush(QColor(210, 183, 115))
                else:
                    qp.setBrush(QColor(128, 84, 47))
                qp.drawRect(j * self.side_of_square, i * self.side_of_square, self.side_of_square, self.side_of_square)
        if self.button_pressed:
            qp.setBrush(QColor(0, 20, 70, 150))
            for square in self.painted_squares:
                qp.drawRect(square[1] * self.side_of_square, square[0] * self.side_of_square, self.side_of_square, self.side_of_square)

    def draw_pieces(self, qp):
        for i in range(8):
            for j in range(8):
                if self.field.coords[i][j] is not None:
                    if self.field.coords[i][j].color == Color.white:
                        image = QImage(self.field.coords[i][j].whiteColorImage)
                    else:
                        image = QImage(self.field.coords[i][j].blackColorImage)
                    qp.drawImage(j * self.side_of_square - 5, i * self.side_of_square - 5, image)