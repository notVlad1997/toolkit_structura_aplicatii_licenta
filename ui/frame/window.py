import tkinter as tk


class FrameWindow(tk.Frame):
    def __init__(self, master, width=0, height=0, title=""):
        super().__init__(master)
        self.master = master
        self.master.configure(borderwidth=5, relief="groove")

        self.config(width=width, height=height, borderwidth=5, relief="ridge")
        self.pack_propagate(False)

        self.title_button_bar = tk.Frame(self, height=25, relief="raised")
        self.title_button_bar.id = f"Title Bar"

        self.title_button_bar.pack(fill="x")
        self.title_button_bar.pack_propagate(False)

        self.min_button = tk.Button(self.title_button_bar, text="🗕", borderwidth=0, width=3, pady=0)
        self.max_button = tk.Button(self.title_button_bar, text="🗖", borderwidth=0, width=3, pady=0)
        self.close_button = tk.Button(self.title_button_bar, text="🗙", borderwidth=0, width=3, pady=0)

        # Bind events for hover and leave
        self.min_button.bind("<Enter>", lambda event, button=self.min_button: self.on_enter(event, button))
        self.min_button.bind("<Leave>", lambda event, button=self.min_button: self.on_leave(event, button))

        self.max_button.bind("<Enter>", lambda event, button=self.max_button: self.on_enter(event, button))
        self.max_button.bind("<Leave>", lambda event, button=self.max_button: self.on_leave(event, button))

        self.close_button.bind("<Enter>", lambda event, button=self.close_button: self.on_enter_exit(event, button))
        self.close_button.bind("<Leave>", lambda event, button=self.close_button: self.on_leave(event, button))

        self.close_button.pack(side="right")
        self.max_button.pack(side="right")
        self.min_button.pack(side="right")

        self.separator = tk.Frame(self, height=2, relief="sunken", background="gray")
        self.separator.pack(side="top", fill="x", pady=2)
        self.separator.id = f"Title Bar"

        self.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        self.place(relx=0.5, rely=0.5, anchor="center")

    def on_enter(self, event, button):
        button.configure(bg="gray90")

    def on_leave(self, event, button):
        button.configure(bg="SystemButtonFace")
        button.configure(foreground="black")

    def on_enter_exit(self, event, button):
        button.configure(bg="red")
        button.configure(foreground="white")

    def update_values(self, width=0, height=0, title=""):
        self.config(width=width, height=height)
        self.title_button_bar = tk.Frame(self, height=25, relief="raised")
        self.title_button_bar.pack(fill="x")
        self.title_button_bar.pack_propagate(False)

        self.min_button = tk.Button(self.title_button_bar, text="🗕", borderwidth=0, width=3, pady=0)
        self.max_button = tk.Button(self.title_button_bar, text="🗖", borderwidth=0, width=3, pady=0)
        self.close_button = tk.Button(self.title_button_bar, text="🗙", borderwidth=0, width=3, pady=0)

        # Bind events for hover and leave
        self.min_button.bind("<Enter>", lambda event, button=self.min_button: self.on_enter(event, button))
        self.min_button.bind("<Leave>", lambda event, button=self.min_button: self.on_leave(event, button))

        self.max_button.bind("<Enter>", lambda event, button=self.max_button: self.on_enter(event, button))
        self.max_button.bind("<Leave>", lambda event, button=self.max_button: self.on_leave(event, button))

        self.close_button.bind("<Enter>", lambda event, button=self.close_button: self.on_enter_exit(event, button))
        self.close_button.bind("<Leave>", lambda event, button=self.close_button: self.on_leave(event, button))

        self.close_button.pack(side="right")
        self.max_button.pack(side="right")
        self.min_button.pack(side="right")

        self.separator = tk.Frame(self, height=2, relief="sunken", background="gray")
        self.separator.pack(side="top", fill="x", pady=2)

        self.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        self.place(relx=0.5, rely=0.5, anchor="center")