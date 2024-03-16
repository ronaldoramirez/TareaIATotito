from PyQt5.QtWidgets import (QMainWindow, QPushButton,
                             QGridLayout, QWidget,
                             QMessageBox, QLabel)
from PyQt5.QtGui import QIcon, QPixmap, QFont
from game.config import (
    WINDOW_TITLE, APP_ICON_PATH, PLAYER1_ICON_PATH, PLAYER2_ICON_PATH,
    BUTTON_FONT_SIZE, LABEL_FONT_SIZE, MESSAGE_FONT_SIZE, ICON_SIZE,
    BUTTON_SIZE, STATUS_ICON_SIZE, TIE_MESSAGE ,WIN_MESSAGE_START,WIN_MESSAGE_END,
    WIN_MESSAGE, PLAYER_TURN_TEXT, BOARD_SIZE, PLAYER_X_SYMBOL, PLAYER_O_SYMBOL,
    TIED, END_MESSAGE
)
from game.board import Board

class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(WINDOW_TITLE)
        self.setWindowIcon(QIcon(APP_ICON_PATH))
        self.board = Board()
        self.player1_icon = QPixmap(PLAYER1_ICON_PATH).scaled(ICON_SIZE, ICON_SIZE)
        self.player2_icon = QPixmap(PLAYER2_ICON_PATH).scaled(ICON_SIZE, ICON_SIZE)
        self.init_ui()

    def init_ui(self):
        self.grid_layout = QGridLayout()
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(self.grid_layout)

        button_font = QFont()
        button_font.setPointSize(BUTTON_FONT_SIZE)
        label_font = QFont()
        label_font.setPointSize(LABEL_FONT_SIZE)

        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                button = QPushButton('')
                button.setFixedSize(BUTTON_SIZE, BUTTON_SIZE)
                button.setFont(button_font)
                button.clicked.connect(lambda checked, row=row, col=col: self.on_click(row, col))
                self.grid_layout.addWidget(button, row, col)

        self.status_label = QLabel()
        self.status_label.setFont(label_font)
        self.status_label.setPixmap(self.player1_icon.scaled(STATUS_ICON_SIZE, STATUS_ICON_SIZE))
        self.grid_layout.addWidget(self.status_label, 3, 0, 1, 3) # Ajusta el span para centrar la etiqueta

    def on_click(self, row, col):
        current_player = self.board.current_turn  # Guarda el turno actual antes de hacer el movimiento
        if self.board.make_move(row, col):
            sender = self.sender()  # Obtiene el botón que fue presionado
            sender.setText(current_player)  # Establece el texto del botón al símbolo del jugador que hizo el movimiento
            sender.setEnabled(False)  # Deshabilita el botón para evitar más clicks en él

            winner = self.board.check_winner()  # Verifica si hay un ganador
            if winner:
                self.board.switch_turn()  # Cambia el turno al siguiente jugador solamente si no hay ganador
                self.end_game(winner)
            elif self.board.is_board_full():
                self.end_game(TIED)
            else:
                self.update_status(f'{PLAYER_TURN_TEXT}{self.board.current_turn}')

    def end_game(self, result):
        # Código para manejar el fin del juego. 'result' puede ser un jugador o "Empate"
        if result == TIED:
            message = TIE_MESSAGE
        else:
            message = f'{WIN_MESSAGE_START} {result} {WIN_MESSAGE_END}'

        message += END_MESSAGE

        font = QFont()
        font.setPointSize(12)  # Ajusta el tamaño de la fuente según sea necesario
        msg_box = QMessageBox()
        msg_box.setFont(font)
        msg_box.setWindowIcon(QIcon(APP_ICON_PATH))
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Information)

        # Muestra un mensaje y reinicia el juego o cierra la aplicación
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)
        reply = msg_box.exec_()

        if reply == QMessageBox.Yes:
            self.reset_game()
        else:
            self.close()

    def reset_game(self):
        # Reinicia el juego limpiando el tablero y reiniciando el estado
        self.board.reset_board()
        for i in range(self.grid_layout.count()):
            button = self.grid_layout.itemAt(i).widget()
            if button:
                button.setText('')
                button.setEnabled(True)
        self.update_status(f'{PLAYER_TURN_TEXT} {self.board.current_turn}')

    def update_status(self, message):
        if self.board.current_turn == "1":
            self.status_label.setPixmap(self.player1_icon.scaled(50, 50))
        else:
            self.status_label.setPixmap(self.player2_icon.scaled(50, 50))
        self.status_label.setText(message)

