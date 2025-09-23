class TicTacToeGame:
    def __init__(self):
        self.board = [' '] * 9  # 3x3 board as a flat list
        self.winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]              # Diagonals
        ]

    def is_valid_move(self, position):
        return 0 <= position < 9 and self.board[position] == ' '

    def make_move(self, position, player):
        if self.is_valid_move(position):
            self.board[position] = player
            return True
        return False

    def check_winner(self):
        for combo in self.winning_combinations:
            if (
                self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]]
                and self.board[combo[0]] != ' '
            ):
                return self.board[combo[0]]  # "X" or "O"
        return None

    def is_board_full(self):
        return ' ' not in self.board

    def copy_board(self):
        new_game = TicTacToeGame()
        new_game.board = self.board.copy()
        return new_game

    def get_available_moves(self):
        return [i for i, cell in enumerate(self.board) if cell == ' ']
