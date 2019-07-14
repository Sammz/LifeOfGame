from tkinter import Tk, Canvas
import config as c
from clock import pause_clock, on_click_change


def random(event):
    pass


def clear(event):
    pass


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

    def delete_all_alive(self):
        self.canvas.delete(c.alive_color)

    def draw(self, x, y, alive):
        color = c.dead_color
        if alive:
            color = c.alive_color
        x = x * c.cell_width
        y = y * c.cell_height
        self.canvas.create_rectangle(x, y, x + c.cell_width, y + c.cell_height, fill=color)
