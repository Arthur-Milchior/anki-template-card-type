from ...debug import assertEqual
from ...editTemplate import compileModel
from ..data import *

modelCompiled = compileModel(model, objects = testObjects, prettify = True)
#print(modelCompiled)
assert assertEqual(modelCompiled['tmpls'][0]['qfmt'],htmlTestObjectCompiled)
assert assertEqual(modelCompiled['tmpls'][0]['afmt'],htmlAnswerTestCompiled)
assert assertEqual(modelCompiled['tmpls'][1]['qfmt'],htmlQuestionCompiled)
assert assertEqual(modelCompiled['tmpls'][1]['afmt'],htmlAnswerCompiled)
