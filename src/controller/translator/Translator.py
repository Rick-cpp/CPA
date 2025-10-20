import os
import pathlib
from controller.translator import Service

CURRENT_PATH = os.getcwd()

def translatorController(args:list[str]) -> None:
    if "*" in args[0]:
        data = files(deep=args[0] == "**")
        

def files(root:str = CURRENT_PATH, current:list[str] = [], deep:bool = False) -> list[str]:
    for i in pathlib.Path(root).glob("*"):
        if deep == True and i.is_dir():
            files(i.absolute(), current, deep)
            continue
        if ".hpp" in i.name:
            current.append(str(i.absolute()))
    return current

def _create(name:str) -> None:
    with open(os.path.join(CURRENT_PATH, name), "r") as File:
        content = File.readlines()
        File.close()
    

    lines = []
    
    for i in range(len(content)):
        line = content[i].replace("\n", "")    
        if len(line) != 0:
            lines.append(line)
    
    del_list = [] 
    index = 0
    end = 0
    target = ""
    _ = 0
    
    for p in range(len(lines)):
        i = lines[p]
        if "{" in i:
            if "class" in i: continue
            if "namespace" in i: continue
            _ += 1
            
            if _ == 1:
                index = p
                end = p
        if _ > 0:
            target += f"{i}\n"
            end = p
        if "}" in i and _ > 0:
            _ -= 1
            if _ == 0:
                lines[index] = target
                del_list.append((index+1, end+1))
                index = -1
                end = -1
    
    
    for i in del_list: del lines[i[0]:i[1]]
 
    file = Service.compiler(lines)
    if file == None:
        return
    
    with open(os.path.join(CURRENT_PATH, file.cclass.name + ".h"), "w") as H:
        H.write(file.h())
        H.close()
        
    with open(os.path.join(CURRENT_PATH, file.cclass.name + ".cpp"), "w") as C:
        C.write(file.cpp())
        C.close()    