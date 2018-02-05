from tkinter import *

from tkinter.messagebox import *

import numpy

import math

from function_parser.default import default_parser


class Displayer(Canvas):
    def __init__(self, root, x_min=-25, x_max=25, y_min=-25, y_max=25, canvas_size=500, border=50):
        self.root = root
        self.canvas_size = canvas_size
        self.border = border
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.functions_list = []
        super(Displayer, self).__init__(root, width=canvas_size + self.border, height=canvas_size + self.border,
                                        bg='white')

    def _update(self, color='blue'):
        x_axis_position = self.canvas_size // 2 + (self.y_max + self.y_min) / 2 * self.canvas_size / (
        self.y_max - self.y_min) + self.border // 2
        y_axis_position = self.canvas_size // 2 - (self.x_max + self.x_min) / 2 * self.canvas_size / (
        self.x_max - self.x_min) + self.border // 2

        if x_axis_position < self.border / 2:
            x_axis_position = self.border / 2
        if y_axis_position < self.border / 2:
            y_axis_position = self.border / 2

        self.y_axis = self.create_line(y_axis_position, self.canvas_size + self.border // 2,
                                       y_axis_position, self.border // 2,
                                       width=1, arrow=LAST, fill="gray")
        self.x_axis = self.create_line(self.border // 2, x_axis_position,
                                       self.canvas_size + self.border // 2, x_axis_position,
                                       width=1, arrow=LAST, fill="gray")
        # marking x_axis
        i = 0
        while True:
            n = 0

            while (self.x_max - self.x_min) * (10 ** n) < 10:
                n += 1

            k = (self.x_max - self.x_min) * (10 ** n) // (self.canvas_size // 50)

            a = k * (i + self.x_min * (10 ** n) // k)

            i += 1

            x = self.canvas_size * (
            1 - (1 - 1 / ((self.x_max - self.x_min) * (10 ** n)) * (a - self.x_min * (10 ** n))))

            if x > self.canvas_size:
                break

            self.create_line(x + self.border // 2, -2 + x_axis_position, x + self.border // 2, 2 + x_axis_position,
                             width=0.25, fill='gray')

            self.create_text(x + self.border // 2, 15 + x_axis_position,
                             text=str(a / (10 ** n)), fill='black',
                             font=('Helvectica', '10'))

        # marking y_axis
        i = 0
        while True:
            n = 0

            while (self.y_max - self.y_min) * (10 ** n) < 10:
                n += 1

            k = (self.y_max - self.y_min) * (10 ** n) // (self.canvas_size // 50)

            a = k * (i + self.y_min * (10 ** n) // k)

            i += 1

            if a == 0:
                continue

            y = self.canvas_size * (1 - 1 / ((self.y_max - self.y_min) * (10 ** n)) * (a - self.y_min * (10 ** n)))

            if y < 0:
                break

            self.create_line(-2 + y_axis_position, y + self.border // 2, 2 + y_axis_position, y + self.border // 2,
                             width=0.25, fill='gray')

            self.create_text(15 + y_axis_position, y + self.border // 2,
                             text=str(a / (10 ** n)), fill='black',
                             font=('Helvectica', '10'))

        if self.functions_list == []:
            return

        for f in self.functions_list:

            f = default_parser.parse(f).calculate
            pp = []
            prev_x = numpy.NaN
            prev_y = numpy.NaN

            for x in range(self.canvas_size + 1):
                point = (
                    x + self.border // 2,
                    self.canvas_size
                    - (self.canvas_size * (f((self.x_max - self.x_min) / self.canvas_size * x + self.x_min) - self.y_min)
                       / (self.y_max - self.y_min))
                    + self.border // 2)

                if math.isnan(point[1]):
                    if len(pp) > 0:
                        self.create_line(pp, fill=color)
                    pp = []
                    continue

                curr_y = round(point[1])
                curr_x = round(point[0])

                if curr_y == prev_y or curr_x == prev_x:
                    continue

                prev_y = curr_y
                prev_x = curr_x
                pp.append(point)

            self.create_line(pp, fill=color)

    def add_point(self, x, y, color="black"):
        self.create_oval(
            x - 1,
            self.canvas_size * y + 1,
            x + 1,
            self.canvas_size * y - 1,
            fill=color)

    def rescale(self, x_min, x_max, y_min, y_max):
        self.x_max = x_max
        self.x_min = x_min
        self.y_min = y_min
        self.y_max = y_max

        self.delete(ALL)
        self._update()

    def add_function(self, func):
        self.functions_list.append(func)
        self.delete(ALL)
        self._update()

    def delete_function(self, func):
        self.functions_list.pop(self.functions_list.index(func))
        self.delete(ALL)
        self._update()

    def clear(self):
        self.functions_list = []
        self.delete(ALL)
        self._update()


class MainFrame:
    def __init__(self):
        self.root = Tk()
        self.canvas_frame = Frame(self.root)
        self.handler_frame = Frame(self.root)
        self.displayer = Displayer(self.canvas_frame)
        self.canvas_frame.grid(row=0, column=0)
        self.handler_frame.grid(row=0, column=1)
        self.displayer.pack()

        self.limitations_frame = Frame(self.handler_frame, pady=50)
        self.limitations_frame.grid(row=3, column=0, columnspan=2)

        self.listbox_handler_frame = Frame(self.handler_frame)
        self.listbox_handler_frame.grid(row=2, column=0, columnspan=2)

        self.listbox_frame = Frame(self.handler_frame, pady=10)
        self.listbox_frame.grid(row=1, column=0, columnspan=2)

        # Entries and labels below
        self.x_min_entry = Entry(self.limitations_frame, width=10)
        self.x_min_entry.insert(0, '-25')
        self.x_min_entry.bind('<Return>', self.rescale)
        self.x_max_entry = Entry(self.limitations_frame, width=10)
        self.x_max_entry.insert(0, '25')
        self.x_max_entry.bind('<Return>', self.rescale)
        self.y_min_entry = Entry(self.limitations_frame, width=10)
        self.y_min_entry.insert(0, '-25')
        self.y_min_entry.bind('<Return>', self.rescale)
        self.y_max_entry = Entry(self.limitations_frame, width=10)
        self.y_max_entry.insert(0, '25')
        self.y_max_entry.bind('<Return>', self.rescale)
        self.function_entry = Entry(self.handler_frame, width=20)
        self.function_entry.bind('<Return>', self.on_click_add)

        self.x_min_label = Label(self.limitations_frame, text='x min')
        self.x_max_label = Label(self.limitations_frame, text='x max')
        self.y_max_label = Label(self.limitations_frame, text='y max')
        self.y_min_label = Label(self.limitations_frame, text='y min')

        self.function_entry.grid(row=0, column=0, columnspan=2)
        self.x_min_label.grid(row=0, column=0)
        self.x_max_label.grid(row=0, column=1)
        self.x_min_entry.grid(row=1, column=0)
        self.x_max_entry.grid(row=1, column=1)
        self.y_min_label.grid(row=2, column=0)
        self.y_max_label.grid(row=2, column=1)
        self.y_min_entry.grid(row=3, column=0)
        self.y_max_entry.grid(row=3, column=1)
        self.function_entry.insert(0, 'x')

        # Listbox
        self.functions_listbox = Listbox(self.listbox_frame)
        self.functions_listbox.pack()

        # handling buttons

        self.delete_but = Button(self.listbox_handler_frame, text='delete')
        self.delete_but.bind('<Button-1>', self.on_click_delete)
        self.delete_but.grid(row=0, column=0)

        self.change_but = Button(self.listbox_handler_frame, text='change')
        self.change_but.bind('<Button-1>', self.on_click_change)
        self.change_but.grid(row=0, column=1)

        self.clear_but = Button(self.listbox_handler_frame, text='clear')
        self.clear_but.bind('<Button-1>', self.on_click_clear)
        self.clear_but.grid(row=0, column=2)

    def rescale(self, event):

        try:
            int(self.x_min_entry.get())
            int(self.x_max_entry.get())
            int(self.y_min_entry.get())
            int(self.y_max_entry.get())
        except ValueError:
            showerror(title='Wrong input', message='Only numeric input is allowed')
            return

        if (int(self.x_max_entry.get()) - int(self.x_min_entry.get()) <= 0) or (
                int(self.y_max_entry.get()) - int(self.y_min_entry.get()) <= 0):
            showerror(title='Wrong input', message="It's impossible to draw graph in these limitations")

    def on_click_add(self, event):
        if self.function_entry.get() == '':
            return

        if ',' in self.function_entry.get():
            showwarning(title='Wrong format', message='Please, use "." instead of ","')
            return

        try:
            default_parser.parse(self.function_entry.get()).calculate
        except AttributeError:
            showerror(title='Parsing error', message='Wrong input format')
            return
        except OverflowError:
            showerror(title='Overflow error', message='Too long numbers')

        self.displayer.add_function(self.function_entry.get())
        self.functions_listbox.insert('end', self.function_entry.get())
        self.function_entry.delete(0, 'end')

    def on_click_delete(self, event):
        self.displayer.delete_function(self.functions_listbox.get('active'))
        self.functions_listbox.delete('active')

    def on_click_change(self, event):
        self.function_entry.delete(0, 'end')
        self.function_entry.insert(0, self.functions_listbox.get('active'))
        self.displayer.delete_function(self.functions_listbox.get('active'))
        self.functions_listbox.delete('active')

    def on_click_clear(self, event):
        self.functions_listbox.delete(0, 'end')
        self.displayer.clear()

    def start(self):
        self.root.mainloop()


if __name__ == '__main__':
    MainFrame().start()
