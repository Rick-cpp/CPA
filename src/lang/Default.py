from typing import TypedDict, Literal

class LangStructure(TypedDict):
    name:str

class LangObject(LangStructure):
    visibility:Literal["public"]|Literal["private"]|Literal["protected"]|None
    scope:Literal["global"]|Literal["internal"]
