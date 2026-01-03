from copy import deepcopy
from html import escape

from bs4 import BeautifulSoup

from ..debug import assertEqual, debug, endDebug, startDebug
from ..generators import *
from ..templates.soupAndHtml import soupFromTemplate, templateFromSoup
from ..templates.templates import compile_
from ..user_files import *
from .data import *
from .functions import (TestHTML, compileGen, genToSoup, genToTags,
                        prettifyGen, testEachStep)

# tmp = '\n <span name="test" template="conf"/>\n'
# soup = soupFromTemplate(tmp)
# print (f"tags are {tags}")

labelDef = [Label("Definition", ["Definition"]),
            FilledOrEmpty("Conjdef",
                          Cascade("Definitions",
                                  [QuestionnedField(
                                      "Conjdef", ["Conjdef"]), ": "],
                                  {"Conjdef"}),
                          Filled("Definition2", "Equivalently: "))
            ]
definitions = NumberedFields(fieldPrefix="Definition",
                             numbered_field=numbered_field,
                             greater=16,
                             numbered_field=numbered_field;
                             label=labelDef
                             )
at = AtLeastOneField(child=CLASS(["foo"], ""),
                     fields=["foo"],
                     otherwise=labelDef,
                     asked=True
                     )
label = Label(label=labelDef,
              fields=["foo"], classes=[])

ex = ('Example',
      NumberedFields('Example',
                     4,
                     numbered_field=numbered_field;
                     suffix=hr,
                     localFun=(lambda i: {"child": LI(FilledOrEmpty(f"Applied to{i}",
                                                                    DecoratedField(prefix="On ",
                                                                                   label={
                                                                                       f"Applied to{i}"},
                                                                                   field=f"Example{i}",
                                                                                   suffix=""),
                                                                    QuestionnedField(f"Example{i}", classes="Example"))),
                                          "filledFields": [f"Example{i}"],
                                          "questions": {f"Example{i}"}})))


na = NotAsked(
    field='asked',
    child=Literal(text="Asked is not asked",),)
labelDef = FilledOrEmpty("Conjdef",
                         Cascade("Definitions",
                                 QuestionnedField("Conjdef", ["Conjdef"]),
                                 {"Conjdef"}),
                         Filled("Definition2",
                                "Equivalently"))
definitions = ("Definition",
               [NumberedFields(fieldPrefix="Definition",
                               greater=3,
                               numbered_field=numbered_field,
                               label=labelDef,
                               #infix = ""
                               ),
                hr])
label = Label(label=labelDef,
              fields=["Definitions", "Definition1", "Definition2"],
              classes="test class")
alo = AtLeastOneField(child=CLASS(["Definitions", "Definition1", "Definition2"], labelDef),
                      fields=["Definitions"],
                      asked=True,
                      otherwise=labelDef)
# compileGen(
#     NotAsked(
#         field = 'Definitions',
#         child = Cascade(
#             field = 'Definitions',
#             cascade = {'Conjdef'},
#             child =NotAsked(
#                 field = 'Conjdef',
#                 child = Field(field = "Conjdef",
#                               useClasses = False,
#                 ),
#             ),
#         )
#     ),
#     fields=frozenset({"Conjdef","Definition","Definition2","Definition3"}),toPrint=True)
# print("""
#raise Exception

"""ListElement([
  Asked(
    field = 'Definitions',
    child = HTML("span",
      attrs = {'class': 'Definitions Definition1 Definition2'},
      child = ListElement([
        Filled(
          field = 'Conjdef',
          child = Cascade(
            field = 'Definitions',
            cascade = {'Conjdef'},
            child = ListElement([
              Asked(
                field = 'Conjdef',
                child = ListElement([
                  Question(
                    child = HTMLAtom("markofquestion",),),
                  Answer(
                    child = HTML("span",
                      attrs = {'class': 'Answer Emphasize Conjdef'},
                      child = Field(field = "Conjdef",
                        useClasses = False,),),)],),),
              NotAsked(
                field = 'Conjdef',
                child = HTML("span",
                  attrs = {'class': 'Conjdef'},
                  child = Field(field = "Conjdef",
                    useClasses = False,),),)],),),),
        Empty(
          field = 'Conjdef',
          child = Filled(
            field = 'Definition2',
            child = Literal(text = "Equivalently",),),)],),),),
  NotAsked(
    field = 'Definitions',
    child = ListElement([
      Filled(
        field = 'Conjdef',
        child = Cascade(
          field = 'Definitions',
          cascade = {'Conjdef'},
          child = ListElement([
            Asked(
              field = 'Conjdef',
              child = ListElement([
                Question(
                  child = HTMLAtom("markofquestion",),),
                Answer(
                  child = HTML("span",
                    attrs = {'class': 'Answer Emphasize Conjdef'},
                    child = Field(field = "Conjdef",
                      useClasses = False,),),)],),),
            NotAsked(
              field = 'Conjdef',
              child = HTML("span",
                attrs = {'class': 'Conjdef'},
                child = Field(field = "Conjdef",
                  useClasses = False,),),)],),),),
      Empty(
        field = 'Conjdef',
        child = Filled(
          field = 'Definition2',
          child = Literal(text = "Equivalently",),),)],),)],)"""


# """)
# compileGen(cascadeUseless, asked=frozenset(),toPrint=True)
#compileGen(question, fields={"Question","Answer","Answer2"}, isQuestion=True,asked={"Answer"}, toPrint=True)

startDebug()
# print(cascadeBeforeTemplate.template(asked={"cascaded"}))

endDebug()
#compileGen(examples, isQuestion=False, fields = {"Example", "Example2", "Example3"},asked =frozenset({"Question"}),   toPrint=True)


# compileGen(
#     fourQuestionsAsTable,
#     asked = frozenset(),
#     fields = {"Question","Question2", "Name","Name2"},
#     toPrint = True
# )
