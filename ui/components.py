from component_template import ComponentTemplate

"""
Class that stores all the elements that are going to be linked for the JSON UI.
"""
class WindowComponents:
    def __init__(self):
        self.components = []

    def add_component(self, component):
        self.components.append(component)
        if isinstance(component, ComponentTemplate):
            component.show_properties()

    def remove_component(self, component):
        self.components.remove(component)

    def modify_value(self, component, attribute_name, value):
        index = self.components.index(component)
        found_component = self.components[index]
        if issubclass(found_component, ComponentTemplate):
            found_component.modify_value(attribute_name, value)

    def save_json(self):
        for component in self.components:
            print(self.components.index(component))
            component.save_to_json(f"{self.components.index(component)}.json")