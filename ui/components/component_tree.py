import json
import os

from component_template import ComponentTemplate
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

    # Modifică metoda save_to_json_recursive din ComponentsTree
    def save_to_json_recursive(self, base_folder="."):
        """
        Metodă recursivă pentru a salva componente într-o structură de directoare și fișiere JSON.

        :param base_folder: Folderul de bază în care să se creeze structura.
        """
        # Creează directorul pentru componenta curentă
        current_folder = os.path.join(base_folder, str(self.value.layer_name))
        os.makedirs(current_folder, exist_ok=True)

        # Salvează componenta într-un fișier JSON în directorul curent
        json_filename = os.path.join(base_folder, f"{self.value.layer_name}.json")
        self.value.save_to_json(json_filename)

        # Verifică dacă componenta este o altă instanță a clasei ComponentsTree și apelează recursiv
        for child in self.children:
            if isinstance(child, ComponentsTree):
                child.save_to_json_recursive(current_folder)
            elif isinstance(child, ComponentTemplate):
                # Salvează componente în fișierul JSON al componentei de bază
                child_json_filename = os.path.join(current_folder, f"{child.layer_name}.json")
                child.save_to_json(child_json_filename)