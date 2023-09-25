import ast

import libcst as cst



# class ChangeInVariableValue(cst.CSTTransformer):
#
#     def __init__(self, tree):
#         self.tree = tree
#
#
#     def leave_Assign(self, original_node, updated_node):
#
#         # if updated_node.targets[0].target.value == "DEBUG":
#         #     # firstWay
#         # #     new_assignment = cst.Assign(targets=[cst.AssignTarget(target=cst.Name("DEBUG"))],
#         # #                                 value=cst.Name("True")  # Change the value to "True"
#         # #     )
#         #     # second way
#         #     new_value = cst.Name("True")
#         #     # new_value = cst.Integer(2)
#         #     updated_node = updated_node.with_changes(value = new_value)
#
#         if updated_node.targets[0].target.value == "SITE":
#             new_value = cst.Integer("2")  # Change the value to "2"
#             updated_node = updated_node.with_changes(value=new_value)
#
#         return updated_node


class ChangeInInstalledApps(cst.CSTTransformer):

    def __init__(self, tree, name):
        self.tree = tree
        self.name = name

    def leave_Assign(self, original_node, updated_node):
        if updated_node.targets[0].target.value == self.name:
            if isinstance(updated_node.value, cst.List):
                elements = list(updated_node.value.elements)
                elements.append(cst.SimpleString("'Core'"))
                updated_node = updated_node.with_changes(value=cst.List(elements=elements))
            elif isinstance(updated_node.value, cst.Tuple):
                # elements = list(updated_node.value.elements)
                elements = [ node.value.value for node in updated_node.value.elements]
                elements.append("Core")
                # elements.append(cst.SimpleString("'Core'"))
                updated_node = updated_node.with_changes(value=elements)
        print(updated_node)
        return updated_node



