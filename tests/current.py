from .functions import testEachStep, compileGen
from bs4 import BeautifulSoup
from html import escape
from copy import deepcopy
from ..generators.imports import *
from ..debug import startDebug, endDebug, debug
from .data.imports import *

# qa = compileGen(
#     twoQuestionsAsTable,
#     asked =frozenset(),
#     goal = QUESTION_ANSWER
# )
#print(f"twoQuestionsAsTable is \n{twoQuestionsAsTable}")
# comp = compileGen(NumberedFields('Definition', 2),toPrint = True, asked = frozenset({"Definitions"}))
# print(f"result: {comp}")
print(f"Normal form: {orderedList.getNormalForm()}")

startDebug()
#compileGen(twoQuestionsAsTable, asked =frozenset({"Definition"}), toPrint = True)

# mr = qa.restrictToModel(fields)
# print(f"mr: {mr}")

# print(f"nf: {compileGen(requirements3, toPrint = True)}")
# assert False
#compileGen(atLeastTwoQuestion,toPrint = True)
# test = AtLeastTwoFields(child = "At least two",
#                         fields = ([ "Definition2", "Definition"]))
# # cg = compileGen(test)
# # print(cg)

# nf =test.getNormalForm()
# print(f"nf is {nf}")
endDebug()
# # debug("current")

#assert False
