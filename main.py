import json
from parse_cpp import parse_file, cursor_to_simple_ast
from ast_to_ir import extract_tu

import sys

file = sys.argv[1]
tu, root = parse_file(file)

# AST snapshot
with open("ast.json", "w") as f:
    json.dump(cursor_to_simple_ast(root), f, indent=2)

# IR
ir = extract_tu(root)
with open("ir.json", "w") as f:
    json.dump(ir, f, indent=2)

print("Generated ast.json and ir.json")
