import tkinter as tk
import numpy as np
import random, math
import threading

# The universe of the Game of Life is an infinite, two-dimensional orthogonal grid of square cells, each of which is in one of two possible states, live or dead (or populated and unpopulated, respectively). Every cell interacts with its eight neighbors, which are the cells that are horizontally, vertically, or diagonally adjacent. At each step in time, the following transitions occur:

# 1. Any live cell with fewer than two live neighbours dies, as if by underpopulation.
# 2. Any live cell with two or three live neighbours lives on to the next generation.
# 3. Any live cell with more than three live neighbours dies, as if by overpopulation.
# 4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

# The initial pattern constitutes the seed of the system. The first generation is created by applying the above rules simultaneously to every cell in the seed, live or dead; births and deaths occur simultaneously, and the discrete moment at which this happens is sometimes called a tick.[nb 1] Each generation is a pure function of the preceding one. The rules continue to be applied repeatedly to create further generations.


class GameOfLife(tk.Tk):
    def __init__(self, grid_size, resolution):
        # initialize game window and attributes
        super().__init__()

        self.title = "Conway's Game of Life"

        self.grid_size = grid_size
        self.resolution = resolution
        self.scale = self.grid_size / self.resolution

        self.geometry(str(self.grid_size + 400) + 'x' + str(self.grid_size + 200))
        self.canvas =tk.Canvas(self, width=self.grid_size, height=self.grid_size, background='grey5')
        self.canvas.pack()

        self.grid = np.zeros((self.resolution, self.resolution))

        for x in range(0, self.resolution):
            for y in range(0, self.resolution):
                self.grid[x][y] = random.randint(0, 1)

        self.running = False

        self.start_button = tk.Button(self,text='Start', command=self.start_game)
        self.start_button.pack()
        self.random_button = tk.Button(self, text='Random', command=self.random_game)
        self.random_button.pack()
        self.stop_button = tk.Button(self, text='Stop', command=self.stop_game)
        self.stop_button.pack()
        self.reset_button = tk.Button(self, text='Reset', command=self.reset_game)
        self.reset_button.pack()

        # Set a click event on the canvas.
        self.canvas.bind('<Button1-Motion>', self.on_click)
        self.canvas.bind('<Button-1>', self.on_click)
        
    
    def generate_board(self):
        # draw square on board if cell is live (value = 1)
        for x in range(0, self.resolution):
            for y in range(0, self.resolution):
                scaled_x = x * self.scale
                scaled_y = y * self.scale
                if self.grid[x][y] == 1:
                    self.canvas.create_rectangle(scaled_x, scaled_y, scaled_x + self.scale, scaled_y + self.scale, fill='grey95', outline='grey50')

    def on_click(self, event):
        # allow user to make their own starting pattern
        gridx = math.floor((event.y/self.grid_size)*self.resolution)
        gridy = math.floor((event.x/self.grid_size)*self.resolution)

        self.grid[gridx][gridy] = 1
        self.canvas.create_rectangle(gridx, gridy, gridx + self.scale, gridy + self.scale, fill='grey95', outline='grey50')

    def start_game(self):
        # start the game by generating the board and updating
        self.running = True
        self.after(17, self.update_board)

    def random_game(self):
        self.generate_board()

    def stop_game(self):
        # stop the game by setting self.running to False
        self.running = False

    def reset_game(self):
        #reset the game by clearing board
        self.canvas.delete('all')
        for x in range(0, self.resolution):
            for y in range(0, self.resolution):
                self.grid[x][y] = random.randint(0, 1)

    def count_neighbors(self, x, y):
        # count the number of live neighbors
        count = 0
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                if x == i and y == j:
                    continue

                # account for the edge cases: if i or j goes beyond the game's border, it will just wrap around to the beginning (hence the modulo)
                wrap_x = (i%self.resolution)
                wrap_y = (j%self.resolution)
                if self.grid[wrap_x][wrap_y] == 1:
                    count += 1

        return count


    def apply_rules(self):
        # apply the four rules to the existing grid
        updated_grid = np.zeros((self.resolution, self.resolution))

        for x in range(0, self.resolution):
            for y in range(0, self.resolution):
                neighbors = self.count_neighbors(x, y)

                # current cell is alive
                if self.grid[x][y] == 1:
                    # if underpopulated or overpopulated, die
                    if neighbors < 2 or neighbors > 3:
                        updated_grid[x][y] = 0
                    else:
                        updated_grid[x][y] = 1
                # current cell is dead
                if self.grid[x][y] == 0:
                    # if perfectly populated, reproduce
                    if neighbors == 3:
                        updated_grid[x][y] = 1
        return updated_grid
    
    def update_board(self):
        # update the board after changing the grid
        if self.running:
            self.canvas.delete('all')
            self.grid = self.apply_rules()
            self.generate_board()
            self.after(17, self.update_board)


if __name__ == "__main__":
    tkinter_canvas = GameOfLife(800, 100)
    tkinter_canvas.mainloop()