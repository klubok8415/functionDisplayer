from tkinter import *

from tkinter.messagebox import *

import numpy

import math

from function_parser.default import default_parser


class Displayer(Canvas):
    def __init__(self, root, x_min=-25, x_max=25, y_min=-25, y_max=25, size_x=500, size_y=500, border=50):
        self.root = root
        self.size_x = size_x
        self.size_y = size_y
        self.border = border
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.functions_list = []
        super(Displayer, self).__init__(self.root, width=self.size_x + self.border, height=self.size_y + self.border,
                                        bg='white')

    def update_graph(self, color='blue'):
        x_axis_position = self.size_y // 2 + (self.y_max + self.y_min) / 2 * self.size_y / (
            self.y_max - self.y_min) + self.border // 2
        y_axis_position = self.size_x // 2 - (self.x_max + self.x_min) / 2 * self.size_x / (
            self.x_max - self.x_min) + self.border // 2

        if x_axis_position < self.border / 2:
            x_axis_position = self.border / 2
        if y_axis_position < self.border / 2:
            y_axis_position = self.border / 2

        if self.functions_list:

            for f in self.functions_list:
                f = default_parser.parse(f).calculate
                pp = []
                prev_x = numpy.NaN
                prev_y = numpy.NaN

                for x in range(self.size_x + 1):
                    point = (
                        x + self.border // 2,
                        self.size_y
                        - (self.size_y * (f((self.x_max - self.x_min) / self.size_x * x + self.x_min) - self.y_min)
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

                if len(pp) > 0:
                    self.create_line(pp, fill=color)

        self.y_axis = self.create_line(y_axis_position, self.size_y + self.border // 2,
                                       y_axis_position, self.border // 2,
                                       width=1, arrow=LAST, fill="gray")
        self.x_axis = self.create_line(self.border // 2, x_axis_position,
                                       self.size_x + self.border // 2, x_axis_position,
                                       width=1, arrow=LAST, fill="gray")
        # marking x_axis
        i = 0
        while True:
            n = 0

            while (self.x_max - self.x_min) * (10 ** n) < self.size_x // 50:
                n += 1

            k = (self.x_max - self.x_min) * (10 ** n) // (self.size_x // 50)

            a = k * (i + self.x_min * (10 ** n) // k)

            i += 1

            x = self.size_x * (
            1 - (1 - 1 / ((self.x_max - self.x_min) * (10 ** n)) * (a - self.x_min * (10 ** n))))

            if x > self.size_x:
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

            while (self.y_max - self.y_min) * (10 ** n) < self.size_y // 50:
                n += 1

            k = (self.y_max - self.y_min) * (10 ** n) // (self.size_y // 50)

            a = k * (i + self.y_min * (10 ** n) // k)

            i += 1

            if a == 0:
                continue

            y = self.size_y * (1 - 1 / ((self.y_max - self.y_min) * (10 ** n)) * (a - self.y_min * (10 ** n)))

            if y < 0:
                break

            self.create_line(-2 + y_axis_position, y + self.border // 2, 2 + y_axis_position, y + self.border // 2,
                             width=0.25, fill='gray')

            self.create_text(15 + y_axis_position, y + self.border // 2,
                             text=str(a / (10 ** n)), fill='black',
                             font=('Helvectica', '10'))


    def add_point(self, x, y, color="black"):
        self.create_oval(
            x - 1,
            self.size_y * y + 1,
            x + 1,
            self.size_y * y - 1,
            fill=color)

    def rescale(self, x_min, x_max, y_min, y_max):
        self.x_max = x_max
        self.x_min = x_min
        self.y_min = y_min
        self.y_max = y_max

        self.delete(ALL)
        self.update_graph()

    def add_function(self, func):
        self.functions_list.append(func)
        self.delete(ALL)
        self.update_graph()

    def delete_function(self, func):
        self.functions_list.pop(self.functions_list.index(func))
        self.delete(ALL)
        self.update_graph()

    def clear(self):
        self.functions_list = []
        self.delete(ALL)
        self.update_graph()


class MainFrame:
    def __init__(self):
        self.root = Tk()
        self.canvas_frame = Frame(self.root)
        self.handler_frame = Frame(self.root, padx=20)
        self.displayer = Displayer(self.canvas_frame)
        self.canvas_frame.pack(side=LEFT, fill=X, expand=1)
        self.handler_frame.pack(side=LEFT, fill=X)
        self.displayer.pack()
        self.root.update()

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

        self.function_entry = Entry(self.handler_frame, width=20, foreground='grey')
        self.function_entry.bind('<Return>', self.on_click_add)
        self.function_entry.insert(0, 'type your function hear')
        self.function_entry.bind('<FocusOut>', self.change_entry_exit)
        self.function_entry.bind('<FocusIn>', self.change_entry_enter)

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

        self.root.update()
        self.root.minsize(self.root.winfo_width(), self.root.winfo_height())
        self.size_x_prev = self.root.winfo_width()
        self.size_y_prev = self.root.winfo_height()
        self.root.bind('<Configure>', self.root_resize)

    def root_resize(self, event):
        delta_x = self.root.winfo_width() - self.size_x_prev
        delta_y = self.root.winfo_height() - self.size_y_prev
        if delta_x != 0 or delta_y != 0:
            self.displayer.size_x += delta_x
            self.displayer.size_y += delta_y
            self.displayer.config(width=self.displayer.size_x + self.displayer.border,
                                  height=self.displayer.size_y + self.displayer.border)
            self.displayer.delete(ALL)
            self.displayer.update_graph()
            self.size_x_prev += delta_x
            self.size_y_prev += delta_y

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
            return

        self.displayer.rescale(
            int(self.x_min_entry.get()),
            int(self.x_max_entry.get()),
            int(self.y_min_entry.get()),
            int(self.y_max_entry.get())
        )

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
        self.change_entry_enter(1)
        self.function_entry.delete(0, 'end')
        self.function_entry.insert(0, self.functions_listbox.get('active'))
        self.displayer.delete_function(self.functions_listbox.get('active'))
        self.functions_listbox.delete('active')

    def on_click_clear(self, event):
        self.functions_listbox.delete(0, 'end')
        self.displayer.clear()

    # methods below create background text in function entrybox

    def change_entry_exit(self, event):
        if self.function_entry.get():
            return
        self.function_entry.delete(0, 'end')
        self.function_entry.insert(0, 'type your function hear')
        self.function_entry.config(foreground='grey')

    def change_entry_enter(self, event):
        if self.function_entry.get() == 'type your function hear':
            self.function_entry.delete(0, 'end')
        self.function_entry.config(foreground='black')

    def start(self):
        self.root.mainloop()


if __name__ == '__main__':
    MainFrame().start()
