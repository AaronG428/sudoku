import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import random
from random import randint, shuffle
import time

#check distinct across dimension
def dimension_check(grid, logging = False, rowcode = '', colcode = '', condition = ''):
    for i in range(len(grid)):
        dist = set()
        for j in range(len(grid[0])):
            row = eval(rowcode)
            col = eval(colcode)
            val = grid[row][col]
            if val == 0:
                continue
            if int(val) in dist:
                if logging:
                    print(f"{condition} condition violated: digit {val} at {(row,col)}")
                return False 
            dist.add(int(val))
    return True

#input: 9x9 list of ints
def sats_constraints(grid, logging = False):
    rowcheck = dimension_check(grid, logging, rowcode = 'i', colcode = 'j', condition = 'row')
    colcheck = dimension_check(grid, logging, rowcode = 'j', colcode = 'i', condition = 'col')
    boxcheck = dimension_check(grid, logging, rowcode = '3*(i//3) + j//3', colcode = '3*(i%3) + j%3', condition = 'box')

    return rowcheck and colcheck and boxcheck

numberList=[1,2,3,4,5,6,7,8,9]


def generateValidPuzzle():
    #TODO test
    # entries = [9*[0] for _ in range(9)]
    entries = generate_full_sudoku()
    remove_cells(entries)
    return entries



def remove_cells(grid, misses = 1, max_gone = 80):
    counter = 0
    while misses > 0 and counter < max_gone:
        counter += 1
        print(f"current grid:{counter}")
        print(grid)
        #Select random nonempty cell
        row = randint(0,8)
        col = randint(0,8)
        while grid[row][col]==0:
            row = randint(0,8)
            col = randint(0,8)
        backup = grid[row][col]
        grid[row][col] = 0
        gridCopy = [l[:] for l in  grid]
        _, solutions_count = count_sudoku_solutions(gridCopy)
        if solutions_count > 1:
            grid[row][col] = backup
            misses -= 1
    return grid

        

def count_sudoku_solutions(grid):
    count = [0]  # use a list so it's mutable inside nested function
    out_grid = []

    def is_valid(row, col, num):
        # Check row and column
        for i in range(9):
            if grid[row][i] == num or grid[i][col] == num:
                return False

        # Check 3x3 box
        box_row = row - row % 3
        box_col = col - col % 3
        for i in range(3):
            for j in range(3):
                if grid[box_row + i][box_col + j] == num:
                    return False
        return True

    def solve(row=0, col=0):
        if row == 9:
            count[0] += 1
            out_grid.append([l[:] for l in grid])
            return

        next_row, next_col = (row, col + 1) if col < 8 else (row + 1, 0)

        if grid[row][col] != 0:
            solve(next_row, next_col)
        else:
            for num in range(1, 10):
                if is_valid(row, col, num):
                    grid[row][col] = num
                    solve(next_row, next_col)
                    grid[row][col] = 0  # backtrack

    solve()
    print(f"out_grid:{out_grid[0]}")
    return out_grid[0], count[0]

import random

def generate_full_sudoku():
    board = [[0 for _ in range(9)] for _ in range(9)]

    def is_valid(row, col, num):
        # Check row and column
        for i in range(9):
            if board[row][i] == num or board[i][col] == num:
                return False

        # Check 3x3 box
        box_row = row - row % 3
        box_col = col - col % 3
        for i in range(3):
            for j in range(3):
                if board[box_row + i][box_col + j] == num:
                    return False
        return True

    def fill_cell(row=0, col=0):
        if row == 9:
            return True  # Grid complete

        next_row, next_col = (row, col + 1) if col < 8 else (row + 1, 0)

        nums = list(range(1, 10))
        random.shuffle(nums)
        for num in nums:
            if is_valid(row, col, num):
                board[row][col] = num
                if fill_cell(next_row, next_col):
                    return True
                board[row][col] = 0  # backtrack

        return False  # No valid digit

    fill_cell()
    return board


class SudokuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku")
        self.difficulty = tk.StringVar(value="Easy")
        self.selected_entry = None
        self.create_menu()

    def create_menu(self):
        self.clear_window()

        tk.Label(self.root, text="Select Difficulty:", font=("Arial", 14)).pack(pady=10)

        difficulties = ["Easy", "Medium", "Hard"]
        for level in difficulties:
            tk.Radiobutton(self.root, text=level, variable=self.difficulty, value=level, font=("Arial", 12)).pack(anchor=tk.W)

        tk.Button(self.root, text="Start Game", command=self.start_game, font=("Arial", 12)).pack(pady=20)

    def start_game(self):
        seed = 42
        random.seed(seed)
        self.clear_window()
        self.entries = [[None for _ in range(9)] for _ in range(9)]
        self.grid_frame = tk.Frame(self.root)
        self.grid_frame.pack(pady=10)
        self.create_grid()
        self.create_buttons()

    def create_grid(self):
        cell_size = 40
        canvas_size = cell_size * 9

        self.canvas = tk.Canvas(self.grid_frame, width=canvas_size, height=canvas_size)
        self.canvas.grid(row=0, column=0)

        for i in range(10):
            width = 3 if i % 3 == 0 else 1
            self.canvas.create_line(0, i * cell_size, canvas_size, i * cell_size, width=width)
            self.canvas.create_line(i * cell_size, 0, i * cell_size, canvas_size, width=width)

        for row in range(9):
            for col in range(9):
                entry = tk.Entry(self.grid_frame, width=2, font=("Arial", 18), justify="center", bd=0)
                entry.place(x=col * cell_size + 2, y=row * cell_size + 2, width=cell_size - 4, height=cell_size - 4)
                entry.bind("<FocusIn>", lambda e, r=row, c=col: self.highlight_cells(r, c))
                
                self.entries[row][col] = entry

        valid_puzzle = generateValidPuzzle()
        print(valid_puzzle)
        valid_puzzle = remove_cells(valid_puzzle, misses = 5) #TODO: change attempts to match difficulty
        print(valid_puzzle) 
        for i in range(len(valid_puzzle)):
            for j in range(len(valid_puzzle[0])):
                val = valid_puzzle[i][j]
                entry = self.entries[i][j]
                entry.delete(0)
                
                if val != 0:
                    entry.insert(0,val)
                    entry.config(state='readonly')
        messagebox.showinfo("Info", f"Puzzle Generated")
        
                    

    def highlight_cells(self, selected_row, selected_col):
        for row in range(9):
            for col in range(9):
                entry = self.entries[row][col]
                pre_state = entry.cget('state')
                # print(pre_state)
                entry.config(state='normal')
                if row == selected_row or col == selected_col or (row//3 == selected_row//3 and col//3 == selected_col//3):
                    entry.config(bg="#406fd6")
                    entry.config(readonlybackground="#406fd6")
                else:
                    entry.config(bg="systemTextBackgroundColor")
                    entry.config(readonlybackground="systemTextBackgroundColor")
                # if(col%2==0):
                entry.config(state = pre_state)

    def create_buttons(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Button(frame, text="Clear", command=self.clear_board).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Back to Menu", command=self.create_menu).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Solve (stub)", command=self.solve_stub).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Hint (stub)", command=self.hint_stub).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Check Puzzle (test)", command=self.check_puzzle_test).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Create Puzzle (test)", command=self.create_puzzle_test).pack(side=tk.LEFT, padx=5)

    def clear_board(self):
        for row in self.entries:
            for entry in row:
                entry.config(state='normal')
                entry.delete(0, tk.END)
                # entry.configure(bg="white")

    def solve_stub(self):
        puzzle = self.convert_entries()

        solution, count = count_sudoku_solutions(puzzle)
        
        if count > 1:
            messagebox.showinfo("Warn", f"Non-unique solution")
        
        for i in range(len(solution)):
            for j in range(len(solution[0])):
                entry = self.entries[i][j]
                if entry.get() != solution[i][j]:
                    entry.delete(0)
                    entry.insert(0,solution[i][j])
        messagebox.showinfo("Info", f"Puzzle solved")

    def hint_stub(self):
        messagebox.showinfo("Info", f"Hint not implemented yet! Difficulty: {self.difficulty.get()}")

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def check_puzzle_test(self):
        valid_puzzle = sats_constraints(self.convert_entries())
        messagebox.showinfo("Info", f"Puzzle Valid: {valid_puzzle}")

    def create_puzzle_test(self):
        valid_puzzle = generateValidPuzzle()
        for i in range(len(valid_puzzle)):
            for j in range(len(valid_puzzle[0])):
                entry = self.entries[i][j]
                entry.delete(0)
                entry.insert(0,valid_puzzle[i][j])

                # entry.config(state='readonly')
        messagebox.showinfo("Info", f"Puzzle Generated")
        

    def convert_entries(self):
        mat =  [[val.get() for val in row] for row in self.entries]
        # Each cell contains only numerics
        for i in range(len(mat)):
            for j in range(len(mat[0])):
                val = mat[i][j]
                if len(val.strip()) == 0:
                    mat[i][j] = 0
                elif not str.isdecimal(val):
                    raise Exception("Strings not decimal")
                elif int(val) > 9 or int(val) < 0:
                    raise Exception("Strings too large")
                else:
                    mat[i][j] = int(val)
        return mat





if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuApp(root)
    root.mainloop()


