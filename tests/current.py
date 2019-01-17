from .functions import testEachStep, compileGen, genToSoup, genToTags, prettifyGen,TestHTML
from bs4 import BeautifulSoup
from html import escape
from copy import deepcopy
from ..generators import *
from ..debug import startDebug, endDebug, debug, assertEqual
from .data import *
from ..templates.soupAndHtml import templateFromSoup, soupFromTemplate
from ..templates.templates import tagsToEdit, compile_
from ..user_files import *

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
                            localFun= (lambda i:{"child":LI(FilledOrEmpty(f"Applied to{i}",
                                                                           DecoratedField(prefix="On ",
                                                                                          label = {f"Applied to{i}"},
                                                                                          field=f"Example{i}",
                                                                                          suffix=""),
                                                                          QuestionnedField(f"Example{i}",classes="Example"))),
                                                 "filledFields":[f"Example{i}"],
                                                 "questions":{f"Example{i}"}})))


na=NotAsked(
      field = 'asked',
      child = Literal(text = "Asked is not asked",),)
# compileGen(na, asked=frozenset(),toPrint=True)
# print("""






# """)
# compileGen(cascadeUseless, asked=frozenset(),toPrint=True)
#compileGen(question, fields={"Question","Answer","Answer2"}, isQuestion=True,asked={"Answer"}, toPrint=True)

startDebug()
#print(cascadeBeforeTemplate.template(asked={"cascaded"}))

endDebug()
#compileGen(examples, isQuestion=False, fields = {"Example", "Example2", "Example3"},asked =frozenset({"Question"}),   toPrint=True)


# compileGen(
#     fourQuestionsAsTable,
#     asked = frozenset(),
#     fields = {"Question","Question2", "Name","Name2"},
#     toPrint = True
# )
