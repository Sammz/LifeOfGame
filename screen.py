from tkinter import Tk, Canvas
from threading import Condition
import config as c


class Screen:

    def __init__(self, screen: Tk):
        self.screen = screen
        self.canvas = Canvas(self.screen, width=c.window_width, height=c.window_height)
        self.clock = None
        self.event_condition = Condition()
        self.draw_condition = Condition()
        self.pause = True

    def start(self):
        self.canvas.bind("<space>", self.pause_event)
        self.canvas.bind("r", self.random_event)
        self.canvas.bind("c", self.clear_event)
        self.canvas.bind("<Button-1>", self.click_event)
        self.canvas.bind("w", self.speed_up_event)
        self.canvas.bind("s", self.speed_down_event)
        self.canvas.configure(background=c.dead_color)
        self.canvas.focus_set()
        self.canvas.pack()
        self.canvas.mainloop()

    def draw_next_frame(self):
        self.draw_condition.acquire()
        self.delete_with_tag(c.cell_tag)
        for (x, y) in self.clock.cell_set:
            self.draw_cell(x, y)
        self.canvas.update()
        self.draw_condition.notify()
        self.draw_condition.release()

    def trigger_draw(self):
        self.draw_condition.acquire()
        self.screen.after_idle(self.draw_next_frame)
        self.draw_condition.wait()
        self.draw_condition.release()

    def draw_pause(self):
        self.canvas.delete(c.pause_tag)
        self.canvas.configure(background=c.pause_background_color)
        for xx in range(0, c.x_cells):
            xx = xx * c.cell_width
            self.canvas.create_line(xx, 0, xx, c.window_height, width=1, tag=c.pause_tag, fill=c.pause_grid_color)
        for yy in range(0, c.x_cells):
            yy = yy * c.cell_height
            self.canvas.create_line(0, yy, c.window_width, yy, width=1, tag=c.pause_tag, fill=c.pause_grid_color)

        x = c.cell_width * 4
        y = c.cell_height * 5
        self.canvas.create_text(x, y, fill=c.pause_sign_color, text="II", font=("arial", 50), tag=c.pause_tag)

    def draw_cell(self, x, y):
        x = x * c.cell_width
        y = y * c.cell_height
        self.canvas.create_rectangle(x, y, x + c.cell_width, y + c.cell_height, fill=c.alive_color, tag=c.cell_tag)

    def delete_with_tag(self, tag):
        if tag == c.pause_tag:
            self.canvas.configure(background=c.dead_color)
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
        self.event_condition.acquire()
        self.pause = not self.pause
        self.event_condition.notify()
        self.event_condition.release()

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

    def speed_up_event(self, event):
        if self.clock.update_speed > 0:
            self.clock.update_speed -= 0.1

    def speed_down_event(self, event):
        if self.clock.update_speed <= 1:
            self.clock.update_speed += 0.1











