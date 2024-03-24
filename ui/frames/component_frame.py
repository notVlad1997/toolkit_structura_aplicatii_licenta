from ui.components.component_tree import ComponentsTree
from ui.util import ui_util
import tkinter as tk


class ComponentFrame:
    def __init__(self, master, frames_list, component_tree, layer_frame):
        self.master = master
        self.component_pane = ui_util.create_scrollbar_pane(self.master)
        self.frames_list = frames_list
        self.component_tree = component_tree
        self.layer_frame = layer_frame
        self.current_component_window = None
        self.window = None
        self.current_component = None
        self.master.bind("<Motion>", self.on_motion)

    def destroy(self):
        for widget in self.component_pane.winfo_children():
            widget.destroy()

    def add_new_component(self, attribute_name, element, window, position=[0, 0]):
        """
        Method that adds a new component on the window, it creates a new layer, and stores it.
        :param attribute_name: Name of the attribute, that it will be added to the UI.
        :param element: Name of the class, that it's going to be added as a new component.
        :return:
        """
        component = element(self.frames_list, position=position)
        component.register_observer(self.component_tree)

        self.layer_frame.create_new_layer(component=component, attribute_name=attribute_name, window=window)
        if str(element) == f"<class 'FrameTkinter'>":
            self.component_tree.add_component(ComponentsTree(value=component))
        elif str(element) == f"<class 'component.Frame.windowFrame_Custom.FrameWindowTK'>":
            self.component_tree.value = component
        else:
            self.component_tree.add_component(component)

    def add_component(self, component, attribute_name, window, element):
        """
        Method that adds a new component on the window, it creates a new layer, and stores it.
        :param component:
        :param window:
        :param attribute_name: Name of the attribute, that it will be added to the UI.
        :param element: Name of the class, that it's going to be added as a new component.
        :return:
        """
        component.register_observer(self.component_tree)
        self.layer_frame.create_new_layer(component=component, attribute_name=attribute_name, window=window)
        if str(element) == f"<class 'FrameTkinter'>":
            self.component_tree.add_component(ComponentsTree(value=component))
        elif str(element) == f"<class 'component.Frame.windowFrame_Custom.FrameWindowTK'>":
            self.component_tree.value = component
        else:
            self.component_tree.add_component(component)

    def component_button(self, button_name, class_element, window=None):
        """
        Method that adds all the buttons with the functionality of getting all the components of the category.
        :param button_name: The name of the button that will be displayed.
        :param class_element: The class of the component
        :return:
        """
        button = tk.Button(self.component_pane, text=button_name,
                           command=lambda name=button_name: self.add_new_component(name, class_element, window=window))
        button.pack(side=tk.TOP)

        button.bind("<ButtonPress-1>",
                    lambda event, name=button_name, element=class_element,
                           win=window: self.on_button_press(event, element, win))

        button.bind("<ButtonRelease-1>",
                    lambda event, name=button_name:
                    self.on_button_release(event=event, button_name=name, class_element=class_element, window=window))
        button.pack(side=tk.TOP)
        button.bind("<Motion>", self.on_motion)

    def on_motion(self, event):
        if self.current_component and self.current_component_window:
            x_cursor_root, y_cursor_root = event.x_root, event.y_root
            x_window_root, y_window_root = self.window.winfo_rootx(), self.window.winfo_rooty()
            x_window = x_cursor_root - x_window_root
            y_window = y_cursor_root - y_window_root
            self.current_component_window.place(x=x_window, y=y_window)

    def on_button_press(self, event, element, window):
        x = event.x
        y = event.y
        component = element(self.frames_list)
        component.register_observer(self.component_tree)
        component_window = component.return_component(window=window)
        component_window.place(x=x, y=y)
        self.current_component = component
        self.current_component_window = component_window
        self.window = window

    def on_button_release(self, event, button_name, class_element, window):
        if self.current_component_window:
            self.current_component_window.destroy()
            self.current_component = None
            self.current_component_window = None
            x_cursor_root, y_cursor_root = event.x_root, event.y_root
            x_window_root, y_window_root = self.window.winfo_rootx(), self.window.winfo_rooty()
            x_window = x_cursor_root - x_window_root
            y_window = y_cursor_root - y_window_root
            self.add_new_component(attribute_name=button_name, element=class_element, window=window, position=[x_window, y_window])
