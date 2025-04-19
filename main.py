import pygame
import sys
import numpy as np
import math
import random
import time

# Game Settings
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)
WIDTH = COLUMN_COUNT * SQUARESIZE
HEIGHT = (ROW_COUNT + 1) * SQUARESIZE
SIZE = (WIDTH, HEIGHT)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
FPS = 1

# Create board
def create_board():
    return np.zeros((ROW_COUNT, COLUMN_COUNT))

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def winning_move(board, piece):
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if all(board[r][c+i] == piece for i in range(4)):
                return True
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if all(board[r+i][c] == piece for i in range(4)):
                return True
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if all(board[r+i][c+i] == piece for i in range(4)):
                return True
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if all(board[r-i][c+i] == piece for i in range(4)):
                return True
    return False

def draw_board(board, screen):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, (r+1)*SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int((r+1)*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), HEIGHT - int((r)*SQUARESIZE + SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), HEIGHT - int((r)*SQUARESIZE + SQUARESIZE/2)), RADIUS)
    pygame.display.update()

# AI Functions
def get_valid_locations(board):
    return [col for col in range(COLUMN_COUNT) if is_valid_location(board, col)]

def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = winning_move(board, 1) or winning_move(board, 2) or len(valid_locations) == 0
    if depth == 0 or is_terminal:
        if winning_move(board, 1):
            return (None, 100000000)
        elif winning_move(board, 2):
            return (None, -100000000)
        else:
            return (None, 0)
    if maximizingPlayer:
        value = -math.inf
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, 1)
            new_score = minimax(temp_board, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best_col, value
    else:
        value = math.inf
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, 2)
            new_score = minimax(temp_board, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return best_col, value

def mcts_move(board, simulations=100):
    valid_moves = get_valid_locations(board)
    move_scores = {move: 0 for move in valid_moves}
    for move in valid_moves:
        for _ in range(simulations):
            temp_board = board.copy()
            row = get_next_open_row(temp_board, move)
            drop_piece(temp_board, row, move, 2)
            move_scores[move] += simulate_game(temp_board, 2)
    best_move = max(move_scores, key=move_scores.get)
    return best_move

def simulate_game(board, starting_piece):
    current_piece = 3 - starting_piece
    while True:
        valid = get_valid_locations(board)
        if not valid:
            return 0
        move = random.choice(valid)
        row = get_next_open_row(board, move)
        drop_piece(board, row, move, current_piece)
        if winning_move(board, current_piece):
            return 1 if current_piece == starting_piece else -1
        current_piece = 3 - current_piece

# Main game loop
def main():
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Connect 4: Minimax (Red) vs MCTS (Yellow)")
    font = pygame.font.SysFont("monospace", 40)
    board = create_board()
    draw_board(board, screen)
    game_over = False
    turn = 0

    minimax_total_time = 0
    mcts_total_time = 0
    minimax_moves = 0
    mcts_moves = 0

    while not game_over:
        pygame.time.wait(1000)
        start = time.time()

        if turn == 0:
            col, _ = minimax(board, 3, -math.inf, math.inf, True)
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 1)
                end = time.time()
                move_time = end - start
                minimax_total_time += move_time
                minimax_moves += 1
                print(f"[Minimax] Move {minimax_moves} took {move_time:.2f} seconds")
                if winning_move(board, 1):
                    draw_board(board, screen)
                    label = font.render("Minimax Wins!", 1, RED)
                    screen.blit(label, (40, 10))
                    pygame.display.update()
                    print("Minimax Wins!")
                    game_over = True
        else:
            col = mcts_move(board, simulations=50)
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 2)
                end = time.time()
                move_time = end - start
                mcts_total_time += move_time
                mcts_moves += 1
                print(f"[MCTS] Move {mcts_moves} took {move_time:.2f} seconds")
                if winning_move(board, 2):
                    draw_board(board, screen)
                    label = font.render("MCTS Wins!", 1, YELLOW)
                    screen.blit(label, (40, 10))
                    pygame.display.update()
                    print("MCTS Wins!")
                    game_over = True

        draw_board(board, screen)
        turn += 1
        turn %= 2

    print("\n--- Game Summary ---")
    print(f"Minimax: {minimax_moves} moves, Total Time = {minimax_total_time:.2f} sec, Avg = {minimax_total_time/minimax_moves:.2f} sec/move")
    print(f"MCTS: {mcts_moves} moves, Total Time = {mcts_total_time:.2f} sec, Avg = {mcts_total_time/mcts_moves:.2f} sec/move")

    if minimax_total_time < mcts_total_time:
        print("🏆 Minimax is faster overall!")
    else:
        print("🏆 MCTS is faster overall!")

    pygame.time.wait(5000)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
