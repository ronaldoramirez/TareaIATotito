from PyQt5.QtWidgets import QApplication
from ui.game_window import GameWindow
import sys

def main():
    app = QApplication(sys.argv)
    window = GameWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()