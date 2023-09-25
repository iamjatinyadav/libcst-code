import libcst as cst


def Merge(dict1, dict2):
    res = {**dict1, **dict2}
    return res
class ChangeInDict(cst.CSTTransformer):
    def leave_Assign(self, original_node, updated_node):
        if isinstance(updated_node.value, cst.Dict):
            # Create a new key-value pair
            instance = updated_node.value.elements
            new_pair = cst.parse_expression("{'demo': 'value'}")
            element = Merge(instance, new_pair)
            updated_node = updated_node.with_changes(name =element)
            print(updated_node)
            return updated_node


        return updated_node


# Your input code
code = """
dic = {'var1':'jatin',}
"""

# Parse the code into a CST
parsed_code = cst.parse_module(code)

# Apply the custom transformer
transformed_code = parsed_code.visit(ChangeInDict())

# Print the updated code
print(transformed_code.code)


