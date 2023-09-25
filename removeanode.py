import libcst as cst

code = """
DATABASES = {
    'default': {
        'CONN_MAX_AGE': 0,
        'ENGINE': 'django.db.backends.',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',  # Or path to database file if using sqlite3.
        'USER': '',
        'PASSWORD': '',
        'HOST': '',  # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',  # Set to an empty string for default.
    },
    'main':"Abcd",
}

LST = [1,3,4,["5","6"]]

URL += ['demo', 'demo']
"""

# Parse the code into a CST tree
module = cst.parse_module(code)

# Find the LST assignment and remove it
for idx, node in enumerate(module.body):
    if isinstance(node, cst.Assign) and node.targets[0].target.value == 'LST':
        del module.body[idx]
        break

# Print the modified code
print(module.code)
