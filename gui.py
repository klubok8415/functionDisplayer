from tkinter import *
from function_parser import default_parser
import math

class Displayer(Canvas):

    def __init__(self, root, x_min=0, x_max=0, y_min=0, y_max=0, canvas_size=500):
        self.root = root
        self.canvas_size = canvas_size
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        super(Displayer, self).__init__(root, width=canvas_size, height=canvas_size, bg='white')

    def add_axis(self):
        x_position = self.canvas_size // 2 + (self.y_max + self.y_min) / 2 * self.canvas_size / (self.y_max - self.y_min)
        y_position = self.canvas_size // 2 - (self.x_max + self.x_min) / 2 * self.canvas_size / (self.x_max - self.x_min)

        self.y_axis = self.create_line(y_position, self.canvas_size, y_position, 0,
                                       width=1, arrow=LAST, fill="gray")
        self.x_axis = self.create_line(0, x_position, self.canvas_size, x_position,
                                       width=1, arrow=LAST, fill="gray")

        # marking x_axis
        for i in range(self.canvas_size + 1):
            if i % (self.canvas_size / 10) == 0:
                k = -self.canvas_size // 2 + i
                self.create_line(k + self.canvas_size // 2, -2 + x_position,
                                 k + self.canvas_size // 2, 2 + x_position,
                                 width=0.25, fill='gray')

                self.create_text(k + self.canvas_size // 2, -10 + x_position,
                                 text=str(k * (self.x_max - self.x_min) // self.canvas_size), fill='black',
                                 font=('Helvectica', '10'))
        # marking y_axis
        for j in range(self.canvas_size + 1):
            if j % (self.canvas_size / 10) == 0:
                k = -self.canvas_size // 2 + j
                if k != 0:
                    self.create_line(-2 + y_position, k + self.canvas_size // 2, 2 + y_position, k + self.canvas_size // 2,
                                     width=0.25, fill='gray')

                    self.create_text(15 + y_position, k + self.canvas_size // 2,
                                     text=str(-k * (self.y_max - self.y_min) // self.canvas_size), fill='black',
                                     font=('Helvectica', '10'))

    def add_function(self, f, color="blue"):
        previous_point = None
        for x in range(self.canvas_size + 1):
            point = [x,  self.canvas_size - (self.canvas_size / (self.y_max - self.y_min) *
                                             (f((self.x_max - self.x_min) / self.canvas_size * x + self.x_min) - self.y_min))]
            if math.isnan(point[1]):
                previous_point = None
                continue

            if previous_point is not None:
                self.create_line(previous_point, point, fill=color)
            previous_point = point

    def add_point(self, x, y, color="black"):
        self.create_oval(
            x - 1,
            self.canvas_size * y + 1,
            x + 1,
            self.canvas_size * y - 1,
            fill=color)

    def rescale(self, f, x_min, x_max, y_min, y_max):
        self.x_max = x_max
        self.x_min = x_min
        self.y_min = y_min
        self.y_max = y_max

        self.delete(ALL)
        self.add_axis()
        self.add_function(default_parser.parse(f).calculate)


class MainFrame:

    def __init__(self):

        self.root = Tk()
        self.canvas_frame = Frame(self.root)
        self.handler_frame = Frame(self.root)
        self.displayer = Displayer(self.canvas_frame)
        self.canvas_frame.grid(row=0, column=0)
        self.handler_frame.grid(row=0, column=1)
        self.displayer.pack()

        # Entries and labels below
        self.x_min_entry = Entry(self.handler_frame, width=10)
        self.x_min_entry.insert(0, '-5')
        self.x_max_entry = Entry(self.handler_frame, width=10)
        self.x_max_entry.insert(0, '5')
        self.y_min_entry = Entry(self.handler_frame, width=10)
        self.y_min_entry.insert(0, '-25')
        self.y_max_entry = Entry(self.handler_frame, width=10)
        self.y_max_entry.insert(0, '25')
        self.function_entry = Entry(self.handler_frame, width=20)

        self.x_min_label = Label(self.handler_frame, text='x min')
        self.x_max_label = Label(self.handler_frame, text='x max')
        self.y_max_label = Label(self.handler_frame, text='y max')
        self.y_min_label = Label(self.handler_frame, text='y min')
        self.function_label = Label(self.handler_frame, text='function input')

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
        self.function_entry.bind('<Return>', self.on_click)


        # handling button
        self.rescale_but = Button(self.handler_frame, text='draw')
        self.rescale_but.bind('<Button-1>', self.on_click)
        self.rescale_but.grid(row=6, column=0, columnspan=2)

    def on_click(self, event):
        if self.function_entry.get() == '':
            return
        self.displayer.rescale(
            self.function_entry.get(),
            int(self.x_min_entry.get()),
            int(self.x_max_entry.get()),
            int(self.y_min_entry.get()),
            int(self.y_max_entry.get()))

    def start(self):
        self.root.mainloop()


if __name__ == '__main__':
    MainFrame().start()
