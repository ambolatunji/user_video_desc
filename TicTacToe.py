import random
import json
import os

class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'
        self.ai_player = 'O'
        self.difficulty = 'medium'
        self.q_table = self.load_q_table()
        self.alpha = 0.1  # Learning rate
        self.gamma = 0.9  # Discount factor
        self.previous_state = None
        self.previous_action = None

    def load_q_table(self):
        if os.path.exists('q_table.json'):
            with open('q_table.json', 'r') as f:
                return json.load(f)
        return {}

    def save_q_table(self):
        with open('q_table.json', 'w') as f:
            json.dump(self.q_table, f)

    def make_move(self, position):
        if position is None or position < 0 or position >= 9:
            return False
        if self.board[position] == ' ':
            self.board[position] = self.current_player
            return True
        return False

    def check_winner(self):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]  # Diagonals
        ]
        for combo in winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != ' ':
                return self.board[combo[0]], combo
        if ' ' not in self.board:
            return 'Tie', None
        return None, None

    def switch_player(self):
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def get_empty_cells(self):
        return [i for i, cell in enumerate(self.board) if cell == ' ']
    
    def get_board_state(self):
        return ''.join(self.board)

    def get_q_value(self, state, action):
        return self.q_table.get((state, action), 0)

    def update_q_value(self, state, action, reward, next_state):
        max_next_q = max([self.get_q_value(next_state, a) for a in self.get_empty_cells()], default=0)
        current_q = self.get_q_value(state, action)
        new_q = current_q + self.alpha * (reward + self.gamma * max_next_q - current_q)
        self.q_table[(state, action)] = new_q

    def minimax(self, depth, is_maximizing):
        result = self.check_winner()
        if result == self.ai_player:
            return 1
        elif result == 'X':
            return -1
        elif result == 'Tie':
            return 0

        if is_maximizing:
            best_score = float('-inf')
            for move in self.get_empty_cells():
                self.board[move] = self.ai_player
                score = self.minimax(depth + 1, False)
                self.board[move] = ' '
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for move in self.get_empty_cells():
                self.board[move] = 'X'
                score = self.minimax(depth + 1, True)
                self.board[move] = ' '
                best_score = min(score, best_score)
            return best_score
    
    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
    def ai_move(self):
        state = self.get_board_state()
        available_moves = self.get_empty_cells()

        if not available_moves:
            return None

        if self.difficulty == 'easy':
            if random.random() < 0.3:
                return random.choice(available_moves)
        elif self.difficulty == 'medium':
            if random.random() < 0.7:
                return random.choice(available_moves)
        if self.difficulty == 'normal':
            best_move = None
            best_score = float('-inf')
            for move in available_moves:
                self.board[move] = self.ai_player
                score = self.minimax(0, False)
                self.board[move] = ' '
                if score > best_score:
                    best_score = score
                    best_move = move
        elif self.difficulty == 'superhard':
            best_move = self.minimax_ai(self.board, self.ai_player)
        else:
            q_values = [(move, self.get_q_value(state, move)) for move in available_moves]
            best_move = max(q_values, key=lambda x: x[1])[0]

        self.previous_state = state
        self.previous_action = best_move
        return best_move

    def minimax_ai(self, board, whoami):
        best_move = None
        best_score = None
        if self.is_board_empty(board):
            return random.choice(self.get_empty_cells())
        for move in self.get_empty_cells():
            new_board = board[:]
            new_board[move] = whoami
            opponent = 'X' if whoami == 'O' else 'O'
            score = self.minimax_score(new_board, opponent, whoami)
            if best_score is None or score > best_score:
                best_move = move
                best_score = score
        return best_move

    def minimax_score(self, board, curr, ai):
        winner = self.check_winner()[0]
        if winner == ai:
            return 10
        elif winner and winner != ai:
            return -10
        elif ' ' not in board:
            return 0
        scores = []
        for move in self.get_empty_cells():
            new_board = board[:]
            new_board[move] = curr
            opponent = 'X' if curr == 'O' else 'O'
            score = self.minimax_score(new_board, opponent, ai)
            scores.append(score)
        return max(scores) if curr == ai else min(scores)

    def is_board_empty(self, board):
        return all(cell == ' ' for cell in board)

    def update_learning(self, reward):
        if self.previous_state and self.previous_action is not None:
            current_state = self.get_board_state()
            self.update_q_value(self.previous_state, self.previous_action, reward, current_state)
            self.save_q_table()

    def reset_game(self):
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'
        self.previous_state = None
        self.previous_action = None

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty