from tkinter import *
from function_displayer import Displayer
from displayer_handler import handler_frame


class MainFrame:
    def __init__(self):
        self.root = Tk()
        self.canvas_frame = Frame()
        self.displayer = Displayer(self.canvas_frame, 0, 0, 0, 0)
        self.handler_frame = handler_frame(self.root, self.displayer)
        self.canvas_frame.grid(row=0, column=0)
        self.handler_frame.grid(row=0, column=1)
        self.displayer.pack()

    def mainloop(self):
        self.root.mainloop()
