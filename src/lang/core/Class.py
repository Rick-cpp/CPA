from typing import TypedDict, List, Literal
from .Funcion import Function
from .Variable import Variable

class Class(TypedDict):
    name:str
    extends:str|None
    implements:List[str]

    members:List[Variable]
    methods:List[Function]

    visibility:Literal["public"]|Literal["private"]|Literal["protected"]
    scope:Literal["global"]|Literal["internal"]

test:Class = {
    "name": "MyClass",
    "extends": None,
    "implements": [],
    "members": [
        {
            "scope": "internal",
            "visibility": "public",
            "const": False,
            "type": "String",
            "name": "message",
            "value": "Ola Mundo"
        }
    ],
    "methods": [
        {
            "scope": "internal",
            "visibility": "public",
            "result": None,
            "name": "main",
            "params": [
                {
                    "const": False,
                    "ref": False,
                    "type": "int",
                    "name": "code",
                    "value": None
                }
            ],
            "const": False,
            "exception": "",
            "code": [
                "\tstd::out << \"Ola Mundo\" << std::endl;"
                "\treturn -1;"
            ]
        }
    ],
    "visibility": "public",
    "scope": "global"
}