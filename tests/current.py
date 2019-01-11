from .functions import testEachStep, compileGen, genToSoup, genToTags, prettifyGen
from bs4 import BeautifulSoup
from html import escape
from copy import deepcopy
from ..generators.imports import *
from ..debug import startDebug, endDebug, debug, assertEqual
#from .data.imports import *
from ..templates.soupAndHtml import templateFromSoup, soupFromTemplate
from ..templates.templates import tagsToEdit
from ..user_files.imports import *

# tmp = '\n <span name="test" template="conf"/>\n'
# soup = soupFromTemplate(tmp)
# tags = tagsToEdit(soup)
# print (f"tags are {tags}")

#print(prettifyGen(NumberedFields('Definition', 2),toPrint=True))
labelDef=[Label("Definition",["Definition"]),
          FilledOrEmpty("Conjdef",
                      Cascade("Definitions",[QuestionnedField("Conjdef",["Conjdef"]),": "],["Conjdef"]),
                      Filled ("Definition2","Equivalently: "))
]
definitions = NumberedFields(fieldPrefix="Definition",
                                        greater=16,
                                        label=labelDef
)
at=AtLeastOneField(child = CLASS(["foo"],""),
                   fields = ["foo"],
                   otherwise = labelDef,
                   asked = True
)
label=Label(label=labelDef,
            fields=["foo"],classes=[])

ex=('Example',
             NumberedFields('Example',
                            4,
                            suffix=hr,
                            localFun= (lambda i:(LI(FilledOrEmpty(f"Applied to{i}",
                                                                  DecoratedField(prefix="On ",
                                                                                 label = {f"Applied to{i}"},
                                                                                 field=f"Example{i}",
                                                                                 suffix=""),
                                                                  QuestionnedField(f"Example{i}",classes="Example"))),
                                                 {f"Example{i}"},{f"Example{i}"}))))

#compileGen(ex, toPrint=True, fields ={"Applied to","Example","Applied to2","Example2","Applied to3","Example3","Applied to4","Example4"})

startDebug()
#print(cascadeBeforeTemplate.template(asked={"cascaded"}))
endDebug()
# compileGen(DecoratedField("Question"), asked =frozenset("Question"),   toPrint=True)

# raise Exception
