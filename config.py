import aqt
from aqt import mw
from .generators import *
from .user_files import *

objects = dict()
def newConf(config):
    global read
    read = False

def readIfRequired():
    global read
    if not read:
        reread()
        read = True

def getObject(s = None, default = None):
    """Get the dictionnary of objects. If a name is given, return the
    object with this name if it exists.

    reads if required."""

    readIfRequired()
    if s is None:
        return objects
    else:
        return objects.get(s, default = None)

def _set(s,value):
    readIfRequired()
    objects[s] = value

def jsonStringToDic(jsonString, dic = dict()):
    json = json.loads(jsonString)
    return jsonToDic(instructions, dic)

def jsonToDic(json, dic = dict()):
    dic.clear()
    if json is not None:
        instructions = json.get("instructions", [])
        for instruction in instructions:
            if isinstance(instruction,list):
                (name,value) = instruction
                #debug("""Evaluating "{name}" as "{value}" of type {type(value)}.""")
                dic[name] =  ensureGen(eval(value,globals(), dic))
            elif isinstance(instruction,str):
                exec(instruction,globals(), dic)
            else:
                assert False
    return dic

read = False
def reread(objects=objects):
    #debug("reread", 1)
    userOption = aqt.mw.addonManager.getConfig(__name__)
    jsonToDic(userOption, objects)

def execute(t):
    #debug("execute({t})",1 )
    exec(t, globals(),locals = objects)
    #debug("reread()",-1 )

def evaluate(t, objects = objects):
    #debug("""evaluating "{t}" """)
    return eval(t, globals(), objects)

def define(name, value):
    #debug("define({name},{value})",1 )
    r = evaluate(value)
    #debug("define() find {r}")
    # r = ensureGen(r).getNormalForm()
    # #debug("define()'s normal form is {r}")
    r = ensureGen(r,objects).getWithoutRedundance()
    objects[name] = r
    #debug("define() returns {r}",-1 )
    return r


mw.addonManager.setConfigUpdatedAction(__name__,newConf)
