from abc import ABC, abstractmethod
from ctypes import pointer
from functools import partial
import re
from typing import Callable, override

from click import group
from httpx import head
from matplotlib.pyplot import step
from numpy import mat
from controller.translator import Data


class Pointer:
    def __init__(self, code:list[str]):
        self.code     : list[str] = code
        self.position : int       = 0
    
    def push(self) -> str:
        return self.code[self.position]
    
    def next(self) -> bool:
        self.position += 1
        if self.position >= len(self.code):
            self.position -= 1
            return False
        return True

class Step(ABC):
    @abstractmethod
    def run(self, pointer:Pointer, output:Data.CHppFile) -> str: pass

class Compiler:
    def __init__(self, pointer:Pointer, steps:list[Step] = []):
        self.steps   : list[Step]    = steps
        self.output  : Data.CHppFile = Data.CHppFile()
        self.pointer : Pointer       = pointer
    
    def run(self) -> bool:
        for s in self.steps:
            r = s.run(self.pointer, self.output)
            if len(r) != 0:
                print(r)
                return False
        return True    

class StepPackage(Step):
    __cmd_regex:str = r"\/\/\s*@package\s*"
    __all_regex:str = __cmd_regex + r"[a-zA-Z\/]*"
    
    @override
    def run(self, pointer:Pointer, output:Data.CHppFile) -> str:
        line = pointer.push().strip()
        
        if not re.fullmatch(StepPackage.__all_regex, line):
            return "Error: Didn't find the Package annotation"
        
        package = re.split(StepPackage.__cmd_regex, line)
        
        if len(package) != 2: return ""
        
        output.package = package[1]
        pointer.next()
        return ""

class StepInclude(Step):
    __cmd_regex:str = r"\/\/\W*@import\W*"
    __cpp_regex:str = __cmd_regex + r"cpp"
    __hpp_regex:str = __cmd_regex + r"global"
    __name_regex:str = r"namespace\W*[a-zA-Z]+\W*{"
    __include_regex:str = r"#include <[a-zA-Z0-9_\-\\/.]+>"
    
    @override
    def run(self, pointer:Pointer, output:Data.CHppFile) -> str:
        line = pointer.push()
        
        if re.fullmatch(StepInclude.__hpp_regex, line):
            return self.h(pointer, output)
        
        if re.fullmatch(StepInclude.__cpp_regex, line):
            return self.cpp(pointer, output)
        
        return ""
    
    def h(self, pointer:Pointer, output:Data.CHppFile) -> str:        
        while pointer.next():
            line = pointer.push()
            
            if len(line.strip()) == 0: continue
            
            if re.fullmatch(StepInclude.__cpp_regex, line): return self.cpp(pointer, output)
            
            if re.fullmatch(StepInclude.__name_regex, line):
                args = line.split(" ")
                if len(args) != 3: return "Error: Incorrect Namespace Syntax"
                output.space = args[1]
                pointer.next()
                return ""
        
            if re.fullmatch(StepInclude.__include_regex, line):
                output.hIncludes.append(line.split("<")[1][:-1])
                continue
                
            return "Error: Unknown token"
            
    def cpp(self, pointer:Pointer, output:Data.CHppFile) -> str:
        while pointer.next():
            line = pointer.push()
            
            if len(line.strip()) == 0: continue
            
            if re.fullmatch(StepInclude.__name_regex, line):
                args = line.split(" ")
                if len(args) != 3: return "Error: Incorrect Namespace Syntax"
                output.space = args[1]
                pointer.next()
                return ""
        
            if re.fullmatch(StepInclude.__include_regex, line):
                output.cppIncludes.append(line.split("<")[1][:-1])
                continue
                
            return "Error: Unknown token"

