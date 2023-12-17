import tkinter as tk


class FrameWindow(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.master.configure(borderwidth=5, relief="ridge")

        self.interior_frame = tk.Frame(self.master, width=300, height=200, borderwidth=5, relief="ridge")
        self.interior_frame.pack_propagate(False)

        self.interior_frame.place(relx=0.5, rely=0.5, anchor="center")

        # self.interior_canvas = tk.Canvas(self.interior_frame, width=500, height=500)
        # self.interior_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.title_button_bar = tk.Frame(self.interior_frame, height=15, relief="raised")
        self.title_button_bar.pack(fill="x")
        self.title_button_bar.pack_propagate(False)

        self.min_button = tk.Button(self.title_button_bar, text="-")
        self.max_button = tk.Button(self.title_button_bar, text="□")
        self.close_button = tk.Button(self.title_button_bar, text="x")

        self.min_button.pack(side="right")
        self.max_button.pack(side="right")
        self.close_button.pack(side="right")

        self.separator = tk.Frame(self.interior_frame, height=2, relief="sunken",background="gray")
        self.separator.pack(side="top", fill="x", pady=2)

        self.rows=0

    def add(self, element):
        self.interior_canvas.create_window((20, 10 + (self.rows - 1) * 30), window=element, anchor="nw")

        self.interior_canvas.update_idletasks()
        self.interior_canvas.config(scrollregion=self.interior_canvas.bbox("all"))

        self.rows += 1
