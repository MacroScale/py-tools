from os import walk

def get_local_tools():
    f = []
    for (_, _, name) in walk("tools"):
        f.extend(name)
        break
    
    f.remove("__init__.py")
    return f
