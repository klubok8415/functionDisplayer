from tkinter import *
from tkinter.messagebox import *

from displayer.custom_canvas import Displayer
from displayer.custom_entry import EntryWithBackgroundText

from displayer.exceptions import TooBigNumbersError
from expressions.core import DifferentiationError
from function_parser.default import default_parser

import signal


class MainFrame:
    def __init__(self):
        self.root = Tk()
        self.TopFrame = Frame(self.root)
        self.canvas_frame = Frame(self.TopFrame)
        self.handler_frame = Frame(self.TopFrame, padx=20)

        self.displayer = Displayer(self.canvas_frame)
        self.functions = []
        self.parser = default_parser

        self.TopFrame.pack(side=TOP, fill=Y)
        self.canvas_frame.pack(side=LEFT, fill=X, expand=1)
        self.handler_frame.pack(side=LEFT, fill=X)

        self.displayer.pack()

        # menu bar
        self.menubar = Menu(self.root)

        self.mathmenu = Menu(self.menubar)
        self.mathmenu.add_command(label='Add derivative for active function', command=self.on_click_add_derivative)
        self.menubar.add_cascade(label='Math', menu=self.mathmenu)

        self.displayer_menu = Menu(self.menubar)
        self.displayer_menu.add_command(label='Center origin', command=self.recenter_canvas)
        self.menubar.add_cascade(label='Displaying options', menu=self.displayer_menu)

        self.helpmenu = Menu(self.menubar)
        self.helpmenu.add_command(label='Help', command=self.help_message)
        self.menubar.add_cascade(label='Help', menu=self.helpmenu)

        self.root.config(menu=self.menubar)

        self.limitations_frame = Frame(self.handler_frame)
        self.limitations_frame.grid(row=4, column=0, columnspan=2)

        self.listbox_handler_frame = Frame(self.handler_frame)
        self.listbox_handler_frame.grid(row=2, column=0, columnspan=2)

        self.listbox_frame = Frame(self.handler_frame, pady=10)
        self.listbox_frame.grid(row=1, column=0, columnspan=2)

        # Entries and labels below
        self.function_label = Label(
            self.handler_frame,
            text='y =',
            font=('Consolas', 14))

        self.function_entry = EntryWithBackgroundText(
            self.handler_frame,
            width=18,
            foreground='grey',
            font=('Consolas', 14),
            background_text='Your function')

        self.function_entry.bind('<Return>', self.on_click_add_function)

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

        self.x_min_label = Label(self.limitations_frame, text='x min')
        self.x_max_label = Label(self.limitations_frame, text='x max')
        self.y_max_label = Label(self.limitations_frame, text='y max')
        self.y_min_label = Label(self.limitations_frame, text='y min')

        self.x_min_label.grid(row=0, column=0)
        self.x_max_label.grid(row=0, column=1)
        self.x_min_entry.grid(row=1, column=0)
        self.x_max_entry.grid(row=1, column=1)
        self.y_min_label.grid(row=2, column=0)
        self.y_max_label.grid(row=2, column=1)
        self.y_min_entry.grid(row=3, column=0)
        self.y_max_entry.grid(row=3, column=1)

        self.function_label.grid(row=0, column=0)
        self.function_entry.grid(row=0, column=1)

        # Listbox
        self.listbox_scrollbar = Scrollbar(self.listbox_frame, orient=VERTICAL)
        self.functions_listbox = Listbox(self.listbox_frame, yscrollcommand=self.listbox_scrollbar.set)
        self.listbox_scrollbar.config(command=self.functions_listbox.yview)
        self.listbox_scrollbar.pack(side=RIGHT, fill=Y)
        self.functions_listbox.pack(side=LEFT, fill=BOTH)

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

        # status bar
        self.statusbar = Label(self.root, bd=1, relief=SUNKEN, anchor=W)
        self.statusbar.pack(side=BOTTOM, fill=X)

        self.root.update()
        self.root.minsize(self.root.winfo_width(), self.root.winfo_height())
        self.root.minsize(self.root.winfo_width(), self.root.winfo_height())
        self.size_x_prev = self.root.winfo_width()
        self.size_y_prev = self.root.winfo_height()
        self.root.bind('<Configure>', self.root_resize)
        self.root.bind('<Motion>', self.canvas_on_motion)
        self.root.bind('<Button-1>', self.canvas_on_click)
        self.root.bind('<ButtonRelease-1>', self.canvas_on_release)
        self.root.bind('<MouseWheel>', self.check_limitations)

        # Hot keys
        self.root.bind('<Delete>', self.on_click_delete)
        self.root.bind('<F2>', self.on_click_change)
        self.functions_listbox.bind('<Return>', self.on_click_add_derivative)

    def _try_update_graph(self):
        try:
            self.displayer.update_graph()
        except TooBigNumbersError as e:
            showinfo(
                title='Overflow',
                message=str.format(
                    'Function {0} can not be calculated. It has been safely removed from list.',
                    self.functions_listbox.get(e.function_index)
                )
            )
            self.functions_listbox.delete(e.function_index)
            self._try_update_graph()

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
            coords = [
                float(self.x_min_entry.get()),
                float(self.x_max_entry.get()),
                float(self.y_min_entry.get()),
                float(self.y_max_entry.get()),
            ]
        except ValueError:
            showerror(title='Wrong input', message='Only float input is allowed')
            return

        self.displayer.rescale(*coords)

        if coords[1] - coords[0] <= 0 or coords[3] - coords[2] <= 0:
            showerror(title='Wrong input', message="It's impossible to draw graph in these limitations")
            return
        self._try_update_graph()

    def on_click_add_derivative(self):
        try:
            f = self.functions[self.functions_listbox.index('active')].differentiate()

        except DifferentiationError:
            showinfo(title='Differentiating problem', message='Function can not be differentiated')
            return

        self.displayer.add_function(f.calculate)
        self.functions.append(f)

        parent_function_text = self.functions_listbox.get('active')
        self.functions_listbox.insert(
            'end',
            str.format(
                "{0}'" if parent_function_text[-1] == "'" else "({0})'",
                parent_function_text))
        self._try_update_graph()

    def on_click_add_function(self, event):
        if self.function_entry.get() == '':
            return

        signal.signal(signal.SIGALRM, self.timeout)
        signal.alarm(5)
        try:
            f = self.parser.parse(self.function_entry.get())
        except TimeoutError:
            signal.alarm(0)
            showerror(title='Input error', message='Function cannot be displayed')
            return

        if f is None:
            showerror(title='Parsing error', message='Wrong input format')
            return
        self.displayer.add_function(f.calculate)
        self.functions.append(f)

        self.functions_listbox.insert('end', self.function_entry.get())
        self.function_entry.delete(0, 'end')
        self.mathmenu.entryconfig('Add derivative for active function', state='normal')
        self._try_update_graph()

    def on_click_delete(self, event):
        if self.functions_listbox.index('end') == 0:
            return
        self.displayer.delete_function(self.functions_listbox.index('active'))
        self.functions.pop(self.functions_listbox.index('active'))
        self.functions_listbox.delete('active')
        if self.functions_listbox.index('end') == 0:
            self.mathmenu.entryconfig('Add derivative for active function', state='disabled')
        self._try_update_graph()

    def on_click_change(self, event):
        if self.functions_listbox.size() < 1:
            return

        if self.functions_listbox.get('active').endswith("'"):
            showwarning(title='Warning', message='Impossible to change derivative')
            return
        # deleting background text in function entry
        self.function_entry.change_enter(1)

        self.function_entry.insert(0, self.functions_listbox.get('active'))
        self.displayer.delete_function(self.functions_listbox.index('active'))
        self.functions.pop(self.functions_listbox.index('active'))
        self.functions_listbox.delete('active')
        self._try_update_graph()

    def on_click_clear(self, event):
        self.functions_listbox.delete(0, 'end')
        self.displayer.clear()
        self.functions.clear()
        self.mathmenu.entryconfig('Add derivative for active function', state='disabled')

    def canvas_on_click(self, event):
        self.canvas_motion = True

    def canvas_on_release(self, event):
        self.canvas_motion = False

    def canvas_on_motion(self, event):
        self.check_limitations(1)
        try:
            self.statusbar.config(
                text='y=' + self.functions_listbox.get(
                    int(self.displayer.gettags(
                        self.displayer.find_overlapping(
                            event.x - 10,
                            event.y - 10,
                            event.x + 10,
                            event.y + 10
                        )[0])[0])))
        except (IndexError, ValueError):
            self.statusbar.config(text='')

    def check_limitations(self, event):
        if self.displayer.x_min != float(self.x_min_entry.get()) \
                or self.displayer.y_min != float(self.y_min_entry.get()) \
                or self.displayer.x_max != float(self.x_max_entry.get()) \
                or self.displayer.y_max != float(self.y_max_entry.get()):

            self.x_min_entry.delete(0, 'end')
            self.y_min_entry.delete(0, 'end')
            self.x_max_entry.delete(0, 'end')
            self.y_max_entry.delete(0, 'end')

            self.x_min_entry.insert(0, str(round(self.displayer.x_min, 1)))
            self.y_min_entry.insert(0, str(round(self.displayer.y_min, 1)))
            self.x_max_entry.insert(0, str(round(self.displayer.x_max, 1)))
            self.y_max_entry.insert(0, str(round(self.displayer.y_max, 1)))

    def recenter_canvas(self):
        x_max = (self.displayer.x_max - self.displayer.x_min) / 2
        x_min = - (self.displayer.x_max - self.displayer.x_min) / 2
        y_max = (self.displayer.y_max - self.displayer.y_min) / 2
        y_min = - (self.displayer.y_max - self.displayer.y_min) / 2
        self.displayer.x_max = x_max
        self.displayer.x_min = x_min
        self.displayer.y_max = y_max
        self.displayer.y_min = y_min
        self.check_limitations(1)
        self._try_update_graph()

    def start(self):
        self._try_update_graph()
        self.root.mainloop()

    @staticmethod
    def timeout(*args):
        raise TimeoutError
        return

    @staticmethod
    def help_message():
        showinfo(
            title='Help',
            message='Available operators: '
                    '\n "+" - Addition  '
                    '\n "-" - Deduction '
                    '\n "*" - Multiplication'
                    '\n "/" - Division'
                    '\n "ˆ" - Power'
                    '\n "sin(argument)" - Sinus'
                    '\n "cos(argument)" - Cosine'
                    '\n "tan(argument)" - Tangent'
                    '\n "cot(argument)" - Cotangent'
                    '\n "arcsin(argument)" - Arcsine'
                    '\n "arccos(argument)" - Arccosine'
                    '\n "acrtan(argument)" - Arctangent'
                    '\n "arccot(argument)" - Arccotangent'
                    '\n "log(argument, base)" - Logarithm'
                    '\n "sqrt(argument)" - Square root'
                    '\n'
                    '\n Other designations:'
                    '\n "()" - Brackets'
                    '\n "||" - Modulus'
                    '\n "[]" - Floor'
                    '\n "{}" - Truncate')


if __name__ == '__main__':
    MainFrame().start()
