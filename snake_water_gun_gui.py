import tkinter as tk
from tkinter import font as tkfont
import random
import time


# ── Colour palette ──────────────────────────────────────────────────────────
BG        = "#0F0E17"
PANEL     = "#9A93C5"
CARD      = "#211F35"
BORDER    = "#2E2B50"
ACCENT    = "#7C6AF7"
ACCENT2   = "#A78BFA"
GREEN     = "#34D399"
RED       = "#F87171"
YELLOW    = "#FBBF24"
WHITE     = "#FFFFFE"
MUTED     = "#6B7280"
TEXT_DARK = "#0F0E17"

EMOJI = {"snake": "🐍", "water": "💧", "gun": "🔫"}
COLORS = {"snake": "#34D399", "water": "#60A5FA", "gun": "#F87171"}


# ── Game logic ───────────────────────────────────────────────────────────────
def get_computer_choice():
    """Returns a random choice for the computer."""
    return random.choice(["snake", "water", "gun"])


def check_winner(player: str, computer: str) -> str:
    """
    Determines the winner of a round using if-else statements.
    Rules:
        gun   beats snake
        water beats gun
        snake beats water
    Returns: 'player', 'computer', or 'draw'
    """
    if player == computer:
        return "draw"
    elif player == "gun"   and computer == "snake":
        return "player"
    elif player == "water" and computer == "gun":
        return "player"
    elif player == "snake" and computer == "water":
        return "player"
    else:
        return "computer"


