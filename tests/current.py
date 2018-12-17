from .functions import testEachStep, compileGen
from bs4 import BeautifulSoup
from html import escape
from copy import deepcopy
from ..generators.imports import *
from ..debug import startDebug, endDebug, debug
from .data.imports import *

#compileGen(atLeastTwoQuestion,toPrint = True)
# test = AtLeastTwoFields(child = "At least two",
#                         fields = ([ "Definition2", "Definition"]))
# # cg = compileGen(test)
# # print(cg)

# startDebug()
# nf =test.getNormalForm()
# print(f"nf is {nf}")
# endDebug()
# # debug("current")

