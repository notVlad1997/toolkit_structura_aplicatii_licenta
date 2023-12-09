import tkinter
from tkinter import ttk
class App(tkinter.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.config(width=600, height=600)

        self.button = ttk.Button(self, text="Create button!")
        self.button.grid(column=0, row=0)
        self.pack()

        self.button.bind('<Button-1>', self.create_button)

    def create_button(self, event):
        self.button1 = ttk.Button(self, text="Created button!")
        self.button1.grid(column=0, row=1)
        self.pack()


root = tkinter.Tk()
root.minsize(width=600, height=600)
myapp = App(root)
myapp.mainloop()