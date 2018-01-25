from tkinter import *

class handler_frame(Frame):
    def __init__(self, root, displayer):
        super(handler_frame, self).__init__(root)
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
        self.rescale_but = Button(self, text='draw', command=self.on_click)
        self.rescale_but.grid(row=6, column=0, columnspan=2)

    def on_click(self):
        x_max = int(self.x_max_entry.get())
        x_min = int(self.x_min_entry.get())
        y_max = int(self.y_max_entry.get())
        y_min = int(self.y_min_entry.get())
        f = self.function_entry.get()
        self.displayer.rescale(f, x_min, x_max, y_min, y_max)
