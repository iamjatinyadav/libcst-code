import libcst as cst

code = """
dic = {1:'jatin',}
"""

# Parse the code into a CST tree
module = cst.parse_module(code)

# Create a new assignment node for Name = Jatin
new_assignment = cst.Assign(
    targets=[cst.Name("Name")],
    value="Jatin"
)

# Find the position to insert the new assignment
for idx, node in enumerate(module.body):
    if isinstance(node, cst.Assign) and node.targets[0].value == "dic":
        # Insert the new assignment after the dictionary assignment
        module.body.insert(idx + 1, new_assignment)
        break

# Print the modified code
print(module.code)





