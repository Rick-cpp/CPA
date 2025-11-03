from typing import TypedDict, List, Literal

class _Function_Result(TypedDict):
    type:str
    
    const:bool
    ref:bool

class _Function_Param(TypedDict):
    name:str
    type:str
    value:str|None
    
    const:bool
    ref:bool

class Function(TypedDict):
    name:str
    result:_Function_Result|None
    params:List[_Function_Param]

    visibility:Literal["public"]|Literal["private"]|Literal["protected"]
    scope:Literal["global"]|Literal["internal"]

    const:bool
    exception:str

    code:List[str]