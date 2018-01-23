from tkinter import *


class Handler(Frame):
    def __init__(self, root):
        super(Handler, self).__init__(root)

        self.x_min_entry = Entry(self, width=10)
        self.x_max_entry = Entry(self, width=10)
        self.y_min_entry = Entry(self, width=10)
        self.y_max_entry = Entry(self, width=10)

        self.x_min_label = Label(self, text='x min')
        self.x_max_label = Label(self, text='x max')
        self.y_max_label = Label(self, text='y max')
        self.y_min_label = Label(self, text='y min')

        self.x_min_label.grid(row=0, column=0)
        self.x_max_label.grid(row=0, column=1)
        self.x_min_entry.grid(row=1, column=0)
        self.x_max_entry.grid(row=1, column=1)
        self.y_min_label.grid(row=2, column=0)
        self.y_max_label.grid(row=2, column=1)
        self.y_min_entry.grid(row=3, column=0)
        self.y_max_entry.grid(row=3, column=1)


if __name__ == '__main__':
    root = Tk()
    s = Handler(root)
    root.mainloop()
