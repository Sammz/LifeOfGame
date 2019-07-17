from tkinter import Tk, Canvas
from threading import Condition
import config as c


class Screen:

    def __init__(self, screen: Tk):
        self.screen = screen
        self.canvas = Canvas(self.screen, width=c.window_width, height=c.window_height)
        self.clock = None
        self.event_lock = Condition()
        self.pause = False

    def start(self):
        self.canvas.bind("<space>", self.pause_event)
        self.canvas.bind("r", self.random_event)
        self.canvas.bind("c", self.clear_event)
        self.canvas.bind("<Button-1>", self.click_event)
        self.canvas.configure(background=c.dead_color)
        self.canvas.focus_set()
        self.canvas.pack()
        self.canvas.mainloop()

    def draw_pause(self):
        self.canvas.delete(c.pause_tag)
        x = c.cell_width * 4
        y = c.cell_height * 5
        self.canvas.create_text(x, y, fill=c.pause_color, text="II", font=("arial", 50), tag=c.pause_tag)

    def draw_cell(self, x, y):
        x = x * c.cell_width
        y = y * c.cell_height
        self.canvas.create_rectangle(x, y, x + c.cell_width, y + c.cell_height, fill=c.alive_color, tag=c.cell_tag)

    def delete_with_tag(self, tag):
        self.canvas.delete(tag)

    def delete_cell(self, x, y):
        x = x * c.cell_width
        y = y * c.cell_height
        self.canvas.delete(self.canvas.find_closest(x + 0.5 * c.cell_width, y + 0.5 * c.cell_height))

    def random_event(self, event):
        if self.pause:
            self.clear_event(event)
            self.clock.generate_and_draw_random_cells()
            self.draw_pause()

    def clear_event(self, event):
        if self.pause:
            self.clock.cell_set = set()
            self.delete_with_tag(c.cell_tag)

    def pause_event(self, event):
        self.event_lock.acquire()
        self.pause = not self.pause
        self.event_lock.notify()
        self.event_lock.release()

    def click_event(self, event):
        if self.pause:
            x = int(event.x / c.cell_width)
            y = int(event.y / c.cell_height)
            if (x, y) in self.clock.cell_set:
                self.clock.cell_set.remove((x, y))
                self.delete_cell(x, y)
            else:
                self.clock.cell_set.add((x, y))
                self.draw_cell(x, y)



