from tkinter import *
from function_displayer import Displayer
from expressions import Function
from scale_handler import Handler

f = Function.parse(input())

root = Tk()

frame1 = Frame(root)
handler = Handler(root)
frame1.grid(row=0, column=0)
handler.grid(row=0, column=1)

displayer = Displayer(frame1)
displayer.add_function(f.calculate)
displayer.pack()

root.mainloop()
