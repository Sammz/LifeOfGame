from tkinter import Tk, Canvas
import config as c


class Screen:

    def __init__(self, screen: Tk):
        self.screen = screen
        self.canvas = Canvas(self.screen, width=c.window_width, height=c.window_height)

    def start(self):
        self.canvas.pack()
        self.canvas.mainloop()

    def draw(self, x, y, alive):
        color = c.dead_color
        if alive:
            color = c.alive_color
        x = x*c.cell_width
        y = y*c.cell_height
        self.canvas.create_rectangle(x, y, x + c.cell_width, y + c.cell_height, fill=color)
