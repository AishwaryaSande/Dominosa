#  Dominosa Game

A Python implementation of the **Dominosa puzzle game** with an interactive GUI and optimized algorithms.  
This project demonstrates the use of **Dynamic Programming, Divide & Conquer, Graph Traversal, and Backtracking** to solve and play the Dominosa puzzle efficiently.

---

#  About the Game

Dominosa is a logic puzzle based on domino tiles.

Given an **N × N grid of numbers**, the objective is to:

• Pair adjacent cells (horizontally or vertically)  
• Each pair forms a domino tile  
• Each domino pair can only appear **once**  

The goal is to cover the entire board using **valid domino pairs without repetition**.

Example Domino Pairs (for numbers 0–2):

```
(0,0)
(0,1)
(0,2)
(1,1)
(1,2)
(2,2)
```

---

#  Project Objectives

This project demonstrates several **algorithm design techniques**:

- Dynamic Programming (Memoization)
- Divide and Conquer
- Graph Algorithms
- Backtracking
- Game AI strategy

---

#  Features

✔ Random Dominosa board generation  
✔ Valid move detection  
✔ Computer opponent  
✔ Move scoring system  
✔ Efficient algorithm optimization using caching  
✔ Graph-based board component detection  
✔ Merge Sort for move ranking  
✔ Backtracking solver for puzzle validation  
✔ GUI interface for gameplay

---

#  Algorithms Used

## 1️ Dynamic Programming (Memoization)

To avoid recomputing valid moves repeatedly, previously calculated board states are stored in a cache.

```
MOVE_CACHE = {}
```

This stores:

```
(board_state) → valid_moves
```

This significantly reduces computation time.

---

## 2 Divide and Conquer (Merge Sort)

Merge Sort is used to rank moves by their score.

Steps:

1. Divide moves list into halves
2. Recursively sort each half
3. Merge them in sorted order

Time Complexity:

```
O(n log n)
```

---

## 3️ Graph Traversal (DFS)

The board is treated as a graph where each cell is a node.

DFS is used to:

• Divide the board into connected components  
• Identify playable regions  

---

## 4️ Backtracking

Backtracking is used to:

• Verify board solvability  
• Explore all possible domino placements  

It recursively tries all valid placements until a valid solution is found.

---

# Project Structure

```
Dominosa/
│
├── main.py              # Program entry point
├── game_logic.py        # Core game algorithms
├── graph_logic.py       # Graph traversal functions
├── models.py            # Data structures (Cell class)
├── renderer.py          # Game rendering and display
├── gui.py               # GUI interface
├── constants.py         # Global constants
│
└── README.md            # Project documentation
```

---

#  Requirements

Make sure you have:

```
Python 3.10+
```

Install dependencies (if required):

```
pip install -r requirements.txt
```

---

#  How to Run the Project

Step 1 — Clone the repository

```
git clone https://github.com/YOUR_USERNAME/Dominosa.git
```

Step 2 — Navigate to the folder

```
cd Dominosa
```

Step 3 — Run the game

```
python main.py
```

---

#  How to Play

1. The board displays numbers.
2. Select two adjacent cells.
3. If the pair is valid and unused, a domino is placed.
4. The game continues until no valid moves remain.

---

#  Complexity Analysis

| Operation | Complexity |
|----------|------------|
Move generation | O(n²) |
Merge sort | O(n log n) |
DFS components | O(V + E) |
Backtracking solver | Exponential |
DP cache lookup | O(1) |

---

#  Key Concepts Demonstrated

This project applies important Computer Science concepts:

• Dynamic Programming  
• Memoization  
• Optimal Substructure  
• Graph Theory  
• Depth First Search  
• Divide and Conquer  
• Backtracking Algorithms  

---

#  Example Game Board

```
1 2 3
0 1 2
3 0 1
```

Valid domino placements must match unique pairs.

---

#  Future Improvements

Possible enhancements:

• Multiplayer mode  
• Online leaderboard  
• Difficulty levels  
• Hint system  
• Improved AI strategy  

---

#  Author

**Aishwarya Sande**

B.Tech Computer Science Student  

---

#  License

This project is open source and available under the MIT License.
