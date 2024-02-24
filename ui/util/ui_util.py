import tkinter as tk

from ui.util.auto_canvas import AutoAdjustCanvas


def create_scrollbar_pane(display_pane):
    """
    Method that creates a new scrollbar pane and adds it to the display window_frame
    :param display_pane: The window_frame where the scrollbar pane will be placed
    :return: The Scrollbar pane
    """
    frame = tk.Frame(display_pane)
    frame.pack(fill=tk.BOTH, expand=tk.YES)
    scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas = AutoAdjustCanvas(frame, yscrollcommand=scrollbar.set)
    canvas.bind("<Configure>", lambda event: canvas.configure(
        scrollregion=canvas.bbox("all")))
    scrollbar.config(command=canvas.yview)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    display_pane.add(frame, minsize=200)
    return canvas.container
