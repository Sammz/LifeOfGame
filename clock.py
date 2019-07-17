from threading import Thread
from time import sleep, time
import config as c
import random


class Clock(Thread):

    def __init__(self, window):
        super().__init__(daemon=True)
        self.window = window
        self.window.clock = self
        self.cell_set = set()

    def run(self) -> None:
        while True:
            start = time()
            self.calculate_next_frame()
            self.window.delete_with_tag(c.cell_tag)
            self.draw_next_frame()
            while self.window.pause:
                self.window.draw_pause()
                self.window.event_lock.acquire()
                self.window.event_lock.wait()
                self.window.event_lock.release()

            self.window.delete_with_tag(c.pause_tag)
            duration = time() - start
            if duration < c.update_time:
                sleep(c.update_time - duration)

    def generate_and_draw_random_cells(self):
        for x in range(0, c.x_cells):
            for y in range(0, c.y_cells):
                if bool(random.getrandbits(1)):
                    self.cell_set.add((x, y))
        self.draw_next_frame()

    def calculate_next_frame(self):
        neighbours_dict = dict()
        for (x, y) in self.cell_set:
            if (x, y) not in neighbours_dict:
                neighbours_dict[(x, y)] = 0
            for i in range(-1, 2):
                for k in range(-1, 2):
                    if i != 0 or k != 0:
                        key = (x + i, y + k)
                        if key in neighbours_dict:
                            neighbours_dict[key] += 1
                        else:
                            neighbours_dict[key] = 1
        for coordinate in neighbours_dict:
            neighbours = neighbours_dict[coordinate]
            if coordinate in self.cell_set:
                if neighbours != 2 and neighbours != 3:
                    self.cell_set.remove(coordinate)
            elif neighbours == 3:
                self.cell_set.add(coordinate)

    def draw_next_frame(self):
        for (x, y) in self.cell_set:
            self.window.draw_cell(x, y)
