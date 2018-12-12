import aqt
from aqt import mw
from .imports import *

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
            execute(instruction)
        else:
            assert False
    #debug("reread", -1)

def execute(t):
    #debug(f"execute({t})",1 )
    exec(t, globals(),locals = objects)
    #debug(f"reread()",-1 )

def evaluate(t, objects = objects):
    #debug(f"""evaluating "{t}" """)
    return eval(t, globals(), objects)
        
def define(name, value):
    #debug(f"define({name},{value})",1 )
    r = evaluate(value)
    #debug(f"define() find {r}")
    # r = ensureGen(r).getNormalForm()
    # #debug(f"define()'s normal form is {r}")
    r = ensureGen(r,objects).getWithoutRedundance()
    objects[name] = r
    #debug(f"define() returns {r}",-1 )
    return r


mw.addonManager.setConfigUpdatedAction(__name__,newConf)
