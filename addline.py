# from libcst import Module, Dict, SimpleStatementLine, Newline
# from libcst import CSTTransformer, parse_statement
import libcst as cst
from libcst import Dict

class AddNewlineTransformer(cst.CSTTransformer):
    def visit_Dict(self, node: Dict) -> Dict:
        if "REST_FRAMEWORK" in str(node):
            new_body = []
            found_rest_framework = False

            for item in node.body:
                if isinstance(item, cst.SimpleStatementLine):
                    if "REST_FRAMEWORK" in str(item):
                        found_rest_framework = True
                        new_line = cst.SimpleStatementLine(
                            body=[cst.SimpleWhitespace("\n")],
                            leading_whitespace=cst.SimpleWhitespace("\n")
                        )
                        new_body.append(item)
                        new_body.append(new_line)
                    else:
                        new_body.append(item)
                else:
                    new_body.append(item)

            if not found_rest_framework:
                # If "REST_FRAMEWORK" was not found, just return the original node
                return node

            return node.with_changes(body=new_body)
        return node

original_code = """
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ]
}

SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "User Token": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Enter your token in the format: 'Token exampletoken'",
        },
    },
}
"""

parsed_code = cst.parse_statement(original_code)
transformer = AddNewlineTransformer()
modified_code = parsed_code.visit(transformer)
print(modified_code.code)
