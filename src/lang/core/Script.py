from typing import TypedDict, List
from .Class import Class

class Script(TypedDict):
    imports:List[str]
    includes:List[str]

    namespace:str

    className:Class
