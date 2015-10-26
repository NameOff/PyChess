from PyQt5.QtWidgets import QWidget, QPushButton
from PyQt5.QtGui import QImage, QIcon, QPainter
from gameinfo import Color
from guiField import Board


class Menu(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.is_active = False
        self.setGeometry(0, 0, 860, 560)
        self.initialize_buttons()
        self.start()

    def initialize_buttons(self):
        self.new_game_button = Button('images/new_Game.png', self.__startNewGame__, (280, 160), (300, 55), self)
        self.multiplayer_button = Button('images/multiplayer.png', self.__multiplayer__, (280, 240), (300, 55), self)
        self.quit_button = Button('images/quit.png', self.__quitGame__, (280, 320), (300, 55), self)
        self.one_player_button = Button('images/one_player.png', self.__onePlayer__, (280, 160), (300, 55), self)
        self.two_players_button = Button('images/two_players.png', self.__twoPlayers__, (280, 240), (300, 55), self)
        self.back_button = Button('images/back.png', self.__back__, (280, 320), (300, 55), self)
        self.white_button = Button('images/white.png', self.__whiteColor__, (280, 160), (300, 55), self)
        self.black_button = Button('images/black.png', self.__blackColor__, (280, 240), (300, 55), self)
        self.continue_button = Button('images/continue.png', self._continue, (280, 80), (300, 55), self)

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        qp.drawImage(0, 0, QImage('images/background.jpg'))
        qp.end()

    def _continue(self):
        self.is_active = False
        self.continue_button.close()
        self.new_game_button.close()
        self.multiplayer_button.close()
        self.quit_button.close()
        self.parent.back_to_menu_button.show()
        self.close()

    def __whiteColor__(self):
        self._start_new_game(1, Color.white)
        self.parent.game_over = False
        self.parent.board.info.downColor = Color.white
        self.parent.board.arrange_pieces(self.parent.board.field, Color.white)
        self.parent.board.create_computer(Color.black)
        self.close()
        self.is_active = False
        self.parent.back_to_menu_button.show()

    def __blackColor__(self):
        self._start_new_game(1, Color.black)
        self.parent.game_over = False
        self.parent.board.info.downColor = Color.black
        self.parent.board.arrange_pieces(self.parent.board.field, Color.black)
        self.parent.board.create_computer(Color.white)
        self.close()
        self.is_active = False
        self.parent.back_to_menu_button.show()

    def __multiplayer__(self): #TODO
        pass

    def __quitGame__(self):
        quit()

    def __startNewGame__(self):
        self.new_game_button.close()
        self.multiplayer_button.close()
        self.quit_button.close()
        self.two_players_button.show()
        self.back_button.show()
        self.one_player_button.show()

    def __back__(self):
        if self.one_player_button.isVisible():
            self.one_player_button.close()
            self.two_players_button.close()
            self.back_button.close()
            self.new_game_button.show()
            self.multiplayer_button.show()
            self.quit_button.show()
        else:
            self.white_button.close()
            self.black_button.close()
            self.one_player_button.show()
            self.two_players_button.show()

    def __onePlayer__(self):
        self.one_player_button.close()
        self.two_players_button.close()
        self.white_button.show()
        self.black_button.show()

    def __twoPlayers__(self): #TODO
        self.close()
        self._start_new_game(2)
        self.parent.board.info.downColor = Color.white
        self.is_active = False
        self.parent.game_over = False
        self.parent.board.vs_player = True
        self.parent.back_to_menu_button.show()

    def start(self):
        self.is_active = True
        self.one_player_button.close()
        self.two_players_button.close()
        self.back_button.close()
        self.white_button.close()
        self.black_button.close()
        self.new_game_button.show()
        self.continue_button.close()
        self.multiplayer_button.show()
        self.quit_button.show()
        if not self.parent.game_over:
            self.continue_button.show()
        self.show()

    def _start_new_game(self, count_of_players, down_color=None):
        for i in range(self.parent.board.height):
            for j in range(self.parent.board.width):
                self.parent.board.field.coords[i][j] = None
        self.parent.set_initial_init()
        if count_of_players == 2:
            self.parent.board.vs_player = True
            self.parent.board.arrange_pieces(self.parent.board.field, Color.white)
        else:
            self.parent.board.vs_player = False
            self.parent.board.arrange_pieces(self.parent.board.field, down_color)
        self.parent.board.info.color = Color.white


class Button(QPushButton):
    def __init__(self, image_path, function, coordinates, size, parent=None):
        super(QPushButton, self).__init__(parent)
        self.function = function
        self.setGeometry(coordinates[0], coordinates[1], size[0], size[1])
        self.setStyleSheet('''background-image: url("%s");
                              background-repeat:no-repeat;''' % image_path)
        self.clicked.connect(self._on_click)

    def _on_click(self):
        self.function()