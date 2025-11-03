from .Default import LangObject;
from .Interface import Interface;
from . import Variable;
from . import Function;

class ClassName(LangObject):
    extends:"ClassName"
    implements:Interface
    members:list[Variable.Variable]|None
    methods:list[Function.Function]|None
