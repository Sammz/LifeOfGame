from threading import Thread, Lock
from time import sleep
import config as c

pause = False
change_alive_lock = Lock()
cell_to_change_x = 0
cell_to_change_y = 0
new_cell_to_change = False


def pause_clock():
    global pause
    pause = not pause


def on_click_change(x, y):
    if pause:
        with change_alive_lock:
            global cell_to_change_x
            global cell_to_change_y
            global new_cell_to_change
            cell_to_change_x = x
            cell_to_change_y = y
            new_cell_to_change = True


class Clock(Thread):

    def __init__(self, grid: [[]], grid2: [[]], window):
        super().__init__()
        self.window = window
        self.grids = [grid, grid2]
        self.grid_index = 0

    def run(self) -> None:
        self.draw_first_frame()
        while True:
            other_grid_index = (self.grid_index + 1) % 2
            self.calculate_next_frame(other_grid_index)
            self.window.delete_all_alive()
            self.draw_next_frame(other_grid_index)
            self.grid_index = other_grid_index
            self.check_for_changes_and_sleeps()

    def draw_first_frame(self):
        for x in range(0, c.x_amount_cells):
            for y in range(0, c.y_amount_cells):
                old_grid_status = self.grids[self.grid_index][x][y]
                if old_grid_status:
                    self.window.draw(x, y, old_grid_status)

    def check_for_changes_and_sleeps(self):
        global pause
        if pause:
            while pause:
                global new_cell_to_change
                if new_cell_to_change:
                    self.change_cell_status()
                sleep(0.15)
        else:
            sleep(c.update_time)

    def calculate_next_frame(self, other_grid_index):
        for x in range(0, c.x_amount_cells):
            for y in range(0, c.y_amount_cells):
                alive = self.dead_or_alive(x, y)
                self.grids[other_grid_index][x][y] = alive

    def draw_next_frame(self, other_grid_index):
        for x in range(0, c.x_amount_cells):
            for y in range(0, c.y_amount_cells):
                old_grid_status = self.grids[self.grid_index][x][y]
                new_grid_status = self.grids[other_grid_index][x][y]
                if old_grid_status != new_grid_status:
                    self.window.draw(x, y, new_grid_status)

    def change_cell_status(self):
        with change_alive_lock:
            global cell_to_change_x
            global cell_to_change_y
            global new_cell_to_change
            new_cell_to_change = False
            alive = self.grids[self.grid_index][cell_to_change_x][cell_to_change_y]
            for i in range(0, 2):
                self.grids[i][cell_to_change_x][cell_to_change_y] = not alive
            self.window.draw(cell_to_change_x, cell_to_change_y, not alive)

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
        result = False
        if 0 <= x < len(self.grids[self.grid_index]) and 0 <= y < len(self.grids[self.grid_index][x]):
            result = self.grids[self.grid_index][x][y]
        return result
