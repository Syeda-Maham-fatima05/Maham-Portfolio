from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

# Global variables
score = 0
grid = [[0, 0, 0, 0] for _ in range(4)]

# ------------------------------
# Game Functions
# ------------------------------

def transpose(grid):
    return [list(row) for row in zip(*grid)]

def add_new_tile(grid):
    empty = [(r, c) for r in range(4) for c in range(4) if grid[r][c] == 0]
    if not empty:
        return grid
    r, c = random.choice(empty)
    grid[r][c] = 2 if random.random() < 0.9 else 4
    return grid

def compress(row):
    new = [i for i in row if i != 0]
    while len(new) < 4:
        new.append(0)
    return new

def merge(row):
    global score
    for i in range(3):
        if row[i] == row[i+1] and row[i] != 0:
            row[i] *= 2
            score += row[i]
            row[i+1] = 0
    return row

def move_left(grid):
    new = []
    for row in grid:
        row = compress(row)
        row = merge(row)
        row = compress(row)
        new.append(row)
    return new

def move_right(grid):
    new = []
    for row in grid:
        row = row[::-1]
        row = compress(row)
        row = merge(row)
        row = compress(row)
        new.append(row[::-1])
    return new

def move_up(grid):
    grid = transpose(grid)
    grid = move_left(grid)
    grid = transpose(grid)
    return grid

def move_down(grid):
    grid = transpose(grid)
    grid = move_right(grid)
    grid = transpose(grid)
    return grid

def game_over(grid):
    for row in grid:
        if 0 in row:
            return False
    for r in range(4):
        for c in range(3):
            if grid[r][c] == grid[r][c+1]:
                return False
    for r in range(3):
        for c in range(4):
            if grid[r][c] == grid[r+1][c]:
                return False
    return True

# ------------------------------
# Flask Routes
# ------------------------------

@app.route("/")
def home():
    global grid, score
    # Reset the game automatically on page load
    score = 0
    grid = [[0, 0, 0, 0] for _ in range(4)]
    add_new_tile(grid)
    add_new_tile(grid)
    return render_template("index2.html")

@app.route("/board")
def board():
    return jsonify({"board": grid, "score": score})

@app.route("/move", methods=["POST"])
def move():
    global grid
    data = request.get_json()
    direction = data["direction"]

    if direction == "left":
        grid = move_left(grid)
    elif direction == "right":
        grid = move_right(grid)
    elif direction == "up":
        grid = move_up(grid)
    elif direction == "down":
        grid = move_down(grid)

    grid = add_new_tile(grid)
    over = game_over(grid)

    return jsonify({
        "board": grid,
        "score": score,
        "game_over": over
    })

@app.route("/newgame", methods=["POST"])
def new_game():
    global grid, score
    score = 0
    grid = [[0, 0, 0, 0] for _ in range(4)]
    add_new_tile(grid)
    add_new_tile(grid)
    return jsonify({"board": grid, "score": score})

# ------------------------------
if __name__ == "__main__":
    # Initial two tiles
    add_new_tile(grid)
    add_new_tile(grid)
    app.run(host="0.0.0.0", port=5000, debug=True)