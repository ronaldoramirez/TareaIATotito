from PyQt5.QtWidgets import (QMainWindow, QPushButton,
                             QGridLayout, QWidget,
                             QMessageBox, QLabel)
from PyQt5.QtGui import QIcon, QPixmap
from game.board import Board

class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Totito IA")
        self.setWindowIcon(QIcon('assets/app_icon.png'))
        self.board = Board()
        self.init_ui()

    def init_ui(self):
        self.grid_layout = QGridLayout()
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(self.grid_layout)

        self.status_label = QLabel("Turno del Jugador 1")
        self.status_label.setPixmap(QPixmap('assets/player1_icon.png').scaled(50, 50))
        self.grid_layout.addWidget(self.status_label, 3, 0, 1, 3)  # Ajusta el span para centrar la etiqueta

        for row in range(3):
            for col in range(3):
                button = QPushButton('')
                button.setFixedSize(100, 100)
                button.clicked.connect(lambda checked, row=row, col=col: self.on_click(row, col))
                self.grid_layout.addWidget(button, row, col)

    def on_click(self, row, col):
        if self.board.make_move(row, col):
            sender = self.sender()  # Obtiene el botón que fue presionado
            sender.setText(self.board.current_turn)  # Establece el texto del botón al símbolo del jugador actual
            sender.setEnabled(False)  # Deshabilita el botón para evitar más clicks en él

            winner = self.board.check_winner()  # Verifica si hay un ganador
            if winner:
                self.end_game(winner)
            elif self.board.is_board_full():
                self.end_game("Empate")
            else:
                self.update_status("Turno del jugador: " + self.board.current_turn)

    def end_game(self, result):
        # Código para manejar el fin del juego. 'result' puede ser un jugador o "Empate"
        if result == "Empate":
            message = "¡Es un empate!"
        else:
            message = f"¡Jugador {result} gana!"

        # Muestra un mensaje y reinicia el juego o cierra la aplicación
        reply = QMessageBox.question(self, 'Juego terminado', message + " ¿Quieres jugar otra vez?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

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

    def update_status(self, message):
        # Actualiza el estado del juego, por ejemplo, mostrando el turno actual
        # Podrías usar una barra de estado o un etiqueta para mostrar el mensaje
        pass