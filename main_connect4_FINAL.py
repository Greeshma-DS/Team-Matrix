import streamlit as st
import numpy as np
import random
import math
import time
import matplotlib.pyplot as plt

# Game Settings
ROW_COUNT = 6
COLUMN_COUNT = 7

# Utility Functions
def create_board():
    return np.zeros((ROW_COUNT, COLUMN_COUNT))

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def get_valid_locations(board):
    return [col for col in range(COLUMN_COUNT) if is_valid_location(board, col)]

def winning_move(board, piece):
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if all(board[r][c+i] == piece for i in range(4)):
                return True
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if all(board[r+i][c] == piece for i in range(4)):
                return True
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if all(board[r+i][c+i] == piece for i in range(4)):
                return True
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if all(board[r-i][c+i] == piece for i in range(4)):
                return True
    return False

def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = winning_move(board, 1) or winning_move(board, 2) or len(valid_locations) == 0
    if depth == 0 or is_terminal:
        if winning_move(board, 1):
            return (None, 1000000)
        elif winning_move(board, 2):
            return (None, -1000000)
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

def mcts_move(board, simulations):
    valid_moves = get_valid_locations(board)
    move_scores = {move: 0 for move in valid_moves}
    for move in valid_moves:
        for _ in range(simulations):
            temp_board = board.copy()
            row = get_next_open_row(temp_board, move)
            drop_piece(temp_board, row, move, 2)
            move_scores[move] += simulate_game(temp_board, 2)
    return max(move_scores, key=move_scores.get)

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

def display_board(board):
    board_display = ""
    for r in reversed(range(ROW_COUNT)):
        for c in range(COLUMN_COUNT):
            if board[r][c] == 0:
                board_display += "⚪"
            elif board[r][c] == 1:
                board_display += "🔴"
            else:
                board_display += "🟡"
        board_display += "\n"
    return board_display

# Streamlit App
st.set_page_config(page_title="Connect 4 AI Evaluation", layout="centered")
st.title("🤖 Connect 4 AI Evaluation: Minimax vs MCTS")

with st.sidebar:
    st.header("⚙️ Configuration")
    num_games = st.slider("Number of Games to Simulate", 1, 50, 10)
    minimax_depth = st.slider("Minimax Depth", 2, 6, 3)
    mcts_simulations = st.slider("MCTS Simulations per Move", 50, 500, 100)

if st.button("🚀 Start Simulation"):
    st.write("Running games...please wait ⏳")
    progress_bar = st.progress(0)

    results = {"Minimax": 0, "MCTS": 0, "Draw": 0}
    total_minimax_time = 0
    total_mcts_time = 0
    total_minimax_moves = 0
    total_mcts_moves = 0

    for game in range(num_games):
        board = create_board()
        game_over = False
        turn = 0
        minimax_time = 0
        mcts_time = 0
        minimax_moves = 0
        mcts_moves = 0

        board_placeholder = st.empty()

        while not game_over:
            if turn == 0:
                start = time.time()
                col, _ = minimax(board, minimax_depth, -math.inf, math.inf, True)
                end = time.time()
                move_time = end - start
                minimax_time += move_time
                minimax_moves += 1
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)
                    if winning_move(board, 1):
                        results["Minimax"] += 1
                        game_over = True
            else:
                start = time.time()
                col = mcts_move(board, mcts_simulations)
                end = time.time()
                move_time = end - start
                mcts_time += move_time
                mcts_moves += 1
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)
                    if winning_move(board, 2):
                        results["MCTS"] += 1
                        game_over = True
            turn = (turn + 1) % 2

            # Update board view live
            board_placeholder.text(display_board(board))
            time.sleep(0.2)  # small pause to see moves

        if not game_over:
            results["Draw"] += 1

        total_minimax_time += minimax_time
        total_mcts_time += mcts_time
        total_minimax_moves += minimax_moves
        total_mcts_moves += mcts_moves

        # Update progress
        progress_bar.progress((game + 1) / num_games)

    st.subheader("📊 Results")
    st.write(f"**Minimax Wins:** {results['Minimax']} / {num_games}")
    st.write(f"**MCTS Wins:** {results['MCTS']} / {num_games}")
    st.write(f"**Draws:** {results['Draw']} / {num_games}")

    avg_minimax = total_minimax_time / total_minimax_moves if total_minimax_moves > 0 else 0
    avg_mcts = total_mcts_time / total_mcts_moves if total_mcts_moves > 0 else 0

    st.write(f"**Average Minimax Move Time:** {avg_minimax:.2f} sec")
    st.write(f"**Average MCTS Move Time:** {avg_mcts:.2f} sec")

    # Bar Chart
    fig, ax = plt.subplots()
    bars = ax.bar(["Minimax", "MCTS"], [results["Minimax"], results["MCTS"]], color=["red", "gold"])
    ax.set_ylabel("Games Won")
    ax.set_title("AI Performance Comparison")
    st.pyplot(fig)

    # Final Verdict
    st.subheader("🏆 Conclusion")
    if results["Minimax"] > results["MCTS"]:
        st.success("🔴 Minimax is winning more games!")
    elif results["MCTS"] > results["Minimax"]:
        st.success("🟡 MCTS is winning more games!")
    else:
        st.info("Both AIs are equally strong.")

    if avg_minimax < avg_mcts:
        st.success("Minimax is faster per move!")
    else:
        st.success("MCTS is faster per move!")

    # Final Verdict
    st.subheader("🏆 Conclusion")

    # Raw outcome messages
    if results["Minimax"] > results["MCTS"]:
        st.write("🔴 **Minimax** is winning more games!")
    elif results["MCTS"] > results["Minimax"]:
        st.write("🟡 **MCTS** is winning more games!")
    else:
        st.write("⚪ Both AIs are equally strong in win rate.")

    if avg_minimax < avg_mcts:
        st.write("⏱️ Minimax is faster per move.")
    else:
        st.write("⏱️ MCTS is faster per move.")

    # Overall final judgment
    st.markdown("---")
    st.subheader("💡 Final Decision")

    if results["Minimax"] > results["MCTS"] and avg_minimax < avg_mcts:
        st.success("🔴 **Minimax is the better AI overall** because it is both **faster** and **wins more** consistently. It’s efficient and strategically strong.")
    elif results["MCTS"] > results["Minimax"] and avg_mcts < avg_minimax:
        st.success("🟡 **MCTS is the better AI overall** because it achieves a **higher win rate** and also performs moves **faster** in this configuration.")
    elif results["Minimax"] > results["MCTS"]:
        st.success("🔴 **Minimax is the better AI overall** because it **wins more games**, even though MCTS may be slightly faster in some cases.")
    elif results["MCTS"] > results["Minimax"]:
        st.success("🟡 **MCTS is the better AI overall** because it **wins more games**, showing better long-term strategy, despite being slower.")
    else:
        st.info("🤝 It's a tie! Both AIs perform similarly. More tuning (depth/simulations) might reveal a better performer.")
