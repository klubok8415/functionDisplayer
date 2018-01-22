from tkinter import *
from function_displayer import Displayer
from expressions import Function

f = Function.parse(input())

root = Tk()

displayer = Displayer(root)
displayer.pack()
displayer.add_function(f.calculate)

root.mainloop()
#  commit tes