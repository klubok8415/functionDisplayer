from function_displayer import Displayer
from expressions import Function

f = Function.parse(input())

displayer = Displayer()
displayer.add_function(f.calculate)
displayer.mainloop()
