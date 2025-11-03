from .Default import LangObject
from . import ClassName

class Variable(LangObject):
    type:ClassName.ClassName
    value:str
    const:bool
