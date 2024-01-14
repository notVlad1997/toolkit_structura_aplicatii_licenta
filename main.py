import tkinter as tk

from ui.main_frame import MainFrame

root = tk.Tk()
root.minsize(width=1700, height=600)
myapp = MainFrame(master=root)
myapp.mainloop()
