import tkinter as tk
from tkinter import messagebox
import threading
import time
from game import TicTacToeGame
from ai_player import AIPlayer

class TicTacToeGUI:
    def __init__(self, root):
        # Main window setup
        self.root = root
        self.root.title("Tic-Tac-Toe vs AI")
        self.root.geometry("500x650")
        self.root.resizable(False, False)

        # App color theme
        self.colors = {
            'bg': '#1e1e2e',
            'surface': '#2a2a40',
            'player': '#00d4ff',
            'ai': '#ff4d6d',
            'draw': '#ffd700',
            'text': '#f5f5f5'
        }
        self.root.configure(bg=self.colors['bg'])

        # Game statistics
        self.stats = {"player_wins": 0, "ai_wins": 0, "draws": 0}
        self.create_menu()

    # Menu Screen
    def create_menu(self):
        # Main menu with difficulty options
        self.clear_window()
        frame = tk.Frame(self.root, bg=self.colors['bg'])
        frame.pack(expand=True)

        tk.Label(frame, text="TIC-TAC-TOE", font=("Helvetica", 24, "bold"),
                 bg=self.colors['bg'], fg=self.colors['text']).pack(pady=20)
        tk.Label(frame, text="Select Difficulty", font=("Helvetica", 16),
                 bg=self.colors['bg'], fg=self.colors['text']).pack(pady=10)

        tk.Button(frame, text="Easy", font=("Helvetica", 14), width=15,
                  bg=self.colors['player'], fg=self.colors['text'],
                  activebackground='#6fcfff', command=lambda: self.start_game("easy")).pack(pady=10)
        tk.Button(frame, text="Hard", font=("Helvetica", 14), width=15,
                  bg=self.colors['ai'], fg=self.colors['text'],
                  activebackground='#ff7b7b', command=lambda: self.start_game("hard")).pack(pady=10)

    # Start Game
    def start_game(self, difficulty):
        # Reset game state and start a new round
        self.difficulty = difficulty
        self.ai = AIPlayer(difficulty)
        self.game = TicTacToeGame()
        self.current_player = "X"
        self.game_over = False
        self.ai_thinking = False
        self.clear_window()
        self.create_title()
        self.create_board()
        self.create_status()
        self.update_board()
        self.update_stats_display()

    # Title
    def create_title(self):
        # Top title section with difficulty display
        title_frame = tk.Frame(self.root, bg=self.colors['bg'])
        title_frame.pack(pady=10)
        tk.Label(title_frame, text="TIC-TAC-TOE", font=("Helvetica", 20, "bold"),
                 bg=self.colors['bg'], fg=self.colors['text']).pack()
        tk.Label(title_frame, text=f"Difficulty: {self.difficulty.title()}",
                 font=("Helvetica", 14), bg=self.colors['bg'], fg=self.colors['text']).pack()

    # Board
    def create_board(self):
        # Create the 3x3 grid of buttons
        self.board_frame = tk.Frame(self.root, bg=self.colors['surface'])
        self.board_frame.pack(pady=20)
        self.buttons = []
        for i in range(3):
            for j in range(3):
                btn = tk.Button(self.board_frame, text="", font=("Helvetica", 24, "bold"),
                                width=5, height=2, bg=self.colors['surface'], fg=self.colors['text'],
                                activebackground=self.colors['player'],
                                command=lambda idx=i*3+j: self.on_button_click(idx))
                btn.grid(row=i, column=j, padx=5, pady=5)
                self.buttons.append(btn)

        self.bottom_frame = tk.Frame(self.root, bg=self.colors['bg'])
        self.bottom_frame.pack(pady=10)
        tk.Button(self.bottom_frame, text="Play Again", font=("Helvetica", 12),
                  bg=self.colors['player'], fg=self.colors['text'],
                  activebackground='#6fcfff', command=lambda: self.start_game(self.difficulty)).pack(side='left', padx=10)
        tk.Button(self.bottom_frame, text="Main Menu", font=("Helvetica", 12),
                  bg=self.colors['ai'], fg=self.colors['text'],
                  activebackground='#ff7b7b', command=self.create_menu).pack(side='left', padx=10)

    # Status & Stats
    def create_status(self):
        self.status_label = tk.Label(self.root, text="Your turn!", font=("Helvetica", 14),
                                     bg=self.colors['bg'], fg=self.colors['text'])
        self.status_label.pack(pady=10)

        stats_frame = tk.Frame(self.root, bg=self.colors['bg'])
        stats_frame.pack(pady=10)
        self.player_label = tk.Label(stats_frame, text=f"You: {self.stats['player_wins']}",
                                     bg=self.colors['bg'], fg=self.colors['player'], font=("Helvetica", 12))
        self.player_label.pack(side="left", padx=10)
        self.ai_label = tk.Label(stats_frame, text=f"AI: {self.stats['ai_wins']}",
                                 bg=self.colors['bg'], fg=self.colors['ai'], font=("Helvetica", 12))
        self.ai_label.pack(side="left", padx=10)
        self.draw_label = tk.Label(stats_frame, text=f"Draws: {self.stats['draws']}",
                                   bg=self.colors['bg'], fg=self.colors['draw'], font=("Helvetica", 12))
        self.draw_label.pack(side="left", padx=10)

    # Gameplay
    def on_button_click(self, idx):
        if self.game_over or self.ai_thinking or not self.game.is_valid_move(idx):
            return
        self.make_move(idx, "X")
        if self.check_game_end():
            return
        self.current_player = "O"
        self.ai_thinking = True
        self.status_label.config(text="AI is thinking...")
        threading.Thread(target=self.ai_move, daemon=True).start()

    def ai_move(self):
        time.sleep(1)  # small delay for realism
        move = self.ai.get_move(self.game.board, "O")
        self.root.after(0, lambda: self.make_move(move, "O"))
        self.root.after(0, self.after_ai_move)

    def after_ai_move(self):
        self.ai_thinking = False
        if not self.check_game_end():
            self.current_player = "X"
            self.status_label.config(text="Your turn!")

    def make_move(self, idx, player):
        self.game.make_move(idx, player)
        self.update_board()

    def update_board(self):
        for i, val in enumerate(self.game.board):
            if val == "X":
                self.buttons[i].config(text="❌", state="disabled", fg=self.colors['player'], bg=self.colors['surface'])
            elif val == "O":
                self.buttons[i].config(text="⭕", state="disabled", fg=self.colors['ai'], bg=self.colors['surface'])
            else:
                self.buttons[i].config(text="", state="normal", bg=self.colors['surface'])

    # Game End
    def check_game_end(self):
        # Check for winner or draw
        winner = self.game.check_winner()
        if winner:
            self.game_over = True
            if winner == "X":
                self.stats['player_wins'] += 1
                self.status_label.config(text="🎉 You won!")
                messagebox.showinfo("Game Over", "🎉 You beat the AI! 🎉")
            else:
                self.stats['ai_wins'] += 1
                self.status_label.config(text="🤖 AI wins!")
                messagebox.showinfo("Game Over", "🤖 AI wins! Try again!")
            self.update_stats_display()
            return True
        elif self.game.is_board_full():
            self.game_over = True
            self.stats['draws'] += 1
            self.status_label.config(text="🤝 Draw!")
            messagebox.showinfo("Game Over", "🤝 It's a draw!")
            self.update_stats_display()
            return True
        return False

    def update_stats_display(self):
        # Refresh scoreboard labels
        self.player_label.config(text=f"🎉 You: {self.stats['player_wins']}")
        self.ai_label.config(text=f"🤖 AI: {self.stats['ai_wins']}")
        self.draw_label.config(text=f"🤝 Draws: {self.stats['draws']}")

    #Utility
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

def run_gui():
    root = tk.Tk()
    TicTacToeGUI(root)
    root.mainloop()

if __name__ == "__main__":
    run_gui()