class ChangeInDict(cst.CSTTransformer):

    def __init__(self, tree, name, value, action, nested=False, key_to_insert=None, position=None):
        self.tree = tree
        self.name = name
        self.value = value
        self.action = action
        self.nested = nested
        self.key_to_insert = key_to_insert
        self.position = position

    def get_integer_value(self, value):
        return int(value.value)

    def get_simplestring_value(self, value):
        return value.raw_value

    def get_dict_value(self, value):
        result = {}
        for obj in value.elements:
            key = obj.key.raw_value
            value = self.get_Value(obj.value)
            result[key] = value
        return result

    def get_name_value(self, value):
        if value in ('True', 'False'):
            return ast.literal_eval(value.value)
        return value.value
    def get_list_value(self, value):
        result =[]
        for node in value.elements:
            node = self.get_Value(node.value)
            result.append(node)
        return result

    def get_tuple_value(self, value):
        result = self.get_list_value(value)
        return tuple(result)

    def get_Value(self, value):
        visit_func = getattr(self, f"get_{value.__class__.__name__.lower()}_value", None)
        retval = visit_func(value)
        return retval

    def update_dict_value(self, origin_python_value, value):
        origin_python_value.update(value)
        return origin_python_value

    def update_list_value(self, origin_python_value, value):
        origin_python_value.append(value)
        return origin_python_value

    def update_tuple_value(self, origin_python_value, value):
        if isinstance(value, (int, str)):
            value = (value,)
        return origin_python_value + value

    def update_str_value(self, origin_python_value, value):
        origin_python_value = str(value)
        return origin_python_value

    def update_int_value(self, origin_python_value, value):
        origin_python_value = value
        return origin_python_value

    def delete_list_value(self, origin_python_value, value):
        if value in origin_python_value:
            origin_python_value.remove(value)
        return origin_python_value

    def delete_tuple_value(self, origin_python_value, value):
        origin_python_value = list(origin_python_value)
        value = self.delete_list_value(origin_python_value, value)
        return tuple(value)

    def delete_dict_value(self, origin_python_value, key):
        if key in origin_python_value.keys():
            origin_python_value.pop(key)
        return origin_python_value

    def delete_Value(self, origin_python_value, value):
        visit_func = getattr(self, f"delete_{origin_python_value.__class__.__name__.lower()}_value", None)
        retval = visit_func(origin_python_value, value)
        return retval

    def update_nested_str_value(self, origin_python_value, value, nested, key_to_insert, position, change):
        return origin_python_value

    def update_nested_int_value(self, origin_python_value, value, nested, key_to_insert, position, change):
        return origin_python_value


    def update_nested_dict_value(self, origin_python_value, add_value, nested, key_to_insert, position, change):
        result = {}
        if change is True:
            origin_python_value.update(add_value)
        for key, dict_value in origin_python_value.items():
            if key == key_to_insert:
                change = True
                dict_value = self.update_Value(dict_value, add_value, nested, key_to_insert, position, change)
            else:
                dict_value = self.update_Value(dict_value, add_value, nested, key_to_insert, position, change)
            result[key] = dict_value
        return result


    def update_nested_list_value(self, origin_python_value, add_value, nested, key_to_insert, position, change):
        result = []
        if change is True:
            if position is not None:
                origin_python_value.insert(position, add_value)
            else:
                origin_python_value.append(add_value)
        for node in origin_python_value:
            node = self.update_Value(node, add_value, nested, key_to_insert, position, change)

            result.append(node)
        return result


    def update_Value(self, origin_python_value, add_value, nested, key_to_insert,position, change):
        if nested is True:
            visit_func = getattr(self, f"update_nested_{origin_python_value.__class__.__name__.lower()}_value", None)
            retval = visit_func(origin_python_value, add_value, nested, key_to_insert, position, change)
        else:
            visit_func = getattr(self, f"update_{origin_python_value.__class__.__name__.lower()}_value", None)
            retval = visit_func(origin_python_value, add_value)
        return retval

    def leave_Assign(self, original_node, updated_node):
        if updated_node.targets[0].target.value == self.name:
            # return cst.RemoveFromParent()
            value = updated_node.value
            origin_python_value = self.get_Value(value)
            if self.action == "add":
                # updated_value = self.update_Value(origin_python_value, self.value)
                updated_value = self.update_Value(origin_python_value, self.value, self.nested,
                                                         self.key_to_insert,
                                                         self.position, change=False)
            elif self.action == "delete":
                updated_value = self.delete_Value(origin_python_value, self.value)

            updated_node_value = cst.parse_expression(str(updated_value))
            updated_node = updated_node.with_changes(value=updated_node_value)
        return updated_node


    # def add_blank_line(self, node):
    #     return cst.SimpleStatementLine(
    #         body=[node],
    #         leading_lines=[
    #             cst.EmptyLine(
    #                 whitespace=cst.SimpleWhitespace(value=""),
    #                 comment=cst.Comment("# Hello comment code"),
    #                 newline=cst.Newline(value="")
    #             )
    #         ]
    #     )
    #
    # def leave_Module(self, original_node: "Module", updated_node: "Module") -> "Module":
    #     return updated_node.with_changes(
    #         body=[
    #             *updated_node.body,
    #             self.add_blank_line(cst.Assign(
    #                 targets=[
    #                     cst.AssignTarget(
    #                         target=cst.Name(value="DEMO")
    #                     )
    #                 ],
    #                 value=cst.parse_expression('"Hello World"'),
    #             ))
    #         ]
    #     )





# Your original code without triple quotes
a = """

DEBUG = False

SITE = 1

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'django.contrib.messages', 
)

MIDDLEWARE = (
    
    'corsheaders.middleware.CorsMiddleware',
    
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

DATABASES = {
    'default': {
        'CONN_MAX_AGE': 0,
        'ENGINE': 'django.db.backends.',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',  # Or path to database file if using sqlite3.
        'USER': '',
        'PASSWORD': '',
        'HOST': '',  # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',  # Set to empty string for default.
    },
    'main':"Abcd",
    
}

TEMPLATES =[
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'constance.context_processors.config',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries' : {
                'templatetags': 'base.templatetags.custom_tags',
            },
        },
    },
]

LST = [1,3,4,["5","6"]]

URL += ['demo', 'demo']


"""

parsed_code = cst.parse_module(a)
# updated_cst = parsed_code.visit(ChangeInVariableValue(a))
# updated_cst = parsed_code.visit(ChangeInInstalledApps(parsed_code, "MIDDLEWARE"))

# updated_cst = parsed_code.visit(ChangeInDict(parsed_code, "DATABASES", {"main2":"Hello"}))
# updated_cst = parsed_code.visit(ChangeInDict(parsed_code, "DATABASES",
#                                              'main',
#                                              'delete'))
updated_cst = parsed_code.visit(ChangeInDict(parsed_code, "TEMPLATES",
                                                  {"main":"abc"}, "add",
                                             True, 'libraries', ))
print(updated_cst.code)

# delete particular variable LST or URL
# append new value in += concvept


# append on postiion
# if condition
# add after variable
#