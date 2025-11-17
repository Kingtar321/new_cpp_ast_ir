from clang import cindex

def get_type(t):
    try: return t.spelling
    except: return None

def extract_function(c):
    return {
        "name": c.spelling,
        "return": get_type(c.result_type) if hasattr(c, "result_type") else None,
        "parameters": [{ "name": a.spelling, "type": get_type(a.type) } for a in c.get_arguments()],
        "location": f"{c.location.file}:{c.location.line}" if c.location.file else None
    }

def extract_class(c):
    return {
        "name": c.spelling,
        "fields": [
            {"name": f.spelling, "type": get_type(f.type)}
            for f in c.get_children()
            if f.kind == cindex.CursorKind.FIELD_DECL
        ],
        "methods": [
            extract_function(m)
            for m in c.get_children()
            if m.kind in (cindex.CursorKind.CXX_METHOD, cindex.CursorKind.CONSTRUCTOR)
        ]
    }

def extract_tu(root):
    ir = {"classes": [], "functions": []}
    for c in root.get_children():
        if c.kind == cindex.CursorKind.CLASS_DECL:
            ir["classes"].append(extract_class(c))
        elif c.kind == cindex.CursorKind.FUNCTION_DECL:
            ir["functions"].append(extract_function(c))
        elif c.kind == cindex.CursorKind.NAMESPACE:
            for child in c.get_children():
                if child.kind == cindex.CursorKind.CLASS_DECL:
                    ir["classes"].append(extract_class(child))
                elif child.kind == cindex.CursorKind.FUNCTION_DECL:
                    ir["functions"].append(extract_function(child))
    return ir
