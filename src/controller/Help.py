from ast import arg


_ARGS = {
    "": """CppUtil is a tool that helps in the creation of CPP Projects with template and tools that help to accelerate development

-> template: The template contains the Scons file template ready for the project

-> translator: Helps with development by converting .hpp to .h and .cpp without having to create two files""",
    "--template": """The template contains the Scons file template ready for the project

-> Win_Basic: Creates a basic template that converts to .exe by reading all files in src""",
    "--translator": """Helps with development by converting .hpp to .h and .cpp without having to create two files

* Compilation Options
Use line comments to set things up.
translator --create <FileName>
It creates an .hpp file with the necessary templates to split the files. Use // as an @ annotation to define the Split option. Example:
//@name args...
[@import] <global|cpp> defines the include list. It must be in the global or cpp file.
[@package] String define package path"""
}

def helpController(args:list[str]) -> None:
    if len(args) == 0: return print(_ARGS[""])
    
    item = args[0]
    if not item in _ARGS.keys(): return help([])
    
    print(_ARGS[item])
