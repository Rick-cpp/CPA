from typing import TypedDict, Literal

class Variable(TypedDict):
    type:str
    name:str
    value:str|None
    
    visibility:Literal["public"]|Literal["private"]|Literal["protected"]
    scope:Literal["global"]|Literal["internal"]

    const:bool
