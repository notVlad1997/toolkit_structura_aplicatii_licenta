from observers.components.component_tree import ComponentsTree
from ui.util import ui_util


class ComponentFrame:
    def __init__(self, master, frames_list, component_tree, layer_frame):
        self.master = master
        self.component_pane = ui_util.create_scrollbar_pane(self.master)
        self.frames_list = frames_list
        self.component_tree = component_tree
        self.component_list = component_tree.create_component_list()
        self.layer_frame=layer_frame

    def destroy(self):
        for widget in self.component_pane.winfo_children():
            widget.destroy()

    def add_new_component(self, attribute_name, element):
        """
        Method that adds a new component on the window, it creates a new layer, and stores it.
        :param attribute_name: Name of the attribute, that it will be added to the UI.
        :param element: Name of the class, that it's going to be added as a new component.
        :return:
        """
        component = element(self.frames_list.get_component_list())
        self.component_list.add_component(component)
        component.register_observer(self.component_tree)

        self.layer_frame.create_new_layer(component=component, attribute_name=attribute_name)

        if str(element) == f"<class 'FrameTkinter'>":
            component_widget = component.return_component(self.master)
            self.frames_list.add_component(component_widget)
            self.component_tree.add_component(ComponentsTree(component))
        elif str(element) == f"<class 'ui.window_frame.layer_window.FrameWindowTK'>":
            self.component_tree = ComponentsTree(component)
        else:
            self.component_tree.add_component(component)