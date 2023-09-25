# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import libcst as cst



# app = "demo"
#
# ASGI_APPLICATION = "voyagepro.asgi.application"



# See PyCharm help at https://www.jetbrains.com/help/pycharm/

# class TT(cst.CSTTransformer):
#     def __init__(self, tree, name):
#         self.tree = tree
#         self.name = name
#
#     def leave_Assign(self, original_node, updated_node):
#         if updated_node.targets[0].target.value == self.name:
#             elements = list(updated_node.value.elements)
#             new_value = cst.parse_expression(str({"heelo": "demo"}))
#             elements.append(new_value.elements[0])
#             value = updated_node.value.with_changes(elements=tuple(elements))
#             updated_node = updated_node.with_changes(value=value)
#         print(updated_node)
#         return updated_node

    # def leave_Assign(self, original_node, updated_node):
#     new_value = cst.Integer("10")  #
#     updated_node = updated_node.with_changes(value=new_value)
#     return updated_node  #  #  #

# def leave_FunctionDef(self, original_node, updated_node):  #
        # print(updated_node)
#     if updated_node.name.value == "print_hi":
#         new_name = cst.parse_expression("demo")
#         updated_node = updated_node.with_changes(name=new_name)
#     return updated_node


# class ChangeMiddleWare(cst.CSTTransformer):
#     def __init__(self, tree):
#         self.tree = tree
#
#     def leave_Assign(self, original_node, updated_node):
#         if updated_node.targets[0].target.value == "MIDDLEWARE":
#             element = list(updated_node.value.elements)
#             new_value = cst.Element(value="make_changes")
#             element.append(new_value)
#             updated_node = updated_node.with_changes(value=cst.List(elements=element))
#         return updated_node


# class ChangeInDict(cst.CSTTransformer):
#     def __init__(self, tree):
#         self.tree = tree
#
#     def leave_Assign(self, original_node, update_node):
#         if isinstance(update_node.targets[0], cst.Name) and isinstance(update_node.value, cst.Dict):
#             # Create a new dictionary entry
#             new_key = cst.SimpleString("2")
#             new_value = cst.SimpleString('"Yadav"')
#             new_pair = cst.DictElement(new_key, colon=cst.Colon(), value=new_value)
#
#             # Modify the existing dictionary with the new key-value pair
#             updated_dict = cst.Dict(original_node.value.elements + [new_pair])
#
#             # Update the assignment node with the modified dictionary
#             return update_node.with_changes(value=updated_dict)
#
#         return update_node



# class AddNewVariable(cst.CSTTransformer):
#     def __init__(self, tree):
#         self.tree = tree
#
#     def leave_add_
# x = 10
# parsed_cst = cst.parse_expression(f"foo{f'{x}'}")
# updated_cst = parsed_cst.visit(TT(parsed_cst))
# updated_cst = parsed_cst.visit(ChangeMiddleWare(parsed_cst))

code = """
dic = {1:'jatin',}
"""

parsed_code = cst.parse_expression(code)
# updated_cst = parsed_code.visit(ChangeInDict(parsed_code))
# print(updated_cst)
