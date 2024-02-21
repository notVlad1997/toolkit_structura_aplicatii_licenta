from observers.observer import MasterObserver


class ComponentsTree(MasterObserver):
    def __init__(self, value):
        self.value = value
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)

    def remove_child(self, child_node):
        self.children = [child for child in self.children
                         if child is not child_node]

    def traverse(self):
        print("START:", self.value)
        for node in self.children:
            if isinstance(node, ComponentsTree):
                print("Traversing frame:", node.value)
                node.traverse()
                print("END", self.value)
            else:
                print("Traversing component:", node)

    def find_parent_of_child(self, parent, child):
        print(parent.children)
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

    def update(self, child):
        parent = self.find_parent_of_child(child=child, parent=self)
        if parent is not None:
            if parent.value.return_component() is not child.master:
                parent_frame = self.find_parent_of_frame(parent=self, frame=child.master)
                if parent_frame is not None:
                    parent.remove_child(child)
                    parent_frame.add_child(child)
                    #self.traverse()
                else:
                    print("CUM?")


