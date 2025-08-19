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

def fill_grid(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                shuffle(numberList)
                for val in numberList:
                    grid[i][j] = val
                    if sats_constraints(grid):
                        if fill_grid(grid):
                            return True
                    grid[i][j] = 0
                return False # no val found
    return True #All cells filled

def generateValidPuzzle():
    #TODO test
    numberList.sort()
    entries = [9*[0] for _ in range(9)]
    fill_grid(entries)
    return entries




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
                    

    def highlight_cells(self, selected_row, selected_col):
        for row in range(9):
            for col in range(9):
                entry = self.entries[row][col]
                if row == selected_row or col == selected_col or (row//3 == selected_row//3 and col//3 == selected_col//3):
                    entry.configure(bg="#40c5d6")
                else:
                    entry.configure(bg="black")

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
                entry.delete(0, tk.END)
                # entry.configure(bg="white")

    def solve_stub(self):
        messagebox.showinfo("Info", f"Solver not implemented yet! Difficulty: {self.difficulty.get()}")

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
                # entry.state(['disabled'])
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


