# Team-Matrix
Ai term project(Connect 4 AI: Minimax with Alpha-Beta Pruning)
# 🤖 Connect 4 AI Evaluation: Minimax vs Monte Carlo Tree Search (MCTS)

This project implements and compares two powerful AI strategies for the classic game of **Connect 4**:
> 🔗 deployment link: https://team-matrixgit-connect4ai.streamlit.app/

- **Minimax with Alpha-Beta Pruning**
- **Monte Carlo Tree Search (MCTS)**

A modern **Streamlit-based web interface** allows users to simulate multiple games between the two algorithms, tweak AI parameters (depth, simulations), and analyze performance using metrics like win rate, decision time, and strategy accuracy.

## 🧩 Project Overview

- **Language:** Python 3.8+
- **Interface:** Streamlit
- **Core Features:**
  - AI vs AI simulations (Minimax vs MCTS)
  - Adjustable depth/simulation settings
  - Win rate and performance charting
  - Interactive UI for gameplay and evaluation
- **Use Case:** AI algorithm benchmarking in turn-based games


## 📚 Theory: Minimax vs MCTS

### 🔁 Minimax (with Alpha-Beta Pruning)
A tree-search algorithm that explores all possible move sequences to a fixed depth. Alpha-Beta pruning cuts off unnecessary branches, making it efficient. It is **deterministic** and **depth-limited**.

### 🌲 Monte Carlo Tree Search (MCTS)
A **probabilistic** strategy that runs many simulated random games to estimate the value of each move. It balances exploration and exploitation using the UCT (Upper Confidence Bound) formula. It's more adaptable than Minimax and doesn't need a depth limit.

## 🖥️ Streamlit App Demo

> 🔧 Launch Instructions:
```bash
streamlit run main_connect4_FINAL.py
```

> 🧪 Requirements:
```bash
pip install -r requirements.txt
```

If `requirements.txt` is missing, install manually:
```bash
pip install streamlit numpy matplotlib
```

## 🕹️ How to Use the App

1. **Sidebar Controls:**
   - 🎮 Select number of games to simulate
   - 🧠 Set Minimax search depth (e.g., 3–5)
   - 🎲 Set MCTS simulations per move (e.g., 100–1000)

2. **Start Simulation:**
   - Click the **Run Simulation** button
   - Results update in real-time

3. **Results Displayed:**
   - 📊 Win rate chart (Minimax vs MCTS)
   - ⏱️ Average move decision time
   - ✅ (Optional) Move optimality or accuracy comparison


## 📈 Example Use Cases

- Benchmarking turn-based game strategies
- AI coursework demonstrations
- Exploring tradeoffs between deterministic vs probabilistic planning

## 📌 Future Improvements

- Add real-time gameplay (vs human)
- Store results over time for long-term evaluation
  

> 📅 **Last Updated**: May 2025  
> 🔗 youtube link: https://youtu.be/Ht9s9lWt2e8?si=LEBv5gshdLUq5KUC

