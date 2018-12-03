import aqt
from aqt import mw
from .generators.sugar.conditionals import *
from .generators.sugar.fields import *
from .generators.sugar.html import *
from .generators.child import *
from .generators.children import *
from .generators.leaf import *

def newConf(config):
    global read
    read = False

def get(s):
    global read
    if not read:
        reread()
        read = True
    return objects.get(s)
    
def set(s,value):
    objects[s] = value

read = False
def reread():
    global userOption
    userOption = dict()
    userOption = aqt.mw.addonManager.getConfig(__name__)
    instructions = userOption.get("instructions", [])
    objects = dict()
    for instruction in instructions:
        if isinstance(instruction,list):
            (name,value) = instruction
            define(name, value)
        elif isinstance(instruction,str):
            evaluate(instruction)
        else:
            assert False

        
    
# def globalIncreased():
#     return {**globals(), **objects}
def define(name, value):
    r = eval(value, globals(),  objects)
    objects[name] = r.getUnRedundate()
    return r
def evaluate(t):
    exec(t, globals(),locals = objects)
        

mw.addonManager.setConfigUpdatedAction(__name__,newConf)
