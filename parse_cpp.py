import sys
import os

# ------------------------------------------------------------
# FIX PYTHON PATH: Force Python to load Ubuntu system clang
# Ubuntu installs clang Python bindings here:
#   /usr/lib/python3/dist-packages/clang
# But GitHub Codespace uses a custom Python interpreter that
# does NOT load system site packages automatically.
# ------------------------------------------------------------
sys.path.insert(0, "/usr/lib/python3/dist-packages")

from clang import cindex

# ------------------------------------------------------------
# IMPORTANT: Set libclang path (Ubuntu 24.04 / LLVM 18)
# Run this to find the exact file:
#   sudo find /usr -name "libclang.so"
# ------------------------------------------------------------
cindex.Config.set_library_file("/usr/lib/llvm-18/lib/libclang.so")


# ------------------------------------------------------------
# Parse a C++ file using libclang
# Returns (translation_unit, root_cursor)
# ------------------------------------------------------------
def parse_file(path, args=['-std=c++17']):
    index = cindex.Index.create()
    tu = index.parse(path, args=args)
    return tu, tu.cursor


# ------------------------------------------------------------
# Convert AST cursor into a simplified JSON-friendly tree
# This is useful for debugging and visualizing the AST.
# ------------------------------------------------------------
def cursor_to_simple_ast(node, depth=0, max_depth=3):
    out = {
        "kind": str(node.kind).split('.')[-1],
        "spelling": node.spelling,
        "location": (
            f"{node.location.file}:{node.location.line}"
            if node.location.file else None
        )
    }

    # Recursively process children nodes
    if depth < max_depth:
        children = []
        for c in node.get_children():
            children.append(cursor_to_simple_ast(c, depth + 1, max_depth))
        if children:
            out["children"] = children

    return out
