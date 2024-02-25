from observers.observer import Observer
from observers.subject import Subject


class ComponentsTree(Observer, Subject):
    def __init__(self, value=None):
        super().__init__()
        self.value = value
        self.children = []

    def add_component(self, child_node):
        self.children.append(child_node)
        self.notify_observers(self)

    def remove_component(self, child_node):
        self.children = [child for child in self.children
                         if child is not child_node]

    def traverse(self, tabs=0):
        for i in range(0, tabs):
            print("  ", end="")
        print("START:", self.value)
        for node in self.children:
            if isinstance(node, ComponentsTree):
                for i in range(0, tabs):
                    print("  ", end="")
                print("Traversing frames:", node.value)
                node.traverse(tabs=tabs+1)
            else:
                for i in range(0, tabs):
                    print("  ", end="")
                print("Traversing component:", node)
        for i in range(0, tabs):
            print("  ", end="")
        print("END", self.value)

    def find_parent_of_child(self, parent, child):
        for children in parent.children:
            if isinstance(children, ComponentsTree):
                parent_found = children.find_parent_of_child(parent=children, child=child)
                if parent_found is not None:
                    return parent_found
            elif children == child:
                return parent
        return None

    def find_parent_of_frame(self, parent, frame):
        for children in parent.children:
            if isinstance(children, ComponentsTree):
                if children.value.return_component() == frame:
                    return children
                else:
                    parent_found = children.find_parent_of_frame(parent=children, frame=frame)
                    if parent_found is not None:
                        return parent

    def update(self, value):
        parent = self.find_parent_of_child(child=value, parent=self)
        if parent is not None:
            if parent.value.return_component() is not value.master:
                parent_frame = self.find_parent_of_frame(parent=self, frame=value.master)
                if parent_frame is not None:
                    parent.remove_component(value)
                    parent_frame.add_component(value)
                    self.notify_observers(self)
                else:
                    print("CUM?")

    def create_component_list(self):
        component_list = [self.value]
        for child in self.children:
            if isinstance(child, ComponentsTree):
                component_list += child.create_component_list()
            else:
                component_list.append(child)

        return component_list