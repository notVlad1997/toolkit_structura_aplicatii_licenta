import importlib
import inspect
import json
import os

from component_template import ComponentTemplate


def transform_into_component(component_tree, component_frame, file_path, frames_list, window):
    """
    Method that opens a JSON file and adds it to the current window
    :return:
    """
    if file_path:
        try:
            with (open(file_path, 'r') as json_file):
                data = json.load(json_file)

                if "name" not in data or "category" not in data or "attributes" not in data:
                    print("No class with such information.")
                    return

                component_name = data["name"]
                category_name = data["category"]
                attributes_data = data["attributes"]

                folder_path = f"./component/{category_name}"

                if os.path.exists(folder_path) and os.path.isdir(folder_path):
                    python_files = [f for f in os.listdir(folder_path) if
                                    f.endswith(".py") and not f.startswith("__")]

                    for python_file in python_files:
                        module_name = os.path.splitext(python_file)[0]
                        template_file_path = os.path.join(folder_path, python_file)

                        try:
                            with open(template_file_path, 'r') as file:
                                module_content = file.read()

                            class_name = None
                            namespace = {}
                            exec(module_content, namespace)
                            for name, obj in namespace.items():
                                if inspect.isclass(obj) and issubclass(
                                        obj, ComponentTemplate) and obj != ComponentTemplate:
                                    instance = obj(frames=None)
                                    print(getattr(instance, 'name', None))
                                    if getattr(instance, 'name', None) == component_name:
                                        class_name = name
                                        break

                            if class_name:
                                create_component(category_name=category_name, module_name=module_name,
                                                 class_name=class_name, attributes_data=attributes_data,
                                                 component_name=component_name, component_tree=component_tree,
                                                 component_frame=component_frame, frames_list=frames_list, window=window)
                                break

                        except Exception as e:
                            print(f"Error on module loading: {module_name}, {e}")

                else:
                    print(f"Not existent JSON File")

        except Exception as e:
            print(f"JSON File Error: {e}")


def create_component(category_name, module_name, class_name, attributes_data, component_tree, component_frame,
                     component_name, frames_list, window):
    module = importlib.import_module(f"component.{category_name}.{module_name}")
    class_instance = getattr(module, class_name)
    print(class_instance)

    component_instance = class_instance(frames_list)

    for attribute_data in attributes_data:
        attribute_name = attribute_data.get("attribute_name", "")
        attribute_value = attribute_data.get("attribute_value", "")
        component_instance.modify_value(attribute_name=attribute_name,
                                        value=attribute_value)

    component_frame.add_component(component=component_instance, attribute_name=component_name, window=window, element=class_instance)
