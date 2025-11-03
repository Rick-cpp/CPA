from .Default import LangObject
from . import Variable

class Function(LangObject):
    result:Variable.Variable|None
    params:list[Variable.Variable]|None
    const:bool
    exception:bool