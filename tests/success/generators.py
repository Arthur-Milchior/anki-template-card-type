# List of templates which must be equals
from ...debug import assertEqual, startDebug
from ..data.imports import *
from ..functions import *
# Core
## Leaf

### Empty
assert assertEqual(emptyGen, none)
assert assertEqual(none.getNormalForm(), none)
assert assertEqual(none.getWithoutRedundance(), none)
assert none.isEmpty()
assert not none.toKeep
assert not none
#assert assertEqual(emptyGen, Empty(createOther = True))
assert none == ensureGen(None)

### Literal
assert assertEqual(literalTest , Literal("test"))
assert assertEqual(literalTest, literalTest.getNormalForm())
assert assertEqual(literalTest, literalTest.getWithoutRedundance())
assert not literalTest.isEmpty()
assert literalTest
assert literalTest !=  emptyGen
assert emptyGen !=  literalTest
assert assertEqual(literalTest.restrictToModel(fields), literalTest)
assert literalTest != literalFoo
stringFoo = ensureGen("foo")
assert assertEqual(stringFoo, literalFoo)

### Field 
assert assertEqual(fieldFoo_, fieldFooClassless)
assert fieldFooClassless  !=  Literal("test")
assert fieldFooClassless !=  Literal("{{foo}}")
assert fieldFooClassless != fieldFooClass
assert assertEqual(fieldFooClassless, Field('foo',addClass=False))
assert assertEqual(fieldFooClassless, fieldFooClassless.getNormalForm())
assert assertEqual(fieldFooClassless, fieldFooClassless.getWithoutRedundance())
assert assertEqual(compileGen(fieldFooClass, fields={"foo"}), CLASS("foo",Field("foo",addClass=False)))
assert assertEqual(fieldFooClass, fieldFooClass.getWithoutRedundance())
assert not fieldFooClassless.isEmpty()
assert fieldFooClassless.toKeep
assert fieldFooClassless
assert assertEqual(compileGen(fieldFooClassless), emptyGen)
assert assertEqual(compileGen(fieldQuestion), fieldQuestion)

## singleChild
### HTML
assert assertEqual(compileGen(image),image)
tdStyle = {"class": "tdStyle"}
trStyle = {"class": "trStyle"}
assert assertEqual(compileGen(table),
                   HTML("table",
                        child = ListElement(
                            [HTML("tr",
                                  child = ListElement([
                                      HTML("td",
                                           child = Literal("00"),
                                           attrs = tdStyle,
                                      ),
                                      HTML("td",
                                           child = Literal("01"),
                                           attrs = tdStyle,
                                      )]),
                                  attrs = trStyle),
                             HTML("tr",
                                  child = ListElement([
                                      HTML("td",
                                           child = Literal("10"),
                                           attrs = tdStyle,
                                      ),
                                      HTML("td",
                                           child = Literal("11"),
                                           attrs = tdStyle,
                                      )]),
                                  attrs = trStyle
                             )]
                            )))
assert assertEqual(compileGen(paragraph),paragraph)
assert assertEqual(compileGen(orderedList),
                   HTML(
                       "ol",
                       child = ListElement([
                           HTML(
                               "li",
                               child = Literal("elt1")
                           ),
                           HTML(
                               "li",
                               child = Literal("elt2")
                           )]
                       )
                   )
)
assert assertEqual(compileGen(unorderedList),HTML(
                       "ul",
                       child = ListElement([
                           HTML(
                               "li",
                               child = Literal("elt1")
                           ),
                           HTML(
                               "li",
                               child = Literal("elt2")
                           )]
                       )
                   ))

### Conditional
assert assertEqual(compileGen(filledFields),filledFields)
                       # MultipleRequirement(requireFilled = {"Question"},
                       #             child = Literal("Question is filled")))
assert assertEqual(compileGen(emptyField),emptyField)
                       # MultipleRequirement(requireFilled = {"Question"},
                       #             child = Literal("Question is empty")))
assert assertEqual(compileGen(questionField),
                   Literal("This is question side"))
assert assertEqual(compileGen(questionField, isQuestion = False),
                   emptyGen)
assert assertEqual(compileGen(answerField),
                   emptyGen)
