from threading import Thread, Lock
from time import sleep
import config as c
import random

pause = False
clear = False
random_begin = False

change_cell_status_lock = Lock()
cell_to_change_x = 0
cell_to_change_y = 0
new_cell_to_change = False


def pause_clock():
    global pause
    pause = not pause


def clear_grids():
    global clear
    clear = True


def start_random():
    global random_begin
    random_begin = True


def on_click_change(x, y):
    if pause:
        with change_cell_status_lock:
            global cell_to_change_x, cell_to_change_y, new_cell_to_change
            cell_to_change_x = x
            cell_to_change_y = y
            new_cell_to_change = True


class Clock(Thread):

    def __init__(self, window):
        super().__init__(daemon=True)
        self.window = window
        self.grids = self.init_grids(c.start_random)
        self.grid_index = 0

    def init_grids(self, random_grid):
        control_grid = [[random_grid for i in range(0, c.y_cells)] for k in range(0, c.x_cells)]
        if random_grid:
            grid = [[bool(random.getrandbits(1)) for i in range(0, c.y_cells)] for k in range(0, c.x_cells)]
            return [grid, control_grid]
        grid = [[random_grid for i in range(0, c.y_cells)] for k in range(0, c.x_cells)]
        return [grid, control_grid]

    def run(self) -> None:
        global pause

        self.draw_first_frame()
        while True:
            other_grid_index = (self.grid_index + 1) % 2
            self.calculate_next_frame(other_grid_index)
            self.draw_next_frame(other_grid_index)
            self.grid_index = other_grid_index
            if pause:
                self.pause_and_handle_user_input()
            else:
                sleep(c.update_time)

    def draw_first_frame(self):
        for x in range(0, c.x_cells):
            for y in range(0, c.y_cells):
                old_grid_status = self.grids[self.grid_index][x][y]
                if old_grid_status:
                    self.window.draw_cell(x, y, old_grid_status)

    def pause_and_handle_user_input(self):
        global pause, new_cell_to_change, random_begin, clear
        pause_id = self.window.draw_pause()

        while pause:
            if new_cell_to_change:
                self.change_cell_status()
                new_cell_to_change = False
            if random_begin:
                self.grids = self.init_grids(True)
                self.window.delete_cells()
                self.grid_index = 0
                self.window.canvas.delete(pause_id)
                self.draw_first_frame()
                random_begin = False
                pause = False
                return
            if clear:
                self.grids = self.init_grids(False)
                self.window.delete_cells()
                clear = False
            sleep(0.15)

        self.window.canvas.delete(pause_id)

    def calculate_next_frame(self, other_grid_index):
        for x in range(0, c.x_cells):
            for y in range(0, c.y_cells):
                alive = self.dead_or_alive(x, y)
                self.grids[other_grid_index][x][y] = alive

    def draw_next_frame(self, other_grid_index):
        for x in range(0, c.x_cells):
            for y in range(0, c.y_cells):
                old_grid_status = self.grids[self.grid_index][x][y]
                new_grid_status = self.grids[other_grid_index][x][y]
                if old_grid_status != new_grid_status:
                    self.window.draw_cell(x, y, new_grid_status)

    def change_cell_status(self):
        with change_cell_status_lock:
            global cell_to_change_x, cell_to_change_y
            alive = self.grids[self.grid_index][cell_to_change_x][cell_to_change_y]
            for i in range(0, 2):
                self.grids[i][cell_to_change_x][cell_to_change_y] = not alive
            self.window.draw_cell(cell_to_change_x, cell_to_change_y, not alive)

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
