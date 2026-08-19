import random
import tkinter as tk
from tkinter import messagebox


CELL_SIZE = 30
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
BOARD_COLOR = "#111827"
GRID_COLOR = "#253047"

SHAPES = [
    ([[1, 1, 1, 1]], "#22d3ee"),
    ([[1, 1], [1, 1]], "#facc15"),
    ([[0, 1, 0], [1, 1, 1]], "#c084fc"),
    ([[0, 1, 1], [1, 1, 0]], "#4ade80"),
    ([[1, 1, 0], [0, 1, 1]], "#f87171"),
    ([[1, 0, 0], [1, 1, 1]], "#fb923c"),
    ([[0, 0, 1], [1, 1, 1]], "#60a5fa"),
]


class Tetris:
    def __init__(self, root):
        self.root = root
        self.root.title("테트리스")
        self.root.resizable(False, False)
        self.root.configure(bg="#0b1020")

        self.canvas = tk.Canvas(
            root,
            width=BOARD_WIDTH * CELL_SIZE,
            height=BOARD_HEIGHT * CELL_SIZE,
            bg=BOARD_COLOR,
            highlightthickness=0,
        )
        self.canvas.grid(row=0, column=0, rowspan=4, padx=(16, 10), pady=16)

        side = tk.Frame(root, bg="#0b1020", width=150)
        side.grid(row=0, column=1, sticky="n", padx=(0, 16), pady=22)
        side.grid_propagate(False)

        tk.Label(
            side, text="테트리스", font=("맑은 고딕", 18, "bold"),
            fg="#f8fafc", bg="#0b1020"
        ).pack(anchor="w")
        self.score_label = tk.Label(
            side, text="점수  0", font=("맑은 고딕", 12, "bold"),
            fg="#facc15", bg="#0b1020"
        )
        self.score_label.pack(anchor="w", pady=(14, 18))
        tk.Label(
            side,
            text="← →  이동\n↑  회전\n↓  빠르게 내리기\n스페이스  즉시 내리기\nR  다시 시작",
            justify="left", font=("맑은 고딕", 10),
            fg="#cbd5e1", bg="#0b1020"
        ).pack(anchor="w")

        self.root.bind("<KeyPress>", self.handle_key)
        self.reset()

    def reset(self):
        self.board = [[None for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.score = 0
        self.game_over = False
        self.drop_delay = 500
        self.spawn_piece()
        self.draw()
        self.root.after(self.drop_delay, self.tick)

    def spawn_piece(self):
        shape, color = random.choice(SHAPES)
        self.piece = [row[:] for row in shape]
        self.color = color
        self.x = (BOARD_WIDTH - len(self.piece[0])) // 2
        self.y = 0
        if self.collides(self.piece, self.x, self.y):
            self.game_over = True

    def collides(self, shape, x, y):
        for row_index, row in enumerate(shape):
            for column_index, filled in enumerate(row):
                if not filled:
                    continue
                board_x = x + column_index
                board_y = y + row_index
                if (
                    board_x < 0
                    or board_x >= BOARD_WIDTH
                    or board_y >= BOARD_HEIGHT
                    or (board_y >= 0 and self.board[board_y][board_x])
                ):
                    return True
        return False

    def move(self, dx, dy):
        if self.game_over:
            return False
        if not self.collides(self.piece, self.x + dx, self.y + dy):
            self.x += dx
            self.y += dy
            return True
        return False

    def rotate(self):
        rotated = [list(row) for row in zip(*self.piece[::-1])]
        for offset in (0, -1, 1, -2, 2):
            if not self.collides(rotated, self.x + offset, self.y):
                self.piece = rotated
                self.x += offset
                return

    def hard_drop(self):
        while self.move(0, 1):
            pass
        self.lock_piece()

    def lock_piece(self):
        for row_index, row in enumerate(self.piece):
            for column_index, filled in enumerate(row):
                if filled and self.y + row_index >= 0:
                    self.board[self.y + row_index][self.x + column_index] = self.color
        self.clear_lines()
        self.spawn_piece()

    def clear_lines(self):
        remaining = [row for row in self.board if any(cell is None for cell in row)]
        cleared = BOARD_HEIGHT - len(remaining)
        self.board = [[None] * BOARD_WIDTH for _ in range(cleared)] + remaining
        self.score += (0, 100, 300, 500, 800)[cleared]
        self.drop_delay = max(100, 500 - (self.score // 500) * 30)
        self.score_label.config(text=f"점수  {self.score}")

    def tick(self):
        if not self.game_over:
            if not self.move(0, 1):
                self.lock_piece()
            self.draw()
        self.root.after(self.drop_delay, self.tick)

    def handle_key(self, event):
        if event.keysym.lower() == "r":
            self.reset()
            return
        if self.game_over:
            return
        if event.keysym == "Left":
            self.move(-1, 0)
        elif event.keysym == "Right":
            self.move(1, 0)
        elif event.keysym == "Down":
            if not self.move(0, 1):
                self.lock_piece()
        elif event.keysym == "Up":
            self.rotate()
        elif event.keysym == "space":
            self.hard_drop()
        self.draw()

    def draw_cell(self, x, y, color):
        left = x * CELL_SIZE
        top = y * CELL_SIZE
        self.canvas.create_rectangle(
            left + 2, top + 2, left + CELL_SIZE - 2, top + CELL_SIZE - 2,
            fill=color, outline=""
        )

    def draw(self):
        self.canvas.delete("all")
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                self.canvas.create_rectangle(
                    x * CELL_SIZE, y * CELL_SIZE,
                    (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE,
                    fill=self.board[y][x] or BOARD_COLOR,
                    outline=GRID_COLOR,
                )
        if not self.game_over:
            for row_index, row in enumerate(self.piece):
                for column_index, filled in enumerate(row):
                    if filled and self.y + row_index >= 0:
                        self.draw_cell(
                            self.x + column_index,
                            self.y + row_index,
                            self.color,
                        )
        else:
            self.canvas.create_text(
                BOARD_WIDTH * CELL_SIZE // 2,
                BOARD_HEIGHT * CELL_SIZE // 2,
                text="GAME OVER\nR 키로 다시 시작",
                fill="#f8fafc", font=("맑은 고딕", 16, "bold"),
            )


if __name__ == "__main__":
    window = tk.Tk()
    Tetris(window)
    window.mainloop()