import tkinter as tk


class AutoAdjustCanvas(tk.Canvas):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.bind("<Configure>", self._on_configure)
        self.container = tk.Frame(self)  # Container pentru elementele canvas-ului
        self.create_window((0, 0), window=self.container, anchor="nw")  # Adaugă containerul în canvas
        self.container.bind("<Configure>", self._on_configure)

    def _on_configure(self, event):
        self.container.update_idletasks()
        self.configure(scrollregion=self.bbox("all"))