class StepClass(Step):
    __regex:str = r"class [a-zA-Z]+( | : [a-zA-Z]+ ){"
    __var_regex:str = r"(?:const\s+)?([a-zA-Z:.\d]+)\s+([a-zA-Z_][a-zA-Z_0-9]*)\s*(?:=\s*(.+?))?;"
    __func_regex:str = r"(\s*const\s+)?([a-zA-Z_][\w:<>\s*&\[\]]*)\s+(operator[^\s(]+|[~\w:]+)\s*\(([^)]*)\)\s*(const\s*)?(?:\s*(final|override)\s*){0,2}\{([\s\S]*)\}"
    __param_regex:str = r"(const\s+)?([a-zA-Z:.\d]+)&?\s+([a-zA-Z_][a-zA-Z_0-9]*)"
    
    @override
    def run(self, pointer:Pointer, output:Data.CHppFile) -> str:
        line = pointer.push().strip()
        
        if not re.fullmatch(StepClass.__regex, line):
            return "Error: Incorrect class syntax"
        
        header = line.split(" ")
        
        output.cclass.name = header[1]
        
        if len(header) == 5:
            output.cclass.extends = header[4]
        
        return self.findScope(pointer, output)

    def findScope(self, pointer:Pointer, output:Data.CHppFile) -> str:
        scopes = [
            partial(self.runnerScope, output.cclass.public, pointer),
            partial(self.runnerScope, output.cclass.private, pointer),
            partial(self.runnerScope, output.cclass.proteced, pointer)
        ]
        target = scopes[1]
        output = None
        
        while not isinstance(output, str) :
            output = target()
            if isinstance(output, int):
                target = scopes[output]
        return output



    def runnerScope(self, cscope:Data.CScope, pointer:Pointer) -> str|int:
        while pointer.next():
            result = self.scope(pointer)
            if result == None: return ""
            
            if isinstance(result, Data.CVariable):
                cscope.cvariables.append(result)
                continue

        
            if isinstance(result, Data.CFunction):
                cscope.cfunctions.append(result)
                continue


            if isinstance(result, int): return result
            
            if len(result) == 0: continue
            
            return result
        


    def scope(self, pointer:Pointer) -> str|Data.CVariable|Data.CFunction|None|int:
        line = pointer.push().strip()
        
        if len(line.strip()) == 0: return ""
            
        if re.fullmatch(StepClass.__var_regex, line):
            var = Data.CVariable()
            if line.startswith("const "): 
                var.const = True
                line = line[6:]
            match = re.match(StepClass.__var_regex, line)
            if match:
                var.type = match.group(1)
                var.name = match.group(2)
                var.value = match.group(3) if match.group(3) else ""
                return var                    
            return "Error: Incorrect Variable Syntax"
        
        if re.fullmatch(StepClass.__func_regex, line):
            func = Data.CFunction()
            match = re.match(StepClass.__func_regex, line)
            
            if match:
                # return
                func.creturn.const = match.group(1) != None
                func.creturn.type = match.group(2)if match.group(2) else ""
                func.creturn.ref = "&" in match.group(2)

                # name
                func.name = match.group(3)
                
                #params
                func_params = match.group(4)
                if func_params:
                    args = func_params.split(", ")
                    for i in args:
                        arg = re.match(StepClass.__param_regex, i)
                        if arg:
                            param = Data.CParam()
                            param.const = arg.group(1) != None
                            param.type = arg.group(2)   
                            param.name = arg.group(3)
                            param.ref = "&" in i
                            func.cparams.append(param)
                        else:
                            return f"Error: Error: Incorrect Param Syntax {i}"
                
                func.const = match.group(5) != None
                func.override = match.group(6) != None
                
                if match.group(7):
                    func.code = match.group(7).split("\n")
                return func

        if line == "};": return None
        
        if line == "public:": return 0
        if line == "private:": return 1
        if line == "protected:": return 2
        
        return f"Error: Not context {line}"

def compiler(code:list[str]) -> Data.CHppFile|None:
    comp = Compiler(
        Pointer(code),
        [
            StepPackage(),
            StepInclude(),
            StepClass()
        ]
    )
    if not comp.run(): return None
    return comp.output