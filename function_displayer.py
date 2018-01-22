from tkinter import *


class Displayer(Canvas):
    def __init__(self, root, scale_x=10, scale_y=1, canvas_size=500):
        self.inc = canvas_size // 2
        super(Displayer, self).__init__(root, width=500, height=500, bg="white")
        self.create_line(250, 500, 250, 0, width=1, arrow=LAST)  # drawing y_axis
        self.create_line(0, 250, 500, 250, width=1, arrow=LAST)  # drawing x_axis

        # marking x_axis
        for i in range(501):
            if i % 50 == 0:
                k = -250 + i
                self.create_line(k+250, -2+250, k+250, 2+250,
                                         width=0.25, fill='black')

                self.create_text(k+250, -10+250,
                                         text=str(k*scale_y//scale_x), fill='black',
                                         font=('Helvectica', '10'))
        # marking y_axis
        for j in range(501):
            if j % 50 == 0:
                k = -250 + j
                if k != 0:
                    self.create_line(-2+250, k+250, 2+250, k+250,
                                             width=0.25, fill='black')

                    self.create_text(10+250, k+250,
                                             text=str(k), fill='black',
                                             font=('Helvectica', '10'))

        self.scale_x = scale_x
        self.scale_y = scale_y

    def add_function(self, f, color="black"):
        previous_point = [0, 0]
        for x in range(-250, 251):
            try:
                point = [x+250, 250 - f(x / self.scale_x) * self.scale_y]
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

