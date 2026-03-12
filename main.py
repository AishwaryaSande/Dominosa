"""Main GUI application for Dominosa game with Pause Functionality"""
import tkinter as tk
from tkinter import ttk, messagebox

# Assuming these are your local imports
from constants import NEON, DEFAULT_GRID_SIZE, DEFAULT_TIME_LIMIT, DEFAULT_HINTS
from models import Cell
from game_logic import GameLogic
from renderer import Renderer

class DominosaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Dominosa - Neon Graph Suite")
        self.root.geometry("1150x750")
        self.root.configure(bg=NEON["bg"])
        
        self.GRID = DEFAULT_GRID_SIZE
        self.time_left = DEFAULT_TIME_LIMIT
        self.current_turn = "User"
        self.user_score = 0
        self.comp_score = 0
        self.game_active = True
        self.is_paused = False  # Track pause state
        self.timer_id = None
        self.show_edges = True

        # Hint system
        self.user_hints_left = DEFAULT_HINTS
        self.comp_hints_left = DEFAULT_HINTS
        self.hinted_move = None

        self._setup_ui()
        self.init_game()
        
        # Bind events
        self.canvas.bind("<Button-1>", self.handle_click)
        self.canvas.bind("<Configure>", lambda e: self.draw_board())

    def _setup_ui(self):
        """Setup all UI components"""
        self.canvas = tk.Canvas(self.root, bg=NEON["bg"], highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        self.sidebar = tk.Frame(self.root, bg=NEON["panel_bg"], width=650)
        self.sidebar.pack(side="right", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(self.sidebar, text="Dominosa", fg=NEON["accent"], bg=NEON["panel_bg"], 
                font=("Segoe UI Semibold", 22)).pack(anchor="w", padx=20, pady=(20, 0))
        
        self.stats_frame = tk.Frame(self.sidebar, bg=NEON["panel_bg"])
        self.stats_frame.pack(fill="x", padx=20, pady=10)
        self.score_lbl = tk.Label(self.stats_frame, text="User: 0 | CPU: 0", fg=NEON["accent2"], 
                                 bg=NEON["panel_bg"], font=("Consolas", 12))
        self.score_lbl.pack(side="left")
        self.timer_lbl = tk.Label(self.stats_frame, text="Time: 30s", fg=NEON["accent"], 
                                 bg=NEON["panel_bg"], font=("Consolas", 12, "bold"))
        self.timer_lbl.pack(side="right")

        self.hints_frame = tk.Frame(self.sidebar, bg=NEON["panel_bg"])
        self.hints_frame.pack(fill="x", padx=20, pady=5)
        self.hints_lbl = tk.Label(self.hints_frame, text="Hints → User: 2/2 | CPU: 2/2", 
                                 fg=NEON["accent2"], bg=NEON["panel_bg"], font=("Consolas", 10))
        self.hints_lbl.pack(side="left")

        tk.Label(self.sidebar, text="Difficulty Level:", fg=NEON["text"], bg=NEON["panel_bg"], 
                font=("Consolas", 10)).pack(anchor="w", padx=20, pady=(5, 0))
        self.case_var = tk.StringVar(value="Random (Easy 4x4)")
        self.case_menu = ttk.Combobox(self.sidebar, textvariable=self.case_var, state="readonly", 
                                     values=["Random (Easy 4x4)", "Random (Medium 6x6)", 
                                           "Dead End Case (Impossible)"])
        self.case_menu.pack(fill="x", padx=20, pady=5)
        self.case_menu.bind("<<ComboboxSelected>>", lambda e: self.init_game())

        btn_frame = tk.Frame(self.sidebar, bg=NEON["panel_bg"])
        btn_frame.pack(fill="x", padx=20, pady=5)
        b_config = {"bg": NEON["btn_bg"], "fg": NEON["text"], "relief": "flat", 
                   "font": ("Consolas", 9, "bold")}
        
        tk.Button(btn_frame, text="🔄 New", command=self.init_game, **b_config).grid(row=0, column=0, sticky="ew", padx=1)
        tk.Button(btn_frame, text="↺ Restart", command=self.restart_game, **b_config).grid(row=0, column=1, sticky="ew", padx=1)
        
        # New Pause Button
        self.pause_btn = tk.Button(btn_frame, text="⏸ Pause", command=self.toggle_pause, **b_config)
        self.pause_btn.grid(row=0, column=2, sticky="ew", padx=1)
        
        tk.Button(btn_frame, text="💡 Hint", command=self.use_hint, **b_config).grid(row=0, column=3, sticky="ew", padx=1)
        tk.Button(btn_frame, text="🤖 Solve", command=self.solve_logic, **b_config).grid(row=0, column=4, sticky="ew", padx=1)
        btn_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        self.tabs = ttk.Notebook(self.sidebar)
        self.tabs.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.terminal = tk.Text(self.tabs, bg=NEON["terminal_bg"], fg=NEON["terminal_fg"], 
                               font=("Consolas", 10), borderwidth=0, padx=10, pady=10)
        self.tabs.add(self.terminal, text="📝 Terminal")
        
        graph_frame = tk.Frame(self.tabs, bg=NEON["terminal_bg"])
        self.tabs.add(graph_frame, text="📊 Graph View")
        
        toggle_frame = tk.Frame(graph_frame, bg=NEON["terminal_bg"])
        toggle_frame.pack(fill="x", padx=10, pady=5)
        self.edge_toggle_btn = tk.Button(toggle_frame, text="🔗 Hide Edges", command=self.toggle_edges,
                                         bg=NEON["btn_bg"], fg=NEON["text"], relief="flat", 
                                         font=("Consolas", 9, "bold"))
        self.edge_toggle_btn.pack(side="left")
        
        self.graph_canvas = tk.Canvas(graph_frame, bg=NEON["terminal_bg"], highlightthickness=0)
        self.graph_canvas.pack(fill="both", expand=True)
        self.graph_canvas.bind("<Configure>", lambda e: self.draw_graph())

    def toggle_pause(self):
        if not self.game_active:
            return
            
        self.is_paused = not self.is_paused
        
        if self.is_paused:
            self.pause_btn.config(text="▶ Resume", fg=NEON["accent"])
            self.log("|| Game Paused")
            # Hide the game board components for fairness
            self.canvas.itemconfigure("all", state="hidden")
            # Draw a temporary "Paused" message
            self.canvas.create_text(
                self.canvas.winfo_width()/2, self.canvas.winfo_height()/2,
                text="PAUSED", fill=NEON["accent"], font=("Consolas", 40, "bold"), tags="pause_msg"
            )
        else:
            self.pause_btn.config(text="⏸ Pause", fg=NEON["text"])
            self.log(">> Game Resumed")
            self.canvas.delete("pause_msg")
            self.canvas.itemconfigure("all", state="normal")
            # If timer loop was somehow broken, restart it
            if not self.timer_id:
                self.update_timer()

    def log(self, msg):
        self.terminal.insert("end", f"{msg}\n")
        self.terminal.see("end")

    def init_game(self):
        case = self.case_var.get()
        self.GRID = 6 if "6x6" in case else 4
        self.is_paused = False
        self.pause_btn.config(text="⏸ Pause", fg=NEON["text"])

        if "Dead End" in case:
            self.current_vals = [[0, 0, 0, 0], [1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3]]
        else:
            self.current_vals = GameLogic.generate_valid_board(self.GRID)

        self.cells = [[Cell(r, c, self.current_vals[r][c]) for c in range(self.GRID)] 
                     for r in range(self.GRID)]
        self.dominoes = []
        self.used_pairs = set()
        self.selected = []
        self.user_score = 0
        self.comp_score = 0
        self.game_active = True
        self.current_turn = "User"
        
        self.user_hints_left = DEFAULT_HINTS
        self.comp_hints_left = DEFAULT_HINTS
        self.hinted_move = None
        
        max_val = self.GRID - 1
        self.all_pairs = [(i, j) for i in range(max_val + 1) for j in range(i, max_val + 1)]
        self.pair_status = {pair: "unclaimed" for pair in self.all_pairs}
        
        self.terminal.delete(1.0, tk.END)
        self.log(f">> Mode: {case}")
        self.log(">> Board Ready. User Turn.")
        
        self.reset_and_start_timer()
        self.draw_board()
        self.draw_graph()
        self.update_hints_display()

    def restart_game(self):
        saved_vals = [row[:] for row in self.current_vals]
        self.cells = [[Cell(r, c, saved_vals[r][c]) for c in range(self.GRID)] 
                     for r in range(self.GRID)]
        self.dominoes = []
        self.used_pairs = set()
        self.selected = []
        self.user_score = 0
        self.comp_score = 0
        self.game_active = True
        self.is_paused = False
        self.pause_btn.config(text="⏸ Pause", fg=NEON["text"])
        self.current_turn = "User"
        self.hinted_move = None
        self.user_hints_left = DEFAULT_HINTS
        self.comp_hints_left = DEFAULT_HINTS
        
        self.log(">> Game Restarted with same board.")
        self.reset_and_start_timer()
        self.draw_board()
        self.draw_graph()
        self.update_hints_display()

    def reset_and_start_timer(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        self.time_left = DEFAULT_TIME_LIMIT
        self.update_timer()

    def update_timer(self):
        if not self.game_active:
            return

        # Handle Pause State
        if self.is_paused:
            self.timer_id = self.root.after(1000, self.update_timer)
            return

        if self.time_left <= 0:
            self.timer_lbl.config(text="Time: 0s", fg=NEON["timer_warn"])
            self.log(f"! {self.current_turn} timed out.")
            self.timer_id = None
            self.switch_turn()
            return

        self.timer_lbl.config(text=f"Time: {self.time_left}s",
                              fg=NEON["timer_warn"] if self.time_left <= 10 else NEON["accent"])
        self.time_left -= 1
        self.timer_id = self.root.after(1000, self.update_timer)

    def update_hints_display(self):
        self.hints_lbl.config(text=f"Hints → User: {self.user_hints_left}/2 | CPU: {self.comp_hints_left}/2")

    def draw_board(self):
        if self.is_paused: return # Don't redraw/show board if paused
        result = Renderer.draw_board(self.canvas, self.cells, self.dominoes, self.selected, self.GRID)
        if result:
            self._s, self._ox, self._oy = result

    def draw_graph(self):
        Renderer.draw_graph(self.graph_canvas, self.all_pairs, self.used_pairs, 
                          self.dominoes, self.show_edges)

    def handle_click(self, event):
        if not self.game_active or self.is_paused or self.current_turn != "User": 
            return
        try:
            c, r = (event.x - self._ox)//self._s, (event.y - self._oy)//self._s
            if 0 <= r < self.GRID and 0 <= c < self.GRID:
                cell = self.cells[r][c]
                if cell.used: return
                if cell in self.selected: self.selected.remove(cell)
                else: self.selected.append(cell)
                
                if len(self.selected) == 2:
                    a, b = self.selected
                    self.selected = []
                    if abs(a.r-b.r) + abs(a.c-b.c) == 1:
                        pair = tuple(sorted((a.v, b.v)))
                        if pair not in self.used_pairs:
                            is_hinted = self.hinted_move in [(a, b), (b, a)]
                            self.place_domino(a, b, "User", is_hinted)
                            self.hinted_move = None
                            self.switch_turn()
                        else:
                            self.log(f"! Pair {pair} already used.")
                    else:
                        self.log("! Selection must be adjacent.")
            self.draw_board()
        except (AttributeError, ZeroDivisionError): pass

    def place_domino(self, a, b, owner, is_hinted=False):
        a.used = b.used = True
        self.used_pairs.add(tuple(sorted((a.v, b.v))))
        self.dominoes.append({'cells': (a, b), 'owner': owner})
        points = (a.v + b.v) + (0 if is_hinted else 5)
        
        if owner == "User": self.user_score += points
        else: self.comp_score += points
        
        self.score_lbl.config(text=f"User: {self.user_score} | CPU: {self.comp_score}")
        self.log(f">> {owner} linked {a.v}:{b.v} (+{points})")
        
        if all(cell.used for row in self.cells for cell in row): 
            self.end_game("BOARD CLEARED")

    def switch_turn(self):
        if not self.game_active: return
        
        if not GameLogic.has_valid_moves(self.cells, self.GRID, self.used_pairs):
            self.end_game("NO VALID MOVES LEFT")
            return

        self.current_turn = "Comp" if self.current_turn == "User" else "User"
        self.reset_and_start_timer()
        
        if self.current_turn == "Comp": 
            self.root.after(1000, self.computer_move)

    def use_hint(self):
        if not self.game_active or self.is_paused: return
        
        if self.current_turn == "User":
            if self.user_hints_left <= 0:
                messagebox.showwarning("No Hints", "You've used all your hints!")
                return
            self.user_hints_left -= 1
        else:
            if self.comp_hints_left <= 0: return
            self.comp_hints_left -= 1
        
        moves = GameLogic.find_all_valid_moves(self.cells, self.GRID, self.used_pairs)
        if moves:
            _, a, b = moves[0]
            self.log(f"💡 Hint: Link {a.v} & {b.v} at ({a.r},{a.c})")
            if self.current_turn == "User": self.hinted_move = (a, b)
        
        self.update_hints_display()

    def solve_logic(self):
        if not self.game_active or self.is_paused: return
        self.log("🤖 AI Solver: Finding path...")
        curr_used = {(c.r, c.c) for row in self.cells for c in row if c.used}
        grid_vals = [[c.v for c in row] for row in self.cells]
        
        sol = GameLogic.backtrack(0, self.GRID, grid_vals, curr_used, self.used_pairs.copy())
        if sol:
            for (r1, c1), (r2, c2) in sol:
                self.place_domino(self.cells[r1][c1], self.cells[r2][c2], "Comp")
            self.draw_board()
            self.draw_graph()
        else:
            messagebox.showwarning("No Solution", "No valid path exists.")

    def end_game(self, reason):
        self.game_active = False
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        winner = "USER WINS!" if self.user_score > self.comp_score else "CPU WINS!" if self.comp_score > self.user_score else "DRAW!"
        self.log(f"GAME OVER: {reason}\nRESULT: {winner}")
        messagebox.showinfo("Match Result", f"{winner}\n\nUser: {self.user_score}\nCPU: {self.comp_score}")

    def computer_move(self):
        if self.current_turn != "Comp" or not self.game_active: return
        
        # If the computer's turn comes up while paused, delay it
        if self.is_paused:
            self.root.after(1000, self.computer_move)
            return

        move = GameLogic.computer_move(self.cells, self.GRID, self.used_pairs)
        if move:
            self.place_domino(move[0], move[1], "Comp")
            self.draw_board()
        self.switch_turn()

    def toggle_edges(self):
        self.show_edges = not self.show_edges
        self.edge_toggle_btn.config(text="🔗 Hide Edges" if self.show_edges else "🔗 Show Edges")
        self.draw_graph()

if __name__ == "__main__":
    root = tk.Tk()
    app = DominosaGUI(root)
    root.mainloop()