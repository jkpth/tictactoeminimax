import time
import math
from typing import List, Tuple, Optional

EMPTY = ' '
X = 'X'  # Player 1
O = 'O'  # Player 2 (opponent)

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

    def get_diagonals_topleft_bottomright(self):
        rows = 5
        cols = 6
        diagonals = []

        # Get diagonals starting from the first row
        for col_start in range(cols):
            diagonal = []
            row, col = 0, col_start
            while row < rows and col < cols:
                diagonal.append(self.board[row][col])
                row += 1
                col += 1
            diagonals.append(diagonal)

        # Get diagonals starting from the first column (excluding the [0,0] diagonal)
        for row_start in range(1, rows):
            diagonal = []
            row, col = row_start, 0
            while row < rows and col < cols:
                diagonal.append(self.board[row][col])
                row += 1
                col += 1
            diagonals.append(diagonal)

        return diagonals

    def get_diagonals_topright_bottomleft(self):
        rows = 5
        cols = 6
        diagonals = []

        # Get diagonals starting from the first row (moving left from the top right)
        for col_start in range(cols):
            diagonal = []
            row, col = 0, col_start
            while row < rows and col >= 0:
                diagonal.append(self.board[row][col])
                row += 1
                col -= 1
            diagonals.append(diagonal)

        # Get diagonals starting from the last column (excluding the [0,cols-1] diagonal)
        for row_start in range(1, rows):
            diagonal = []
            row, col = row_start, cols - 1
            while row < rows and col >= 0:
                diagonal.append(self.board[row][col])
                row += 1
                col -= 1
            diagonals.append(diagonal)

        return diagonals

    def evaluate(self, player, verbose=False):
        opponent = 'X' if player == 'O' else 'O'
        
        two_side_open_3_me = one_side_open_3_me = 0
        two_side_open_3_opponent = one_side_open_3_opponent = 0
        two_side_open_2_me = one_side_open_2_me = 0
        two_side_open_2_opponent = one_side_open_2_opponent = 0


        h_seqs = []
        for row in range(5):
            h_seq = self.board[row][:6]
            h_seqs.append(h_seq)
        
        v_seqs = []
        for col in range(6): 
            v_seq = [self.board[row][col] for row in range(5)]
            v_seqs.append(v_seq)

        diaglr = self.get_diagonals_topleft_bottomright()

        diagrl = self.get_diagonals_topright_bottomleft()

        all_seqs = h_seqs + v_seqs + diaglr + diagrl

        for seq in all_seqs:
            # Check for three in a row
            if self.check_open_3(seq, player):
                two_side_open_3_me += 1
                if verbose:
                    print(player, "two-side-open-3-in-a-row-me count:", two_side_open_3_me)
            elif self.check_open_3(seq, opponent):
                two_side_open_3_opponent += 1
                if verbose:
                    print(player, "two-side-open-3-in-a-row-opp count:", two_side_open_3_opponent)

            # Check for one-sided three in a row
            elif self.check_one_side_open_3(seq, player):
                one_side_open_3_me += 1
                if verbose:
                    print(player, "one-side-open-3-in-a-row-me count:", one_side_open_3_me)
            elif self.check_one_side_open_3(seq, opponent):
                one_side_open_3_opponent += 1
                if verbose:
                    print(player, "one-side-open-3-in-a-row-opp count:", one_side_open_3_opponent)

            # Check for two in a row
            elif self.check_open_2(seq, player):
                two_side_open_2_me += 1
                if verbose:
                    print(player, "two-side-open-2-in-a-row-me count:", two_side_open_2_me)
            elif self.check_open_2(seq, opponent):
                two_side_open_2_opponent += 1
                if verbose:
                    print(player, "two-side-open-2-in-a-row-opp count:", two_side_open_2_opponent)

            # Check for one-sided two in a row
            elif self.check_one_side_open_2(seq, player):
                one_side_open_2_me += 1
                if verbose:
                    print(player, "one-side-open-2-in-a-row-me count:", one_side_open_2_me)
            elif self.check_one_side_open_2(seq, opponent):
                one_side_open_2_opponent += 1
                if verbose:
                    print(player, "one-side-open-2-in-a-row-opp count:", one_side_open_2_opponent)
    
        heuristic_score = (200 * two_side_open_3_me
                         - 80  * two_side_open_3_opponent
                         + 150 * one_side_open_3_me
                         - 40  * one_side_open_3_opponent
                         + 20  * two_side_open_2_me
                         - 15  * two_side_open_2_opponent
                         + 5   * one_side_open_2_me
                         - 2   * one_side_open_2_opponent)
        
        if verbose:
            print(heuristic_score)

        return heuristic_score

    def check_open_3(self, seq, player):
        return [' ', player, player, player, ' '] in [seq[i:i + 5] for i in range(len(seq) - 4)]

    def check_one_side_open_3(self, seq, player):
        return ([player, player, player, ' '] in [seq[i:i + 4] for i in range(len(seq) - 3)] or
                [' ', player, player, player] in [seq[i:i + 4] for i in range(len(seq) - 3)])

    def check_open_2(self, seq, player):
        return [' ', player, player, ' '] in [seq[i:i + 4] for i in range(len(seq) - 3)]

    def check_one_side_open_2(self, seq, player):
        return ([player, player, ' '] in [seq[i:i + 3] for i in range(len(seq) - 2)] or
                [' ', player, player] in [seq[i:i + 3] for i in range(len(seq) - 2)])




    def print_board(self):
        for row in self.board:
            print('|' + '|'.join(row) + '|')
        print('-' * 13)
        print(' 0 1 2 3 4 5')

# main minimax function
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
            if eval == max_eval:
                if move[1] < best_move[1]:
                    max_eval = eval
                    best_move = move
                elif move[1] == best_move[1] and move[0] < best_move[0]:
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
            if eval == min_eval:
                if move[1] < best_move[1]:
                    min_eval = eval
                    best_move = move
                elif move[1] == best_move[1] and move[0] < best_move[0]:
                    min_eval = eval
                    best_move = move
                    
            beta = min(beta, eval)
            if beta <= alpha:
                break

        return min_eval, best_move, nodes_generated

def play_game():
    game = FourInARow()
    
    # Player 1 (X) makes the first move
    game.make_move(2, 3)
    print("Player 1 (X) makes the first move at [3, 4]")
    game.print_board()
    
    # Player 2 (O) makes the second move
    game.make_move(2, 2)
    print("Player 2 (O) makes the second move at [3, 3]")
    game.print_board()
    
    while True:
        current_player = 'X' if game.current_player == 'X' else 'O'
        depth = 2 if current_player == 'X' else 4
        #depth = 2 if current_player == 'O' else 4
        
        
        start_time = time.time()
        _, move, nodes = minimax(game, depth, -math.inf, math.inf, True, current_player)
        # print(f"Evaluation score for {current_player}: {_}, Best move: {move}")
        # print(_, move)
        end_time = time.time()
        
        if move:
            game.make_move(move[0], move[1])

            game.evaluate(current_player)
            print(f"Player {1 if current_player == 'X' else 2} ({current_player}) makes a move at [{move[0]+1}, {move[1]+1}]")
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

def test():
    game = FourInARow()
    game.make_move(4,2)
    game.make_move(3,1)
    game.make_move(3,2)
    game.make_move(2,2)
    game.make_move(3,3)
    game.make_move(1,2)
    game.make_move(2,4)
    game.make_move(3,4)
    game.make_move(1,3)
    game.make_move(2,3)
    game.print_board()
    print(game.evaluate('X'))


if __name__ == "__main__":
    #test()
    play_game()