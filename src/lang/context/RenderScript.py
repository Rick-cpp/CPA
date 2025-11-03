from src.lang.core.Script import Script

def renderH(script:Script) -> str:
    code = "#pragma once;\n\n"
    
    code += f"\n#include <{script['namespace']}>;\n"

    for i in script["includes"]:
        code += f"#include <{i}>;\n"
    
    code += "\n"
    path = script['namespace'].split("\\")
    code += f"namespace {path[len(path)-1]} "
    code += "{\n"



    return code
