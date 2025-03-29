import random

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


symbols = ["🍒", "🍋", "🍊", "🍇", "🍉", "🍓", "🍎", "🍍", "🍌", "💎"]


# @app.get("/spin")
# def spin():
#     # Generate random symbols for each column
#     cols = [[random.choice(symbols) for _ in range(3)] for _ in range(3)]
#
#     # Transpose columns into rows for win checking
#     rows = list(zip(*cols))
#
#     # Check for horizontal wins (rows)
#     win_row = any(all(s == row[0] for s in row) for row in rows)
#
#     # Check for vertical wins (columns)
#     win_col = any(all(rows[r][c] == rows[0][c] for r in range(3)) for c in range(3))
#
#     # Check for diagonal wins
#     win_diag1 = all(rows[i][i] == rows[0][0] for i in range(3))  # ↘ Diagonal
#     win_diag2 = all(rows[i][2 - i] == rows[0][2] for i in range(3))  # ↙ Diagonal
#
#     # Combine all win conditions
#     is_win = win_row or win_col or win_diag1 or win_diag2
#     message = "You win! 🎉" if is_win else "Try again!"
#
#     return JSONResponse(
#         content={
#             "columns": cols,
#             "win": is_win,
#             "message": message
#         }
#     )


@app.get("/spin")
def spin():
    win_chance = 0.3  # 30% chance to force a win

    if random.random() < win_chance:
        # Force a win by setting at least one row, column, or diagonal to the same symbol
        symbol = random.choice(symbols)

        # Randomly choose a winning type: row, column, or diagonal
        win_type = random.choice(["row", "col", "diag1", "diag2"])

        if win_type == "row":
            row_index = random.randint(0, 2)
            cols = [[random.choice(symbols) for _ in range(3)] for _ in range(3)]
            cols[0][row_index] = symbol
            cols[1][row_index] = symbol
            cols[2][row_index] = symbol

        elif win_type == "col":
            col_index = random.randint(0, 2)
            cols = [[symbol if i == col_index else random.choice(symbols) for i in range(3)] for _ in range(3)]

        elif win_type == "diag1":
            cols = [[symbol if i == j else random.choice(symbols) for j in range(3)] for i in range(3)]

        else:  # diag2
            cols = [[symbol if i + j == 2 else random.choice(symbols) for j in range(3)] for i in range(3)]

    else:
        # Generate normally (harder to win)
        cols = [[random.choice(symbols) for _ in range(3)] for _ in range(3)]

    # Transpose columns into rows for win checking
    rows = list(zip(*cols))

    # Check for horizontal wins (rows)
    win_row = any(all(s == row[0] for s in row) for row in rows)

    # Check for vertical wins (columns)
    win_col = any(all(rows[r][c] == rows[0][c] for r in range(3)) for c in range(3))

    # Check for diagonal wins
    win_diag1 = all(rows[i][i] == rows[0][0] for i in range(3))  # ↘ Diagonal
    win_diag2 = all(rows[i][2 - i] == rows[0][2] for i in range(3))  # ↙ Diagonal

    # Combine all win conditions
    is_win = win_row or win_col or win_diag1 or win_diag2
    message = "You win! 🎉" if is_win else "Try again!"

    return JSONResponse(
        content={
            "columns": cols,
            "win": is_win,
            "message": message
        }
    )


# Starting with uvicorn: uvicorn main:app --reload