# ── GUI Application ──────────────────────────────────────────────────────────
class SnakeWaterGunApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Snake · Water · Gun")
        self.configure(bg=BG)
        self.resizable(False, False)

        # Scores
        self.player_score    = 0
        self.computer_score  = 0
        self.draws           = 0
        self.rounds          = 0
        self.result_pending  = False

        self._build_fonts()
        self._build_ui()
        self._center_window()

    # ── Fonts ────────────────────────────────────────────────────────────────
    def _build_fonts(self):
        self.f_title   = tkfont.Font(family="Helvetica Neue", size=22, weight="bold")
        self.f_sub     = tkfont.Font(family="Helvetica Neue", size=11)
        self.f_emoji   = tkfont.Font(family="Segoe UI Emoji",  size=48)
        self.f_btn     = tkfont.Font(family="Helvetica Neue", size=14, weight="bold")
        self.f_score_n = tkfont.Font(family="Helvetica Neue", size=30, weight="bold")
        self.f_score_l = tkfont.Font(family="Helvetica Neue", size=10)
        self.f_result  = tkfont.Font(family="Helvetica Neue", size=16, weight="bold")
        self.f_vs      = tkfont.Font(family="Helvetica Neue", size=22, weight="bold")

    # ── Window helpers ────────────────────────────────────────────────────────
    def _center_window(self):
        self.update_idletasks()
        w, h = self.winfo_width(), self.winfo_height()
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"+{(sw-w)//2}+{(sh-h)//2}")

    # ── UI Construction ───────────────────────────────────────────────────────
    def _build_ui(self):
        root = tk.Frame(self, bg=BG, padx=28, pady=24)
        root.pack(fill="both", expand=True)

        # Title
        tk.Label(root, text="Snake · Water · Gun",
                 font=self.f_title, bg=BG, fg=WHITE).pack()
        tk.Label(root, text="Gun beats Snake  •  Water beats Gun  •  Snake beats Water",
                 font=self.f_sub, bg=BG, fg=MUTED).pack(pady=(2, 16))

        # Scoreboard
        self._build_scoreboard(root)

        # Arena (battle display)
        self._build_arena(root)

        # Result label
        self.result_var = tk.StringVar(value="Choose your weapon!")
        tk.Label(root, textvariable=self.result_var,
                 font=self.f_result, bg=BG, fg=ACCENT2,
                 pady=8).pack()

        # Choice buttons
        self._build_buttons(root)

        # Reset button
        tk.Button(root, text="Reset Game", font=self.f_score_l,
                  bg=CARD, fg=MUTED, relief="flat", bd=0,
                  activebackground=BORDER, activeforeground=WHITE,
                  cursor="hand2", pady=6, padx=16,
                  command=self._reset_game).pack(pady=(8, 0))

    def _build_scoreboard(self, parent):
        frame = tk.Frame(parent, bg=PANEL, pady=14, padx=10)
        frame.pack(fill="x", pady=(0, 16))
        frame.columnconfigure((0, 1, 2), weight=1)

        for col, (label, var_name, color) in enumerate([
            ("YOU", "player_score_var",   GREEN),
            ("DRAWS", "draws_var",        YELLOW),
            ("CPU", "computer_score_var", RED),
        ]):
            cell = tk.Frame(frame, bg=PANEL)
            cell.grid(row=0, column=col, sticky="nsew")

            setattr(self, var_name, tk.StringVar(value="0"))
            tk.Label(cell, textvariable=getattr(self, var_name),
                     font=self.f_score_n, bg=PANEL, fg=color).pack()
            tk.Label(cell, text=label,
                     font=self.f_score_l, bg=PANEL, fg=MUTED).pack()

    def _build_arena(self, parent):
        arena = tk.Frame(parent, bg=PANEL, pady=20, padx=20)
        arena.pack(fill="x", pady=(0, 4))
        arena.columnconfigure((0, 2), weight=1)
        arena.columnconfigure(1, weight=0)

        # Player side
        p_side = tk.Frame(arena, bg=PANEL)
        p_side.grid(row=0, column=0, sticky="nsew")
        tk.Label(p_side, text="YOU", font=self.f_score_l, bg=PANEL, fg=MUTED).pack()
        self.player_emoji_var = tk.StringVar(value="❓")
        self.player_emoji_lbl = tk.Label(p_side, textvariable=self.player_emoji_var,
                                          font=self.f_emoji, bg=PANEL, fg=WHITE)
        self.player_emoji_lbl.pack(pady=4)
        self.player_choice_var = tk.StringVar(value="")
        tk.Label(p_side, textvariable=self.player_choice_var,
                 font=self.f_sub, bg=PANEL, fg=MUTED).pack()

        # VS divider
        tk.Label(arena, text="VS", font=self.f_vs, bg=PANEL,
                 fg=BORDER, padx=20).grid(row=0, column=1)

        # CPU side
        c_side = tk.Frame(arena, bg=PANEL)
        c_side.grid(row=0, column=2, sticky="nsew")
        tk.Label(c_side, text="CPU", font=self.f_score_l, bg=PANEL, fg=MUTED).pack()
        self.cpu_emoji_var = tk.StringVar(value="❓")
        self.cpu_emoji_lbl = tk.Label(c_side, textvariable=self.cpu_emoji_var,
                                       font=self.f_emoji, bg=PANEL, fg=WHITE)
        self.cpu_emoji_lbl.pack(pady=4)
        self.cpu_choice_var = tk.StringVar(value="")
        tk.Label(c_side, textvariable=self.cpu_choice_var,
                 font=self.f_sub, bg=PANEL, fg=MUTED).pack()

    def _build_buttons(self, parent):
        frame = tk.Frame(parent, bg=BG)
        frame.pack(pady=(4, 0))

        for choice in ["snake", "water", "gun"]:
            emoji = EMOJI[choice]
            color = COLORS[choice]
            btn = tk.Button(
                frame,
                text=f"{emoji}\n{choice.upper()}",
                font=self.f_btn,
                bg=CARD, fg=color,
                relief="flat", bd=0,
                activebackground=BORDER,
                activeforeground=WHITE,
                cursor="hand2",
                width=8, height=3,
                command=lambda c=choice: self._play(c),
            )
            btn.pack(side="left", padx=8, pady=4)
            self._add_hover(btn, CARD, BORDER)

    # ── Hover effect ──────────────────────────────────────────────────────────
    def _add_hover(self, widget, normal_bg, hover_bg):
        widget.bind("<Enter>", lambda e: widget.config(bg=hover_bg))
        widget.bind("<Leave>", lambda e: widget.config(bg=normal_bg))

    # ── Game logic ────────────────────────────────────────────────────────────
    def _play(self, player_choice: str):
        if self.result_pending:
            return

        computer_choice = get_computer_choice()
        result = check_winner(player_choice, computer_choice)

        self.rounds += 1
        self.player_emoji_var.set(EMOJI[player_choice])
        self.player_choice_var.set(player_choice.capitalize())
        self.cpu_emoji_var.set(EMOJI[computer_choice])
        self.cpu_choice_var.set(computer_choice.capitalize())

        if result == "player":
            self.player_score += 1
            msg = "🎉  You Win!"
            color = GREEN
        elif result == "computer":
            self.computer_score += 1
            msg = "💻  CPU Wins!"
            color = RED
        else:
            self.draws += 1
            msg = "🤝  It's a Draw!"
            color = YELLOW

        self.result_var.set(msg)
        self.player_score_var.set(str(self.player_score))
        self.computer_score_var.set(str(self.computer_score))
        self.draws_var.set(str(self.draws))

        # Flash result colour on label
        for lbl in [self.player_emoji_lbl, self.cpu_emoji_lbl]:
            lbl.config(fg=color)

        self.result_pending = True
        self.after(1800, self._reset_round)

    def _reset_round(self):
        self.player_emoji_lbl.config(fg=WHITE)
        self.cpu_emoji_lbl.config(fg=WHITE)
        self.result_pending = False
        if self.rounds > 0:
            self.result_var.set("Choose your weapon!")

    def _reset_game(self):
        self.player_score   = 0
        self.computer_score = 0
        self.draws          = 0
        self.rounds         = 0
        self.result_pending = False
        self.player_score_var.set("0")
        self.computer_score_var.set("0")
        self.draws_var.set("0")
        self.player_emoji_var.set("❓")
        self.cpu_emoji_var.set("❓")
        self.player_choice_var.set("")
        self.cpu_choice_var.set("")
        self.result_var.set("Choose your weapon!")
        self.player_emoji_lbl.config(fg=WHITE)
        self.cpu_emoji_lbl.config(fg=WHITE)


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = SnakeWaterGunApp()
    app.mainloop()