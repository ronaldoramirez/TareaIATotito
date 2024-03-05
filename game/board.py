class Board:
    def __init__(self):
        self.reset_board()
        self.current_turn = 'X'

    def reset_board(self):
        """ Reinicia el tablero a su estado inicial vacío. """
        self.board = [['' for _ in range(3)] for _ in range(3)]

    def make_move(self, row, col):
        """ Realiza un movimiento en el tablero, si es válido. """
        if self.is_valid_move(row, col):
            self.board[row][col] = self.current_turn
            self.current_turn = 'O' if self.current_turn == 'X' else 'X'
            return True
        return False

    def is_valid_move(self, row, col):
        """ Verifica si un movimiento es válido (la celda está vacía). """
        return self.board[row][col] == ''

    def check_winner(self):
        """ Verifica si hay un ganador en el tablero. """
        # Verificar filas, columnas y diagonales
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != '':
                return self.board[i][0]
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != '':
                return self.board[0][i]

        if self.board[0][0] == self.board[1][1] == self.board[2][2] != '':
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != '':
            return self.board[0][2]

        return None

    def is_board_full(self):
        """ Verifica si el tablero está completamente lleno. """
        return all(all(cell != '' for cell in row) for row in self.board)
