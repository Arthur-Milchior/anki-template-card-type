from ..imports import *
modelCompiled = compileModel(model, objects = testObjects, prettify = True)
print(modelCompiled)
assert assertEqual("modelCompiled['tmpls'][0]['qfmt']","htmlTestObjectCompiled")
assert assertEqual("modelCompiled['tmpls'][0]['afmt']","htmlAnswerTestCompiled")
assert assertEqual("modelCompiled['tmpls'][1]['qfmt']","htmlFrontFieldCompiledFront")
#assert assertEqual("modelCompiled['tmpls'][1]['afmt']","htmlAnswerTestCompiled")
