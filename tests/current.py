from .functions import testEachStep, compileGen, genToSoup, genToTags, prettifyGen
from bs4 import BeautifulSoup
from html import escape
from copy import deepcopy
from ..generators.imports import *
from ..debug import startDebug, endDebug, debug, assertEqual
#from .data.imports import *
from ..templates.soupAndHtml import templateFromSoup, soupFromTemplate
from ..templates.templates import tagsToEdit

# tmp = '\n <span name="test" template="conf"/>\n'
# soup = soupFromTemplate(tmp)
# tags = tagsToEdit(soup)
# print (f"tags are {tags}")

#print(prettifyGen(NumberedFields('Definition', 2),toPrint=True))
#cascadeBeforeTemplate=compileGen(cascadeUseless, asked={"asked"})
startDebug()
#print(cascadeBeforeTemplate.template(asked={"cascaded"}))
endDebug()
# compileGen(DecoratedField("Question"), asked =frozenset("Question"),   toPrint=True)

# raise Exception
