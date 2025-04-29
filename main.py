import pygame
import sys
import numpy as np
import math
import random
import time

# Game Settings
ROW_COUNT = 6  # Number of rows in the Connect 4 board
COLUMN_COUNT = 7  # Number of columns in the Connect 4 board
SQUARESIZE = 100  # Size of each square in pixels
RADIUS = int(SQUARESIZE / 2 - 5)  # Radius of the game piece circles
WIDTH = COLUMN_COUNT * SQUARESIZE  # Total width of the game window
HEIGHT = (ROW_COUNT + 1) * SQUARESIZE  # Total height of the game window (extra row for top)
SIZE = (WIDTH, HEIGHT)  # Window size tuple
BLUE = (0, 0, 255)  # Color for the board background
BLACK = (0, 0, 0)  # Color for empty slots
RED = (255, 0, 0)  # Color for player 1 (Minimax) pieces
YELLOW = (255, 255, 0)  # Color for player 2 (MCTS) pieces
FPS = 1  # Frames per second (not directly used in this code)

# Create an empty game board using NumPy
def create_board():
    return np.zeros((ROW_COUNT, COLUMN_COUNT))  # Returns a 6x7 matrix of zeros

# Place a piece on the board
def drop_piece(board, row, col, piece):
    board[row][col] = piece  # Sets the board position to the player's piece (1 or 2)

# Check if a column is valid for placing a piece
def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0  # True if the top row of the column is empty

# Find the next available row in a column
def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:  # Returns the lowest empty row in the column
            return r

# Check for a winning move (four pieces in a row)
def winning_move(board, piece):
    # Check horizontal wins
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if all(board[r][c+i] == piece for i in range(4)):
                return True
    # Check vertical wins
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if all(board[r+i][c] == piece for i in range(4)):
                return True
    # Check positive diagonal wins
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if all(board[r+i][c+i] == piece for i in range(4)):
                return True
    # Check negative diagonal wins
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if all(board[r-i][c+i] == piece for i in range(4)):
                return True
    return False  # No winning move found

# Draw the game board and pieces
def draw_board(board, screen):
    # Draw the blue board with black circles for empty slots
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, (r+1)*SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int((r+1)*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    # Draw player pieces (red for Minimax, yellow for MCTS)
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), HEIGHT - int((r)*SQUARESIZE + SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), HEIGHT - int((r)*SQUARESIZE + SQUARESIZE/2)), RADIUS)
    pygame.display.update()  # Refresh the display

# AI Functions
# Get a list of valid columns for moves
def get_valid_locations(board):
    return [col for col in range(COLUMN_COUNT) if is_valid_location(board, col)]

# Minimax algorithm with alpha-beta pruning
def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    # Check for terminal states (win, loss, or draw)
    is_terminal = winning_move(board, 1) or winning_move(board, 2) or len(valid_locations) == 0
    if depth == 0 or is_terminal:
        if winning_move(board, 1):
            return (None, 100000000)  # High score for Minimax win
        elif winning_move(board, 2):
            return (None, -100000000)  # Low score for MCTS win
        else:
            return (None, 0)  # Neutral score for draw or depth limit
    if maximizingPlayer:  # Minimax's turn (player 1)
        value = -math.inf
        best_col = random.choice(valid_locations)  # Default to a random valid move
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()  # Create a copy of the board
            drop_piece(temp_board, row, col, 1)  # Simulate move
            new_score = minimax(temp_board, depth-1, alpha, beta, False)[1]  # Recursive call
            if new_score > value:
                value = new_score
                best_col = col  # Update best column
            alpha = max(alpha, value)  # Update alpha
            if alpha >= beta:
                break  # Prune branch
        return best_col, value
    else:  # MCTS's turn (player 2)
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
            beta = min(beta, value)  # Update beta
            if alpha >= beta:
                break  # Prune branch
        return best_col, value

# Monte Carlo Tree Search (MCTS) move selection
def mcts_move(board, simulations=100):
    valid_moves = get_valid_locations(board)
    move_scores = {move: 0 for move in valid_moves}  # Track scores for each move
    for move in valid_moves:
        for _ in range(simulations):
            temp_board = board.copy()
            row = get_next_open_row(temp_board, move)
            drop_piece(temp_board, row, move, 2)  # Simulate MCTS move
            move_scores[move] += simulate_game(temp_board, 2)  # Add simulation result
    best_move = max(move_scores, key=move_scores.get)  # Choose move with highest score
    return best_move

# Simulate a random game from the current board state
def simulate_game(board, starting_piece):
    current_piece = 3 - starting_piece  # Alternate player (1 or 2)
    while True:
        valid = get_valid_locations(board)
        if not valid:
            return 0  # Draw
        move = random.choice(valid)  # Random valid move
        row = get_next_open_row(board, move)
        drop_piece(board, row, move, current_piece)
        if winning_move(board, current_piece):
            return 1 if current_piece == starting_piece else -1  # Win or loss
        current_piece = 3 - current_piece  # Switch player

# Main game loop
def main():
    pygame.init()  # Initialize Pygame
    screen = pygame.display.set_mode(SIZE)  # Create game window
    pygame.display.set_caption("Connect 4: Minimax (Red) vs MCTS (Yellow)")  # Set window title
    font = pygame.font.SysFont("monospace", 40)  # Font for win messages
    board = create_board()  # Initialize empty board
    draw_board(board, screen)  # Draw initial board
    game_over = False
    turn = 0  # 0 for Minimax, 1 for MCTS

    # Track time and move counts for performance analysis
    minimax_total_time = 0
    mcts_total_time = 0
    minimax_moves = 0
    mcts_moves = 0

    while not game_over:
        pygame.time.wait(1000)  # Pause for 1 second between moves
        start = time.time()  # Record move start time

        if turn == 0:  # Minimax's turn (Red)
            col, _ = minimax(board, 3, -math.inf, math.inf, True)  # Get best move (depth=3)
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 1)  # Place Minimax piece
                end = time.time()
                move_time = end - start
                minimax_total_time += move_time
                minimax_moves += 1
                print(f"[Minimax] Move {minimax_moves} took {move_time:.2f} seconds")
                if winning_move(board, 1):
                    draw_board(board, screen)
                    label = font.render("Minimax Wins!", 1, RED)
                    screen.blit(label, (40, 10))  # Display win message
                    pygame.display.update()
                    print("Minimax Wins!")
                    game_over = True
        else:  # MCTS's turn (Yellow)
            col = mcts_move(board, simulations=50)  # Get best move (50 simulations)
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 2)  # Place MCTS piece
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

        draw_board(board, screen)  # Update board display
        turn += 1
        turn %= 2  # Alternate turns

    # Print game summary with performance metrics
    print("\n--- Game Summary ---")
    print(f"Minimax: {minimax_moves} moves, Total Time = {minimax_total_time:.2f} sec, Avg = {minimax_total_time/minimax_moves:.2f} sec/move")
    print(f"MCTS: {mcts_moves} moves, Total Time = {mcts_total_time:.2f} sec, Avg = {mcts_total_time/mcts_moves:.2f} sec/move")

    # Compare total times to determine faster algorithm
    if minimax_total_time < mcts_total_time:
        print("🏆 Minimax is faster overall!")
    else:
        print("🏆 MCTS is faster overall!")

    pygame.time.wait(5000)  # Wait 5 seconds before closing
    pygame.quit()  # Close Pygame
    sys.exit()  # Exit program

if __name__ == "__main__":
    main()  # Run the game