assert assertEqual(compileGen(answerField, isQuestion = False),
                   Literal("This is answer side"))

assert assertEqual(compileGen(presentQuestion),Literal("Question is present in the model"))
assert assertEqual(compileGen(presentAbsent),emptyGen)
assert assertEqual(compileGen(absentQuestion),emptyGen)
assert assertEqual(compileGen(absentAbsent),Literal("Absent is absent in the model"))

assert assertEqual(compileGen(asked,asked = frozenset({"asked"})),Literal("is asked"))
assert assertEqual(compileGen(asked,asked = frozenset({})),emptyGen)
assert assertEqual(compileGen(notAsked,asked = frozenset({"asked"})),emptyGen)
assert assertEqual(compileGen(notAsked,asked = frozenset({})),Literal("is not asked"))
assert assertEqual(compileGen(notAsked, asked = frozenset({}), hide = frozenset({"asked"})),emptyGen)
assert assertEqual(compileGen(notAsked,hide = frozenset({"asked"})),emptyGen)
assert assertEqual(compileGen(asked,hide = frozenset({"asked"})),emptyGen)

assert assertEqual(compileGen(cascadeUseless, asked=frozenset()), Literal("Asked is not asked"))
assert assertEqual(compileGen(cascadeUseless, asked=frozenset(["cascaded"])), Literal("Asked is not asked"))
assert assertEqual(compileGen(cascadeUseless, asked=frozenset(["asked"])), Literal( "Asked is asked"))
assert assertEqual(compileGen(cascadeUseless, hide=frozenset(["cascaded"])), Literal("Asked is not asked"))
assert assertEqual(compileGen(cascadeUseless, hide=frozenset(["asked"])), emptyGen)
assert assertEqual(compileGen(cascade, asked=frozenset()), Literal("Cascaded is not asked"))
assert assertEqual(compileGen(cascade, asked=frozenset(["cascaded"])), Literal("Cascaded is asked"))
assert assertEqual(compileGen(cascade, asked=frozenset(["asked"])), Literal( "Cascaded is asked"))
assert assertEqual(compileGen(cascade, hide=frozenset(["cascaded"])), emptyGen)
assert assertEqual(compileGen(cascade, hide=frozenset(["asked"])), emptyGen)


## MultipleChildren
### List
listEmptyInexistingField_ = ensureGen(["foo",emptyGen,fieldFooClassless])
assert listEmptyInexistingField
assert listEmptyInexistingField.toKeep is not False
assert not listEmptyInexistingField.isEmpty()
assert assertEqual(listEmptyInexistingField.force(), listEmptyInexistingField_.force())
listEmptyInexistingFieldNormal = listEmptyInexistingField.getNormalForm()
listEmptyInexistingFieldWR = listEmptyInexistingField.getWithoutRedundance()
assert assertEqual(listEmptyInexistingField.force(), listEmptyInexistingFieldNormal.force())
assert assertEqual(listEmptyInexistingField.force(), listEmptyInexistingFieldWR.force())
assert assertEqual(compileGen(listEmptyInexistingField), literalFoo)

assert assertEqual(compileGen(listEmptyExistingField), ListElement([literalFoo, fieldQuestion]))




### QuestionOrAnswer
assert assertEqual(compileGen(qoa),Literal("question side"))
assert assertEqual(compileGen(qoa, isQuestion = False),Literal("answer side"))
assert assertEqual(compileGen(questionsRecursive),Literal("question side"))
assert assertEqual(compileGen(questionsRecursive, isQuestion = False),Literal("answer side"))

# Sugar
assert assertEqual(compileGen(parenthisedFoo),
                   ListElement(["(","foo",")"]))
# assert assertEqual(compileGen(emptyParenthesis),
#                    emptyGen) TODO when tokeep is precise
## Dichotomy
assert assertEqual(compileGen(filledOrEmpty),
                   ListElement([Filled(field = "Question", child = Literal(text = "Question is filled", ), ), Empty(field = "Question", child = Literal(text = "Question is empty", ), )], ))

assert assertEqual(compileGen(presentOrAbsentQuestion),Literal("Question is present in the model"))
assert assertEqual(compileGen(presentOrAbsentAbsent),Literal("Absent is absent from the model"))

