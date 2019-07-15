from screen import Screen
from clock import Clock
from tkinter import Tk

tk_screen = Tk()
tk_screen.title("p=Pause, c=Clear, r=Random, click while paused to change cells")
window = Screen(tk_screen)
Clock(window).start()
window.start()
