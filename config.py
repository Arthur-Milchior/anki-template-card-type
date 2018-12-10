import aqt
from aqt import mw
from .generators.sugar.conditionals import *
from .generators.sugar.fields import *
from .generators.sugar.html import *
from .generators.child import *
from .generators.children import *
from .generators.leaf import *
from .generators.generators import ensureGen
from .debug import debug

objects = dict()
def newConf(config):
    global read
    read = False

def readIfRequired():
    global read
    if not read:
        reread()
        read = True
        
def getObject(s = None):
    """Get the dictionnary of objects. If a name is given, return the
    object with this name if it exists.

    reads if required."""
    
    readIfRequired()
    if s is None:
        return objects
    else:
        return objects.get(s)
    
def _set(s,value):
    readIfRequired()
    objects[s] = value

read = False
def reread(objects=objects):
    #debug("reread", 1)
    global userOption
    userOption = aqt.mw.addonManager.getConfig(__name__)
    instructions = userOption.get("instructions", [])
    objects.clear()
    for instruction in instructions:
        #debug(f"reread {instruction}" )
        if isinstance(instruction,list):
            (name,value) = instruction
            define(name, value)
        elif isinstance(instruction,str):
            evaluate(instruction)
        else:
            assert False
    #debug("reread", -1)

def evaluate(t):
    #debug(f"evaluate({t})",1 )
    exec(t, globals(),locals = objects)
    #debug(f"reread()",-1 )
        
def define(name, value):
    #debug(f"define({name},{value})",1 )
    r = eval(value, globals(),  objects)
    #debug(f"define() find {r}")
    # r = ensureGen(r).getNormalForm()
    # #debug(f"define()'s normal form is {r}")
    r = ensureGen(r,objects).getWithoutRedundance()
    objects[name] = r
    #debug(f"define() returns {r}",-1 )
    return r


mw.addonManager.setConfigUpdatedAction(__name__,newConf)
