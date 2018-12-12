from ..imports import *

jsonTest = """{
    "instructions":[
        ["test", "'test'"],
        ["foo","['foo',None, Field('Question')]"],
        ["Question", "DecoratedField('Question')"],
        ["TwoDefsMiddle","ListFields(['Definition1', 'Definition2'])"],
        ["TwoDefsHard","NumberedFields('Definition', 2)"],
        ["TwoDefsEasy","ListElement([DecoratedField('Definition1'),DecoratedField('Definition2')])"]
    ]
}"""
#,

#        ["Definitions_","NumberedFields(\\"Definition\\", 16)"]
#,\\"Definition3\\",\\"Definition4\\",\\"Definition5\\",\\"Definition6\\",\\"Definition7\\",
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
