import os

def translatorMiddleware(args:list[str]) -> bool:
    if len(args) != 1:
        return False
    if args[0] == "*":
        return True
    
    if args[0] == "**":
        return True
    exist = os.path.exists(os.path.join(os.getcwd(), args[0]))
    if not exist:
        return print("Error: File not found.") == True
    return True