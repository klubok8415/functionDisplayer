from tkinter import *
from expressions import Function

class Displayer(Canvas):
    def __init__(self, root,  x_min, x_max, y_min, y_max, x_scale=1, y_scale=1, canvas_size=500):
        super(Displayer, self).__init__(root, width=canvas_size, height=canvas_size, bg="white")
        self.canvas_size = canvas_size
        self.x_scale = x_scale
        self.y_scale = y_scale
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max

    def add_axis(self):
        self.y_axis = self.create_line(self.canvas_size // 2, self.canvas_size, self.canvas_size // 2, 0,
                                       width=1, arrow=LAST)
        self.x_axis = self.create_line(0, self.canvas_size // 2, self.canvas_size, self.canvas_size // 2,
                                       width=1, arrow=LAST)

        # marking x_axis
        for i in range(501):
            if i % 50 == 0:
                k = -250 + i
                self.create_line(k + 250, -2 + 250, k + 250, 2 + 250,
                                 width=0.25, fill='black')

                self.create_text(k + 250, -10 + 250,
                                 text=str(k * self.y_scale * (self.x_max - self.x_min) // (self.x_scale * 500)), fill='black',
                                 font=('Helvectica', '10'))
        # marking y_axis
        for j in range(501):
            if j % 50 == 0:
                k = -250 + j
                if k != 0:
                    self.create_line(-2 + 250, k + 250, 2 + 250, k + 250,
                                     width=0.25, fill='black')

                    self.create_text(10 + 250, k + 250,
                                     text=str(k * (self.y_max - self.y_min) // 500), fill='black',
                                     font=('Helvectica', '10'))

    def add_function(self, f, color="black"):
        previous_point = [0, 0]
        for x in range(-251, 250):
            x = x * (self.x_max - self.x_min) / 500
            point = [x * 500 // (self.x_max - self.x_min) + 250,
                     250 - (f(x / self.x_scale) * self.y_scale) * 500 // (self.y_max - self.y_min)]
            self.create_line(previous_point, point, fill=color)
            previous_point = point

    def add_point(self, x, y, color="black"):
        self.create_oval(
            self.x_scale * x - 1,
            500 - self.y_scale * y + 1,
            self.x_scale * x + 1,
            500 - self.y_scale * y - 1,
            fill=color)


class Handler(Frame):
    def __init__(self, root, displayer):
        super(Handler, self).__init__(root)
        self.displayer = displayer
        # Entries and labels behind
        self.x_min_entry = Entry(self, width=10)
        self.x_min_entry.insert(0, '-5')
        self.x_max_entry = Entry(self, width=10)
        self.x_max_entry.insert(0, '5')
        self.y_min_entry = Entry(self, width=10)
        self.y_min_entry.insert(0, '-25')
        self.y_max_entry = Entry(self, width=10)
        self.y_max_entry.insert(0, '25')
        self.function_entry = Entry(self, width=20)

        self.x_min_label = Label(self, text='x min')
        self.x_max_label = Label(self, text='x max')
        self.y_max_label = Label(self, text='y max')
        self.y_min_label = Label(self, text='y min')
        self.function_label = Label(self, text='function input')

        self.x_min_label.grid(row=0, column=0)
        self.x_max_label.grid(row=0, column=1)
        self.x_min_entry.grid(row=1, column=0)
        self.x_max_entry.grid(row=1, column=1)
        self.y_min_label.grid(row=2, column=0)
        self.y_max_label.grid(row=2, column=1)
        self.y_min_entry.grid(row=3, column=0)
        self.y_max_entry.grid(row=3, column=1)
        self.function_label.grid(row=4, column=0, columnspan=2)
        self.function_entry.grid(row=5, column=0, columnspan=2)

        # handling button
        self.rescale_but = Button(self, text='draw', command=self.rescale)
        self.rescale_but.grid(row=6, column=0, columnspan=2)

    def rescale(self):
        self.displayer.x_max = int(self.x_max_entry.get())
        self.displayer.x_min = int(self.x_min_entry.get())
        self.displayer.y_max = int(self.y_max_entry.get())
        self.displayer.y_mix = int(self.y_min_entry.get())
        self.displayer.delete(ALL)
        self.displayer.add_axis()
        f = Function.parse(self.function_entry.get())
        self.displayer.add_function(f.calculate)
