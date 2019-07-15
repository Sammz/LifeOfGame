from tkinter import Tk, Canvas
import config as c
from clock import pause_clock, on_click_change, clear_grids, start_random


def random(event):
    start_random()


def clear(event):
    clear_grids()


def pause(event):
    pause_clock()


def click(event):
    x = int(event.x / c.cell_width)
    y = int(event.y / c.cell_height)
    on_click_change(x, y)


class Screen:

    def __init__(self, screen: Tk):
        self.screen = screen
        self.canvas = Canvas(self.screen, width=c.window_width, height=c.window_height)

    def start(self):
        self.canvas.bind("p", pause)
        self.canvas.bind("r", random)
        self.canvas.bind("c", clear)
        self.canvas.bind("<Button-1>", click)
        self.canvas.configure(background=c.dead_color)
        self.canvas.focus_set()
        self.canvas.pack()
        self.canvas.mainloop()

    def draw_pause(self):
        x = c.cell_width * 4
        y = c.cell_height * 5
        return self.canvas.create_text(x, y, fill=c.pause_color, text="II", font=("arial", 50))

    def draw_cell(self, x, y, alive):
        x = x * c.cell_width
        y = y * c.cell_height
        if alive:
            self.canvas.create_rectangle(x, y, x + c.cell_width, y + c.cell_height, fill=c.alive_color, tag="cell")
        else:
            self.canvas.delete(self.canvas.find_closest(x + 0.5 * c.cell_width, y + 0.5 * c.cell_height))

    def delete_cells(self):
        self.canvas.delete("cell")



