from ..imports import *

jsonTest = """{
    "instructions":[
        ["test", "'test'"],
        ["foo","[\\"foo\\",None, Field(\\"Question\\")]"],
        ["Question", "DecoratedField('Question')"]
    ]
}"""
testObjects = dict()
userOption = json.loads(jsonTest)
instructions = userOption.get("instructions", [])
for instruction in instructions:
    if isinstance(instruction,list):
        (name,value) = instruction
        #debug(f"""Evaluating "{name}" as "{value}" of type {type(value)}.""")
        testObjects[name] =  ensureGen(eval(value,globals(), testObjects))
    elif isinstance(instruction,str):
        exec(instruction,globals(), testObjects)
    else:
        assert False
