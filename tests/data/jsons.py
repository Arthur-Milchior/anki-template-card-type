import json

from ...config import jsonToDic

jsonTest = """{
    "instructions":[
        ["test", "'test'"],
        ["foo","['foo',None, Field('Question')]"],
        ["Question", "DecoratedField('Question')"],
        ["TwoDefsHard","NumberedFields('Definition', 2)"],
        ["TwoDefsEasy","ListElement([DecoratedField('Definition'),DecoratedField('Definition2')])"]
    ]
}"""
# ,        ["TwoDefsMiddle","ListFields(['Definition', 'Definition2'])"],


#        ["Definitions_","NumberedFields(\\"Definition\\", 16)"]
# ,\\"Definition3\\",\\"Definition4\\",\\"Definition5\\",\\"Definition6\\",\\"Definition7\\",
testObjects = dict()
userOption = json.loads(jsonTest)
testObjects = jsonToDic(userOption)