### Asked or Not
assert assertEqual(compileGen(askedOrNot, asked = frozenset({"askedOrNot"})),Literal("Asked"))
assert assertEqual(compileGen(askedOrNot, asked = frozenset()),Literal(text = "notAsked", ))

## LabeledFields:
assert assertEqual(labeledFieldFromString,labeledFieldFromField)
assert assertEqual(labeledFieldFromStringLabel,labeledFieldFromFieldLabel)

## Label:
assert assertEqual(compileGen(labelBarForFieldFoo,
                              isQuestion=False),
                   Literal("bar"))
assert assertEqual(compileGen(labelBarForFieldFoo,
                              asked = {"foo"},
                              isQuestion=False),
                   Literal("bar"))
assert assertEqual(compileGen(labelBarForFieldFoo,
                              asked = {"foo"},
                              isQuestion=True),
                   CLASS(["Question","Emphasize", "foo"],Literal("bar")))
assert assertEqual(compileGen(labelBarForFieldFoo,
                              isQuestion = True),
                   Literal("bar"))

assert assertEqual(compileGen(labelBarForFieldsFoos),
                   Literal("bar"))
assert assertEqual(compileGen(labelBarForFieldsFoos,
                              isQuestion=False),
                   Literal("bar"))
assert assertEqual(compileGen(labelBarForFieldsFoos,
                              asked = {"foo"},
                              isQuestion=False),
                   Literal("bar"))
assert assertEqual(compileGen(labelBarForFieldsFoos,
                              asked = {"foo"},
                              isQuestion=True),
                   CLASS(["Question","Emphasize","foos"],Literal("bar")))

## Hide
assert assertEqual(compileGen(hideTest, asked = frozenset(), isQuestion = True), 
                   Literal("Content"))
assert assertEqual(compileGen(hideTest, asked = frozenset({"hide field"}), isQuestion = True), 
                   emptyGen)
assert assertEqual(compileGen(hideTest, asked = frozenset(), isQuestion = False), 
                   Literal("Content"))
assert assertEqual(compileGen(hideTest, asked = frozenset({"hide field"}), isQuestion = False), 
                   Literal("Content"))

## Fields
assert assertEqual(compileGen(questionnedField, asked = frozenset({"Question"})), 
                   Literal("???"))
assert assertEqual(compileGen(questionnedField, asked = frozenset()), 
                   Field("Question",addClass=False))
assert assertEqual(compileGen(questionnedField, isQuestion = False),
                   Field("Question",addClass=False))
assert assertEqual(
    compileGen(
        decoratedField,
        asked = frozenset({"Question"})),
    Filled(field = "Question",
           child = ListElement([
               CLASS(["Question","Emphasize", "Question"],Literal("Question")), Literal(": "), Literal("???"), br]
           )))
assert assertEqual(compileGen(decoratedField, asked = frozenset()), 
                   Filled(field = "Question",
                          child = ListElement([
                              Literal("Question"),
                              Literal(": "),
                              Field("Question",addClass=False),
                              br]
                          )))
assert assertEqual(compileGen(decoratedField, isQuestion = False),
                   Filled(field = "Question",
                          child = ListElement([
                              Literal("Question"),
                              Literal(": "),
                              Field("Question",addClass=False),
                              br]
                          )))
## FromAndTo
# assert assertEqual(compileGen(frenchToEnglish, fields={"Français","English"}),
#                    Filled("English",
#                           Filled("Français",
#                                  ListElement([ListElement([Field("English"),
#                                                            Literal(" in ")]),
#                                               Literal("French"),
#                                               Literal(" is "),
#                                               Field("Français",addClass=False),
#                                               br]
#                                  )
#                           )
#                    )
# )
assert assertEqual(compileGen(EnglishToFrench, fields={"Français","English"}),
                   Filled("Français",
                          Filled("English",
                                 ListElement([ListElement([HTML("span",
  attrs = {'class': 'English'},
  child = Field(field = "English",
    addClass = False,),),
                                                           Literal(" in ")]),
                                              CLASS(["Question","Emphasize","Français"],
                                                    Literal("French")),
                                              Literal(" is "),
                                              Literal("???"),
                                              br]
                                 )
                          )
                   )
)
assert assertEqual(compileGen(EnglishToFrench, fields={"Français","English"},isQuestion = False),
                   Filled("Français",
                          Filled("English",
                                 ListElement([ListElement([HTML("span",
  attrs = {'class': 'English'},
  child = Field(field = "English",
    addClass = False,),),
                                                           Literal(" in ")]),
                                              Literal("French"),
                                              Literal(" is "),
                                              CLASS(["Answer","Emphasize","Français"],
                                                    Field("Français",addClass=False)
                                              ),
                                              br]
                                 )
                          )
                   )
)

