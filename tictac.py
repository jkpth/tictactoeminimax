import time
import math
from typing import List, Tuple, Optional

class FourInARow:
    def __init__(self):
        self.board = [[' ' for _ in range(6)] for _ in range(5)]
        self.current_player = 'X'

    def make_move(self, row: int, col: int) -> bool:
        if self.board[row][col] == ' ':
            self.board[row][col] = self.current_player
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            return True
        return False

    def is_valid_move(self, row: int, col: int) -> bool:
        if 0 <= row < 5 and 0 <= col < 6:
            return self.board[row][col] == ' ' and self.has_neighbor(row, col)
        return False

    def has_neighbor(self, row: int, col: int) -> bool:
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = row + dr, col + dc
                if 0 <= nr < 5 and 0 <= nc < 6 and self.board[nr][nc] != ' ':
                    return True
        return False

    def get_valid_moves(self) -> List[Tuple[int, int]]:
        moves = []
        for row in range(5):
            for col in range(6):
                if self.is_valid_move(row, col):
                    moves.append((row, col))
        return sorted(moves, key=lambda x: (x[1], x[0]))

    def check_win(self, player: str) -> bool:
        # Check horizontal, vertical, and diagonal wins
        for row in range(5):
            for col in range(6):
                if self.board[row][col] == player:
                    if self.check_direction(row, col, 0, 1, player) or \
                       self.check_direction(row, col, 1, 0, player) or \
                       self.check_direction(row, col, 1, 1, player) or \
                       self.check_direction(row, col, 1, -1, player):
                        return True
        return False

    def check_direction(self, row: int, col: int, dr: int, dc: int, player: str) -> bool:
        for i in range(4):
            r, c = row + i*dr, col + i*dc
            if r < 0 or r >= 5 or c < 0 or c >= 6 or self.board[r][c] != player:
                return False
        return True

    def is_full(self) -> bool:
        return all(self.board[row][col] != ' ' for row in range(5) for col in range(6))

    def evaluate(self, player: str) -> int:
        if self.check_win(player):
            return 1000
        if self.check_win('O' if player == 'X' else 'X'):
            return -1000
        if self.is_full():
            return 0

        me = player
        opponent = 'O' if me == 'X' else 'X'

        two_side_open_3_me = self.count_open_n_in_a_row(me, 3, 2)
        two_side_open_3_opp = self.count_open_n_in_a_row(opponent, 3, 2)
        one_side_open_3_me = self.count_open_n_in_a_row(me, 3, 1)
        one_side_open_3_opp = self.count_open_n_in_a_row(opponent, 3, 1)
        two_side_open_2_me = self.count_open_n_in_a_row(me, 2, 2)
        two_side_open_2_opp = self.count_open_n_in_a_row(opponent, 2, 2)
        one_side_open_2_me = self.count_open_n_in_a_row(me, 2, 1)

        score = 200 * two_side_open_3_me - 80 * two_side_open_3_opp + \
                150 * one_side_open_3_me - 40 * one_side_open_3_opp + \
                20 * two_side_open_2_me - 15 * two_side_open_2_opp + \
                5 * one_side_open_2_me

        return score

    def count_open_n_in_a_row(self, player: str, n: int, open_sides: int) -> int:
        count = 0
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        for row in range(5):
            for col in range(6):
                if self.board[row][col] == player:
                    for dr, dc in directions:
                        if self.check_open_n_in_a_row(row, col, dr, dc, player, n, open_sides):
                            count += 1
        
        return count

    def check_open_n_in_a_row(self, row: int, col: int, dr: int, dc: int, player: str, n: int, open_sides: int) -> bool:
        # Check if there's enough space in this direction
        if not (0 <= row + (n-1)*dr < 5 and 0 <= col + (n-1)*dc < 6):
            return False

        # Check for n in a row
        for i in range(n):
            if self.board[row + i*dr][col + i*dc] != player:
                return False

        # Check for open sides
        open_count = 0
        if 0 <= row - dr < 5 and 0 <= col - dc < 6 and self.board[row - dr][col - dc] == ' ':
            open_count += 1
        if 0 <= row + n*dr < 5 and 0 <= col + n*dc < 6 and self.board[row + n*dr][col + n*dc] == ' ':
            open_count += 1

        return open_count >= open_sides

    def print_board(self):
        for row in self.board:
            print('|' + '|'.join(row) + '|')
        print('-' * 13)
        print(' 0 1 2 3 4 5')

# The rest of the code (minimax and play_game functions) remains the same

def minimax(game: FourInARow, depth: int, alpha: float, beta: float, maximizing_player: bool, player: str) -> Tuple[int, Optional[Tuple[int, int]], int]:
    nodes_generated = 1
    
    if depth == 0 or game.check_win('X') or game.check_win('O') or game.is_full():
        return game.evaluate(player), None, nodes_generated

    valid_moves = game.get_valid_moves()
    
    if maximizing_player:
        max_eval = -math.inf
        best_move = None
        for move in valid_moves:
            game.make_move(move[0], move[1])
            eval, _, child_nodes = minimax(game, depth - 1, alpha, beta, False, player)
            game.board[move[0]][move[1]] = ' '
            game.current_player = 'X' if game.current_player == 'O' else 'O'
            nodes_generated += child_nodes
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move, nodes_generated
    else:
        min_eval = math.inf
        best_move = None
        for move in valid_moves:
            game.make_move(move[0], move[1])
            eval, _, child_nodes = minimax(game, depth - 1, alpha, beta, True, player)
            game.board[move[0]][move[1]] = ' '
            game.current_player = 'X' if game.current_player == 'O' else 'O'
            nodes_generated += child_nodes
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move, nodes_generated

def play_game():
    game = FourInARow()
    
    # Player 1 (X) makes the first move
    game.make_move(3, 4)
    print("Player 1 (X) makes the first move at [3, 4]")
    game.print_board()
    
    # Player 2 (O) makes the second move
    game.make_move(3, 3)
    print("Player 2 (O) makes the second move at [3, 3]")
    game.print_board()
    
    while True:
        current_player = 'X' if game.current_player == 'X' else 'O'
        depth = 2 if current_player == 'X' else 4
        
        start_time = time.time()
        _, move, nodes = minimax(game, depth, -math.inf, math.inf, True, current_player)
        end_time = time.time()
        
        if move:
            game.make_move(move[0], move[1])
            print(f"Player {1 if current_player == 'X' else 2} ({current_player}) makes a move at [{move[0]}, {move[1]}]")
            print(f"Nodes generated: {nodes}")
            print(f"CPU execution time: {end_time - start_time:.4f} seconds")
            game.print_board()
            
            if game.check_win(current_player):
                print(f"Player {1 if current_player == 'X' else 2} ({current_player}) wins!")
                break
            elif game.is_full():
                print("It's a tie!")
                break
        else:
            print("No valid moves left. It's a tie!")
            break

if __name__ == "__main__":
    play_game()