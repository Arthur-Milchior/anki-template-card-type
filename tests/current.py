from .functions import testEachStep, compileGen, genToSoup, prettifyGen
from bs4 import BeautifulSoup
from html import escape
from copy import deepcopy
from ..generators.imports import *
from ..debug import startDebug, endDebug, debug
from .data.imports import *
from ..templates.soupAndHtml import templateFromSoup, soupFromTemplate
from ..templates.templates import tagsToEdit

# tmp = '\n <span name="test" template="conf"/>\n'
# soup = soupFromTemplate(tmp)
# tags = tagsToEdit(soup)
# print (f"tags are {tags}")


startDebug()
endDebug()

