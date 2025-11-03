from typing import TypedDict, List, Literal
from .Funcion import Function


class Interface(TypedDict):
    name:str
    extends:str

    visibility:Literal["public"]|Literal["private"]|Literal["protected"]
    scope:Literal["global"]|Literal["internal"]

    methods:List[Function]