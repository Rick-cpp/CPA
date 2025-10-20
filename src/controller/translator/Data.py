class CParam:
    def __init__(self):
        self.ref   : bool = False
        self.name  : str = ""
        self.type  : str = ""
        self.const : bool = False
    
    def __str__(self) -> str:
        text = "const " if self.const else ""
        text += f"{self.type}"
        if self.ref: text += "&"
        text += f" {self.name}"
        return text

class CReturn:
    def __init__(self):
        self.ref   : bool = False
        self.type  : str  = ""
        self.const : bool = False
    
    def __str__(self) -> str:
        text = "const " if self.const else ""
        text += f"{self.type}"
        if self.ref: text += "&"
        return text

class CFunction:
    def __init__(self):
        self.name     : str          = ""
        self.code     : list[str]    = []
        self.const    : bool         = False
        self.creturn  : CReturn      = CReturn()
        self.cparams  : list[CParam] = []
        self.override : bool         = False
    
    def cpp(self, className:str) -> str:
        text = f"{self.creturn}"
        if len(text) != 0: text += " "
        text += f"{className}::{self.name}("
        
        if len(self.cparams) != 0:
            for i in self.cparams:
                text += f"{i}, "
            text = text[:-2]
        
        text += ")"
        text += " const" if self.const else ""
        text += " override" if self.override else ""
        text += " {"
        
        if len(self.code) != 0:
            for i in self.code:
                text += f"{i}\n"
            text = text[:-1]
        text += "}"
        
        return text
    
    def h(self) -> str:
        text = f"{self.creturn}"
        if len(text) != 0: text += " "
        text += f"{self.name}("
        
        if len(self.cparams) != 0:
            for i in self.cparams:
                text += f"{i}, "
            text = text[:-2]
        
        text += ")"
        text += " const" if self.const else ""
        text += " override " if self.override else ""
        text += ";"
        return text

class CVariable:
    def __init__(self):
        self.name  : str = ""
        self.type  : str = ""
        self.value : str = ""
        self.const : bool = False
    
    def __str__(self) -> str:
        text = "const " if self.const else ""
        text += f"{self.type} {self.name}"
        if len(self.value) != 0: text += f" = {self.value}"
        text += ";"
        return text

class CScope:
    def __init__(self, name:str):
        self.name       : str             = name
        self.cvariables : list[CVariable] = []
        self.cfunctions : list[CFunction] = []
    
    def cpp(self, className:str) -> str:
        text = ""
        for i in self.cfunctions:
            text += f"{i.cpp(className)}\n"
        return text

    def h(self) -> str:
        text = f"{self.name}:\n\n"
        
        if len(self.cvariables) != 0:
            for i in self.cvariables: text += f"{i}\n"
            text += "\n"
        
        if len(self.cfunctions) != 0:
            for i in self.cfunctions: text += f"{i.h()}\n"
            text += "\n"
        
        return text
    
class CClass:
    def __init__(self):
        self.name     : str    = ""
        self.public   : CScope = CScope("public")
        self.extends  : str    = ""
        self.private  : CScope = CScope("private")
        self.proteced : CScope = CScope("proteced")
    
    def cpp(self) -> str:
        text = f"{self.public.cpp(self.name)}"
        text += f"{self.private.cpp(self.name)}\n"
        text += f"{self.proteced.cpp(self.name)}\n"

        return text
    
    def h(self) -> str:
        text = f"class {self.name}"
        if len(self.extends) != 0: text += f" : public {self.extends}"
        text += " {\n"
        text += f"{self.public.h()}\n"
        text += f"{self.private.h()}\n"
        text += f"{self.proteced.h()}\n"
        text += "};"
        return text

class CHppFile:
    def __init__(self):
        self.space       : str = ""
        self.cclass      : CClass = CClass()
        self.package     : str = ""
        self.hIncludes   : list[str] = []
        self.cppIncludes : list[str] = []
    
    def cpp(self) -> str:
        text = "#include <"
        if len(self.package) != 0: text += f"{self.package}/"
        text += f"{self.cclass.name}.h>\n\n"
        
        if len(self.cppIncludes) != 0:
            for i in self.cppIncludes: text += f"#include <{i}>\n"
            text += "\n"
        
        text += f"using namespace {self.space};\n\n"
        text += self.cclass.cpp()
        return text

    def h(self) -> str:
        text = "#pragma once\n\n"
        
        if len(self.hIncludes) != 0:
            for i in self.hIncludes: text += f"#include <{i}>\n"
            text += "\n"
        
        text += f"namespace {self.space}"
        text += " {\n"
        text += self.cclass.h()
        text += "\n}"
        
        return text