## Numbers
assert assertEqual(compileGen(atLeastOneQuestion),
                   Filled(field = "Question", child = Literal(text = "At least one", ), ))

assert assertEqual(compileGen(atLeastTwoQuestion),
                   emptyGen)
assert assertEqual(atLeastOneDefinition.getNormalForm(),
                   ListElement([
                       Filled(
                           field = 'Definition3',
                           child = Literal(text = "At least one", ),
                       ),
                       Empty(
        field = 'Definition3',
        child = ListElement([
            Filled(
                field = 'Definition2',
                child = Literal(text = "At least one", ),
            ),
            Empty(
                field = 'Definition2',
                child = Filled(
                    field = 'Definition',
                    child = Literal(text = "At least one", ),
                ),
            )],
        ),
    )],
))

assert assertEqual(compileGen(atLeastTwoDefinition),#this is false, 
ListElement([
  Filled(
    field = 'Definition3',
    child = ListElement([
      Filled(
        field = 'Definition2',
        child = Literal(text = "At least two", ),
          ),
      Empty(
        field = 'Definition2',
        child = Filled(
          field = 'Definition',
          child = Literal(text = "At least two", ),
            ),
          )],
        ),
      ),
  Empty(
    field = 'Definition3',
    child = Filled(
      field = 'Definition2',
      child = Filled(
        field = 'Definition',
        child = Literal(text = "At least two", ),
          ),
        ),
      )],
    )
)

## Conditionals

### ToAsk
assert assertEqual(toask.getQuestions(),['Definition','Definition2'])
assert toask.getQuestionToAsk("model name") in ['Definition','Definition2']
toask.assumeAsked("Definition","model name")
assert assertEqual(toask.getQuestionToAsk("model name"),'Definition2')
toask.assumeAsked("Definition2","model name")
assert assertEqual(toask.getQuestionToAsk("model name"),None)


### MultipleRequirement
assert assertEqual(compileGen(requireQuestion),Filled(
  field = 'Question',
  child = Literal(text = "Question", ),
))
assert assertEqual(compileGen(requirements3),
                   Empty(
  field = 'Definition3',
  child = Filled(
    field = 'Question',
    child = Literal(text = "Foo",))))
# assert assertEqual(compileGen(contradictionRequirement), emptyGen)
assert assertEqual(compileGen(requiringInexistant),emptyGen)
## List Fields

# assert assertEqual(compileGen(twoQuestionsAsList, asked =frozenset()),
#                    compileGen([["Definition", ": ", Field("Definition",addClass=False)],["Definition2", ": ", Field("Definition2",addClass=False)]]))
# assert assertEqual(compileGen(twoQuestionsAsList, asked ={"Definition"}, isQuestion = False),
#                    compileGen([["Definition", ": ", Field("Definition",addClass=False)],["Definition2", ": ", Field("Definition2",addClass=False)]]))
# assert assertEqual(compileGen(twoQuestionsAsList, asked ={"Definition"}),
#                    compileGen([["Definition", ": ", Literal("???")],["Definition2", ": ", Field("Definition2",addClass=False)]]))

# assert assertEqual(compileGen(twoQuestionsAsNamedList, asked =frozenset()),
#                    compileGen([["Definition", ": ", Field("Definition",addClass=False)],["Definition2", ": ", Field("Definition2",addClass=False)]]))
# assert assertEqual(compileGen(twoQuestionsAsNamedList, asked ={"Definition"}, isQuestion = False),
#                    compileGen([["Definition", ": ", Field("Definition",addClass=False)],["Definition2", ": ", Field("Definition2",addClass=False)]]))
# assert assertEqual(compileGen(twoQuestionsAsNamedList, asked ={"Definition"}),
#                    compileGen([["Definition", ": ", Literal("???")],["Definition2", ": ", Field("Definition2",addClass=False)]]))
# assert assertEqual(compileGen(twoQuestionsAsNamedList, asked ={"ListName"}),
#                    compileGen([["Definition", ": ", Literal("???")],["Definition2", ": ", Literal("???")]]))

