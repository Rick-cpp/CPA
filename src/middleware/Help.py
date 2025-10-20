_HELP_ARGS:list[str] = [
    "--template",
    "--translator"
]

def helpMiddleware(args:list) -> bool:
    size = len(args)
    
    if size < 0 and size > 1: return False
    if size == 1: return args[0] in _HELP_ARGS
    return True