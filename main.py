from screen import Screen
from clock import Clock
import config as c
from tkinter import *
import random

tk_screen = Tk()
grid = [[bool(random.getrandbits(1)) for i in range(0, c.y_amount_cells)] for k in range(0, c.x_amount_cells)]
# grid = [[False for i in range(0, c.y_amount_cells)] for k in range(0, c.x_amount_cells)]


grid2 = [[False for i in range(0, c.y_amount_cells)] for k in range(0, c.x_amount_cells)]
window = Screen(tk_screen)

Clock(grid, grid2, window).start()

window.start()
