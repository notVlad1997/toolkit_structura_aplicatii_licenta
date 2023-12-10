import tkinter as tk
from tkinter import ttk

class App(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.main_pane = None
        self.master = master
        self.config(width=600, height=600)
        self.create_widgets()
        self.pack(fill=tk.BOTH, expand=True)
        self.rows = 1

        # Bind the Configure event to the update_scroll_region method
        self.main_pane.bind("<Configure>", self.update_scroll_region)

    def create_widgets(self):
        self.main_pane = tk.PanedWindow(self, orient=tk.HORIZONTAL, sashrelief=tk.SUNKEN, sashwidth=7)
        self.main_pane.pack(fill=tk.BOTH, expand=True)

        middle_pane = tk.PanedWindow(self.main_pane, orient=tk.VERTICAL, sashrelief=tk.RAISED, sashwidth=7)
        self.main_pane.add(middle_pane, minsize=100)

        top_middle_pane = tk.Canvas(middle_pane, bg='green', width=500, height=500)
        scrollbar = tk.Scrollbar(top_middle_pane, command=top_middle_pane.yview)
        top_middle_pane.config(yscrollcommand=scrollbar.set, scrollregion=(0, 0, 0, 2000))
        top_middle_pane.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        bottom_middle_pane = tk.Frame(middle_pane, bg='blue')
        middle_pane.add(top_middle_pane)
        middle_pane.add(bottom_middle_pane)

        self.create_buttons(bottom_middle_pane, top_middle_pane)

        right_pane = tk.Frame(self.main_pane, bg='yellow')
        self.main_pane.add(right_pane, minsize=100)

    def create_buttons(self, window, window1):
        button = ttk.Button(window, text="Create button!", command=lambda: self.create_button(window1))
        button.pack(pady=10, padx=10)

    def create_button(self, canvas):
        button1 = ttk.Button(canvas, text=f"Created button{self.rows}!")
        # Add the button to the canvas
        canvas.create_window((20, 10 + (self.rows - 1) * 30), window=button1, anchor="nw")

        # Update the scroll region based on the new button
        canvas.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        self.rows += 1

    def update_scroll_region(self, event):
        # Update the scroll region of the canvas when the PanedWindow is configured
        self.main_pane.children["!canvas"].config(scrollregion=self.main_pane.children["!canvas"].bbox("all"))

root = tk.Tk()
root.minsize(width=600, height=600)
myapp = App(master=root)
myapp.mainloop()