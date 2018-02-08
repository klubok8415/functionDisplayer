from tkinter import Entry


class EntryWithBackgroundText(Entry):
    def __init__(self, *args, **kwargs):
        self.background_text = kwargs.pop("background_text", "")
        super(EntryWithBackgroundText, self).__init__(*args, **kwargs)
        self.insert(0, self.background_text)
        self.bind('<FocusOut>', self.change_exit)
        self.bind('<FocusIn>', self.change_enter)

    def change_exit(self, event):
        if self.get():
            return
        self.delete(0, 'end')
        self.insert(0, self.background_text)
        self.config(foreground='grey')

    def change_enter(self, event):
        if self.get() == self.background_text:
            self.delete(0, 'end')
        self.config(foreground='black')