assert assertEqual(
    compileGen(
        twoQuestionsAsTable,
        asked =frozenset(),
        fields={"Definition","Definition2", "Name","Name2"}
    ),
    tableTwoShown
)
                   
assert assertEqual(
    compileGen(
        twoQuestionsAsTable,
        asked =frozenset({"Definition"}),
        isQuestion = False,
        fields={"Definition","Definition2", "Name","Name2"}
    ),
    tableTwoShownAnswer1
)
                   
assert assertEqual(compileGen(twoQuestionsAsTable,
                              asked =frozenset({"Definition"}),
                              fields={"Definition","Definition2", "Name","Name2"}),
                   tableTwoShownQuestion1)
assert assertEqual(compileGen(twoQuestionsAsTable,
                              asked =frozenset({"Definitions"}),
                              fields={"Definition","Definition2", "Name","Name2"}),
                   tableTwoShownQuestionAll)
assert assertEqual(compileGen(twoQuestionsAsTable,
                              asked =frozenset({"Definitions"}),
                              fields={"Definition","Definition2", "Name","Name2"},
                              isQuestion = False),
                   tableTwoShownAnswerAll)

### Table 3 columns
assert assertEqual(
    compileGen(
        fourQuestionsAsTable,
        asked =frozenset(),
        fields={"Definition","Definition2", "Name","Name2"}
    ),
    tableFourShown
)
                   
assert assertEqual(
    compileGen(
        fourQuestionsAsTable,
        asked =frozenset({"Definition"}),
        isQuestion = False,
        fields={"Definition","Definition2", "Name","Name2"},
    ),
    tableFourShownAnswer1
)
                   
assert assertEqual(
    compileGen(
        fourQuestionsAsTable,
        fields={"Definition","Definition2", "Name","Name2"},
        asked =frozenset({"Definition"})),
    tableFourShownQuestion1)

assert assertEqual(
    compileGen(fourQuestionsAsTable,
               fields={"Definition","Definition2","Name","Name2"},
               asked = frozenset({"Definitions"})),
    tableFourShownQuestionAll)

assert assertEqual(compileGen(fourQuestionsAsTable,
                              fields={"Definition","Definition2", "Name", "Name2"},
                              asked = frozenset({"Definitions"}),
                              isQuestion = False),
                   tableFourShownAnswerAll)

### Numbered
assert assertEqual(compileGen(twoQuestionsNumbered, asked =frozenset()),
                   twoQuestionsNumberedShown)
assert assertEqual(compileGen(twoQuestionsNumbered, asked =frozenset({"Definition"}), isQuestion = False),
                   twoQuestionsNumberedShown1Answer)
assert assertEqual(compileGen(twoQuestionsNumbered, asked =frozenset({"Definition"})),
                   twoQuestionsNumberedShown1Question)
assert assertEqual(compileGen(twoQuestionsNumbered, asked =frozenset({"Definitions"})),
                   twoQuestionsNumberedAllAsked)
assert assertEqual(compileGen(twoQuestionsNumbered, asked =frozenset({"Definitions"}), isQuestion = False),
                   twoQuestionsNumberedAllAnswer)

assert assertEqual(compileGen(twoQuestionsNumbered,
                              asked =frozenset({"Definition"}),
                              mandatory = frozenset({"Definition"})),
                   twoQuestionsNumberedAskDefinitionMandatory)
## For debugging
decreaseRelation = Parenthesis(left = " ",
                               right = " ",
                               child = QuestionnedField(field = "Greater to smaller",
                                                        child = FilledOrEmpty("Greater to smaller",
                                                                              {"Greater to smaller"},
                                                                              FilledOrEmpty( "Smaller to greater",
                                                                                            {"Smaller to greater"},
                                                                                            "implied by"))))
