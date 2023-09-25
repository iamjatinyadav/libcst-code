
import libcst as cst
import ast

class WorkingWithNested(cst.CSTTransformer):
    def __init__(self, tree, name, value, nested=False, key_to_insert=None, position=None):
        self.tree = tree
        self.name = name
        self.value = value
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

    def update_dict_value(self, origin_python_value, value, nested, key_to_insert):
        # if nested == False:
            origin_python_value.update(value)
            return origin_python_value
        # else:
        #     current_dict = origin_python_value
        #     for k in value:
        #         if k in current_dict:
        #             current_dict = current_dict[k]
        #         else:
        #             return origin_python_value  # One of the keys is missing, can't proceed
        #
        #     if isinstance(current_dict, list):
        #         current_dict.insert(0, key_to_insert)
        #     return origin_python_value

    def update_list_value(self, origin_python_value, value, nested, key_to_insert):
        # if nested == False:
            origin_python_value.append(value)
            return origin_python_value
        # else:
        #     current_dict = origin_python_value[0]
        #     for k in key_to_insert:
        #         if k in current_dict:
        #             current_dict = current_dict[k]
        #         else:
        #             return origin_python_value  # One of the keys is missing, can't proceed
        #
        #     if isinstance(current_dict, list):
        #         current_dict.insert(0, value)
        #     return origin_python_value



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

    def update_nested_str_value(self, origin_python_value, value, nested, key_to_insert, position, change):
        return origin_python_value

    def update_nested_int_value(self, origin_python_value, value, nested, key_to_insert, position, change):
        return origin_python_value

    def update_Value(self, origin_python_value, value, nested, key_to_insert):
        visit_func = getattr(self, f"update_{origin_python_value.__class__.__name__.lower()}_value", None)
        retval = visit_func(origin_python_value, value, nested, key_to_insert)
        return retval

    def update_nested_dict_value(self, origin_python_value, add_value, nested, key_to_insert, position, change):
        result = {}
        if change is True:
            origin_python_value.update(add_value)
        for key, dict_value in origin_python_value.items():
            if key == key_to_insert:
                change = True
                dict_value = self.update_nested_Value(dict_value, add_value, nested, key_to_insert, position, change)
            else:
                dict_value = self.update_nested_Value(dict_value, add_value, nested, key_to_insert, position, change)
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
            node = self.update_nested_Value(node, add_value, nested, key_to_insert, position, change)

            result.append(node)
        return result


    def update_nested_Value(self, origin_python_value, add_value, nested, key_to_insert,position, change):
        visit_func = getattr(self, f"update_nested_{origin_python_value.__class__.__name__.lower()}_value", None)
        retval = visit_func(origin_python_value, add_value, nested, key_to_insert, position, change)
        return retval

    def leave_Assign(self, original_node: "Assign", updated_node: "Assign"):
        if updated_node.targets[0].target.value == self.name:
            value = updated_node.value
            origin_python_value = self.get_Value(value)
            updated_value = self.update_nested_Value(origin_python_value, self.value, self.nested, self.key_to_insert,
                                                    self.position, change=False)
            updated_node_value = cst.parse_expression(str(updated_value))
            updated_node = updated_node.with_changes(value=updated_node_value)
        return updated_node


code = """
TEMPLATES = {
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
    }
"""
parsed_code = cst.parse_module(code)
# updated_cst = parsed_code.visit(ChangeInVariableValue(a))
# updated_cst = parsed_code.visit(ChangeInInstalledApps(parsed_code, "MIDDLEWARE"))

# updated_cst = parsed_code.visit(ChangeInDict(parsed_code, "DATABASES", {"main2":"Hello"}))
updated_cst = parsed_code.visit(WorkingWithNested(parsed_code, "TEMPLATES",
                                                  {"main":"abc"},
                                             True, 'libraries', ))
print(updated_cst.code)