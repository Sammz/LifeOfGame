from threading import Thread
from time import sleep

import config as c


class Clock(Thread):

    def __init__(self, grid: [[]], grid2: [[]], window):
        super().__init__()
        self.window = window
        self.grids = [grid, grid2]
        self.grid_index = 0

    def run(self) -> None:
        for x in range(0, c.x_amount_cells):
            for y in range(0, c.y_amount_cells):
                old_grid_status = self.grids[self.grid_index][x][y]
                self.window.draw(x, y, old_grid_status)

        while True:
            other_grid_index = (self.grid_index + 1) % 2
            for x in range(0, c.x_amount_cells):
                for y in range(0, c.y_amount_cells):
                    alive = self.dead_or_alive(x, y)
                    self.grids[other_grid_index][x][y] = alive

            for x in range(0, c.x_amount_cells):
                for y in range(0, c.y_amount_cells):
                    old_grid_status = self.grids[self.grid_index][x][y]
                    new_grid_status = self.grids[other_grid_index][x][y]
                    if old_grid_status != new_grid_status:
                        self.window.draw(x, y, new_grid_status)

            self.grid_index = (self.grid_index + 1) % 2
            sleep(0.5)

    def dead_or_alive(self, x: int, y: int):
        count_alive = 0
        for i in range(-1, 2):
            for k in range(-1, 2):
                if (i != 0 or k != 0) and self.safe_get(x + i, y + k):
                    count_alive += 1

        if count_alive < 2 or count_alive > 3:
            return False
        if not self.safe_get(x, y) and count_alive != 3:
            return False
        elif 2 <= count_alive < 4:
            return True

    def safe_get(self, x, y):
        if 0 <= x < len(self.grids[self.grid_index]) and 0 <= y < len(self.grids[self.grid_index][x]):
            return self.grids[self.grid_index][x][y]
        else:
            return False
