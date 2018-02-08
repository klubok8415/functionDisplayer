from tkinter import *

from tkinter.messagebox import *

from expressions.displayer.custom_canvas import Displayer
from expressions.displayer.custom_entry import EntryWithBackgroundText
from expressions.displayer.exceptions import TooBigNumbersError, WrongFunctionStringError


class MainFrame:
    def __init__(self):
        self.root = Tk()
        self.canvas_frame = Frame(self.root)
        self.handler_frame = Frame(self.root, padx=20)

        self.displayer = Displayer(self.canvas_frame)

        self.canvas_frame.pack(side=LEFT, fill=X, expand=1)
        self.handler_frame.pack(side=LEFT, fill=X)

        self.displayer.pack()

        # menu bar
        self.menubar = Menu(self.root)

        self.mathmenu = Menu(self.menubar)
        self.mathmenu.add_command(label='Add derivative for active function', command=self.on_click_add_derivative)
        self.menubar.add_cascade(label='Math', menu=self.mathmenu)

        self.helpmenu = Menu(self.menubar)
        self.helpmenu.add_command(label='Help', command=MainFrame.help_message)
        self.menubar.add_cascade(label='Help', menu=self.helpmenu)

        self.root.config(menu=self.menubar)

        self.limitations_frame = Frame(self.handler_frame, pady=50)
        self.limitations_frame.grid(row=3, column=0, columnspan=2)

        self.listbox_handler_frame = Frame(self.handler_frame)
        self.listbox_handler_frame.grid(row=2, column=0, columnspan=2)

        self.listbox_frame = Frame(self.handler_frame, pady=10)
        self.listbox_frame.grid(row=1, column=0, columnspan=2)

        # Entries and labels below
        self.function_entry = EntryWithBackgroundText(
            self.handler_frame,
            width=27,
            foreground='grey',
            font=('Consolas', 10),
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

        self.function_entry.grid(row=0, column=0, columnspan=2)

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

        self.root.update()
        self.root.minsize(self.root.winfo_width(), self.root.winfo_height())
        self.root.minsize(self.root.winfo_width(), self.root.winfo_height())
        self.size_x_prev = self.root.winfo_width()
        self.size_y_prev = self.root.winfo_height()
        self.root.bind('<Configure>', self.root_resize)

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
        self.displayer.add_derivative(self.functions_listbox.index('active'))
        self.functions_listbox.insert('end', '('+self.functions_listbox.get('active')+")'")
        self._try_update_graph()

    def on_click_add_function(self, event):
        if self.function_entry.get() == '':
            return

        try:
            self.displayer.add_function(self.function_entry.get())
        except WrongFunctionStringError:
            showerror(title='Parsing error', message='Wrong input format')
            return

        self.functions_listbox.insert('end', self.function_entry.get())
        self.function_entry.delete(0, 'end')
        self.mathmenu.entryconfig('Add derivative for active function', state='normal')
        self._try_update_graph()

    def on_click_delete(self, event):
        self.displayer.delete_function(self.functions_listbox.index('active'))
        self.functions_listbox.delete('active')
        if self.functions_listbox.index('end') == 0:
            self.mathmenu.entryconfig('Add derivative for active function', state='disabled')

    def on_click_change(self, event):
        if self.functions_listbox.size() < 1:
            return

        if self.functions_listbox.get('active')[-1] == "'":
            showwarning(title='Warning', message='Impossible to change derivative')
            return
        # deleting background text in function entry
        self.function_entry.delete(0, 'end')

        self.function_entry.insert(0, self.functions_listbox.get('active'))
        self.displayer.delete_function(self.functions_listbox.index('active'))
        self.functions_listbox.delete('active')

    def on_click_clear(self, event):
        self.functions_listbox.delete(0, 'end')
        self.displayer.clear()
        self.mathmenu.entryconfig('Add derivative for active function', state='disabled')

    def start(self):
        self.root.mainloop()

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
