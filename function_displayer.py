from tkinter import *


class Displayer(Canvas):
    def __init__(self, root, x_min=-25, y_min=-25, x_max=25, y_max=25, x_scale=1, y_scale=1):
        super(Displayer, self).__init__(root, width=510, height=510, bg="white")
        self.create_line(250, 500, 250, 0, width=1, arrow=LAST)  # drawing y_axis
        self.create_line(0, 250, 500, 250, width=1, arrow=LAST)  # drawing x_axis
        self.x_max = x_max
        self.x_min = x_min
        self.y_min = y_min
        self.y_max = y_max
        # marking x_axis
        for i in range(501):
            if i % 50 == 0:
                k = -250 + i
                self.create_line(k+250, -2+250, k+250, 2+250,
                                         width=0.25, fill='black')

                self.create_text(k + 250, -10 + 250,
                                 text=str(k * y_scale * (self.x_max - self.x_min) // (x_scale * 500)), fill='black',
                                 font=('Helvectica', '10'))
        # marking y_axis
        for j in range(501):
            if j % 50 == 0:
                k = -250 + j
                if k != 0:
                    self.create_line(-2+250, k+250, 2+250, k+250,
                                             width=0.25, fill='black')

                    self.create_text(10+250, k+250,
                                             text=str(k * (self.y_max - self.y_min) // 500), fill='black',
                                             font=('Helvectica', '10'))

        self.scale_x = x_scale
        self.scale_y = y_scale

    def add_function(self, f, color="black"):
        previous_point = [0, 0]
        for x in range(self.x_min, self.x_max):
            try:
                point = [x * 500 // (self.x_max - self.x_min) + 250,
                         250 - (f(x / self.scale_x) * self.scale_y) * 500 // (self.y_max - self.y_min)]
                self.create_line(previous_point, point, fill=color)
                previous_point = point
            except:
                pass

    def add_point(self, x, y, color="black"):
        self.create_oval(
            self.scale_x * x - 1,
            500 - self.scale_y * y + 1,
            self.scale_x * x + 1,
            500 - self.scale_y * y - 1,
            fill=color)

    @staticmethod
    def rescale():
        x_min = Handler.x_min_entry.get()
        print(x_min)



class Handler(Frame):
    def __init__(self, root):
        super(Handler, self).__init__(root)

        # Entries and labels behind
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

        # handling button
        self.rescale_but = Button(self, text='rescale', command=Displayer.rescale)
        self.rescale_but.grid(row=4, column=0, columnspan=2)


