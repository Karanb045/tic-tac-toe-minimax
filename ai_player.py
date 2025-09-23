import random
from game import TicTacToeGame

class AIPlayer:
    def __init__(self, difficulty="hard"):
        self.difficulty = difficulty  # "easy" = random, "hard" = smarter(min- max algo)

    def get_move(self, board, player):
        if self.difficulty == "easy":
            return self._random_move(board)
        _, move = self._minimax(board.copy(), player, True, player, depth=0)
        return move if move is not None else -1

    def _random_move(self, board):
        available = [i for i, cell in enumerate(board) if cell == ' ']
        return random.choice(available) if available else -1

    def _minimax(self, board, current_player, is_maximizing, ai_player, depth):
        game = TicTacToeGame()
        game.board = board.copy()

        winner = game.check_winner()
        if winner == ai_player:
            return 10 - depth, None   # AI wins
        elif winner is not None:
            return depth - 10, None   # Opponent wins
        elif game.is_board_full():
            return 0, None            # Draw

        available_moves = [i for i, cell in enumerate(board) if cell == ' ']
        opponent = 'X' if current_player == 'O' else 'O'

        if is_maximizing:
            best_score = float('-inf')
            best_moves = []
            for mv in available_moves:
                board[mv] = current_player
                score, _ = self._minimax(board, opponent, False, ai_player, depth + 1)
                board[mv] = ' '
                if score > best_score:
                    best_score = score
                    best_moves = [mv]
                elif score == best_score:
                    best_moves.append(mv)
            return best_score, random.choice(best_moves)
        else:
            best_score = float('inf')
            best_moves = []
            for mv in available_moves:
                board[mv] = current_player
                score, _ = self._minimax(board, opponent, True, ai_player, depth + 1)
                board[mv] = ' '
                if score < best_score:
                    best_score = score
                    best_moves = [mv]
                elif score == best_score:
                    best_moves.append(mv)
            return best_score, random.choice(best_moves)
