class ComponentsTree:
    def __init__(self, value):
        self.value = value
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)

    def remove_child(self, child_node):
        self.children = [child for child in self.children
                         if child is not child_node]

    def traverse(self):
        for node in self.children:
            if isinstance(node, ComponentsTree):
                print("Traversing component:", node.value)
                node.traverse()
            else:
                print("Traversing layer:", node)
        print()
