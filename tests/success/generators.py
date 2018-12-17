# List of templates which must be equals
from ...debug import assertEqual
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
assert assertEqual(fieldFoo_, fieldFoo)
assert fieldFoo  !=  Literal("test")
assert fieldFoo !=  Literal("{{foo}}")
assert assertEqual(fieldFoo, Field('foo'))
assert assertEqual(fieldFoo, fieldFoo.getNormalForm())
assert assertEqual(fieldFoo, fieldFoo.getWithoutRedundance())
assert not fieldFoo.isEmpty()
assert fieldFoo.toKeep
assert fieldFoo
assert assertEqual(compileGen(fieldFoo), emptyGen)
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
assert assertEqual(compileGen(filledField),filledField)
                       # Requirement(requireFilled = {"Question"},
                       #             child = Literal("Question is filled")))
assert assertEqual(compileGen(emptyField),emptyField)
                       # Requirement(requireFilled = {"Question"},
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



## MultipleChildren
### List
listEmptyInexistingField_ = ensureGen(["foo",emptyGen,fieldFoo])
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

assert singletonList

### Name
assert assertEqual(compileGen(name, asked = frozenset({"name"})),Literal("Asked"))
assert assertEqual(compileGen(recursiveName, asked = frozenset({"name"})),ListElement(elements = [Literal(text = "prefix", ), Literal(text = "Asked", ), Literal(text = "suffix", )], ))
assert assertEqual(compileGen(name, asked = frozenset()),Literal(text = "notAsked", ))
assert assertEqual(compileGen(recursiveName, asked = frozenset()),Literal(text = "notAsked", ))

### QuestionOrAnswer
assert assertEqual(compileGen(qoa),Literal("question side"))
assert assertEqual(compileGen(qoa, isQuestion = False),Literal("answer side"))
assert assertEqual(compileGen(questionsRecursive),Literal("question side"))
assert assertEqual(compileGen(questionsRecursive, isQuestion = False),Literal("answer side"))

# Sugar
## Dichotomy
assert assertEqual(compileGen(filledOrEmpty),
                   ListElement([Filled(field = "Question", child = Literal(text = "Question is filled", ), ), Empty(field = "Question", child = Literal(text = "Question is empty", ), )], ))

assert assertEqual(compileGen(presentOrAbsentQuestion),Literal("Question is present in the model"))
assert assertEqual(compileGen(presentOrAbsentAbsent),Literal("Absent is absent from the model"))
## Fields
assert assertEqual(compileGen(questionnedField, asked = frozenset({"Question"})), 
                   Literal("???"))
assert assertEqual(compileGen(questionnedField, asked = frozenset()), 
                   Field("Question"))
assert assertEqual(compileGen(questionnedField, isQuestion = False),
                   Field("Question"))
assert assertEqual(compileGen(decoratedField, asked = frozenset({"Question"})), 
                   ListElement([
                       Literal("Question"),
                       Literal(": "),
                       Literal("???")]
                   ))
assert assertEqual(compileGen(decoratedField, asked = {}), 
                   ListElement([
                       Literal("Question"),
                       Literal(": "),
                       Field("Question")]
                   ))
assert assertEqual(compileGen(decoratedField, isQuestion = False),
                   ListElement([
                       Literal("Question"),
                       Literal(": "),
                       Field("Question")]
                   ))

## Numbers
assert assertEqual(compileGen(atLeastOneQuestion),
                   Filled(field = "Question", child = Literal(text = "At least one", ), ))

assert assertEqual(compileGen(atLeastTwoQuestion),
                   emptyGen)
assert assertEqual(atLeastOneDefinition.getNormalForm(),
ListElement(elements = [Filled(field = "Definition3", child = Literal(text = "At least one", ), ), Empty(field = "Definition3", child = ListElement(elements = [Filled(field = "Definition2", child = Literal(text = "At least one", ), ), Empty(field = "Definition2", child = ListElement(elements = [Filled(field = "Definition", child = Literal(text = "At least one", ), ), Empty(field = "Definition", child = emptyGen, )], ), )], ), )], ) )

assert assertEqual(compileGen(atLeastTwoDefinition),#this is false, 
                   ListElement([
                       Requirement(requireFilled = {"Definition"},
                                   child = Literal("At least two")),
                       Requirement(requireEmpty = {"Definition"},
                                   child = 
                                   ListElement([
                                       Requirement(requireFilled = {"Definition2"},
                                                   child = Literal("At least two")),
                                       Requirement(requireEmpty = {"Definition2"},
                                                   child = 
                                                   ListElement([
                                                       Requirement(requireFilled = {"Definition3"},
                                                                   child = Literal("At least two")),
                                                   ])                                                   
                                       ),
                                   ])
                       ),
                   ])
)

## Conditionals

### Requirement
assert assertEqual(compileGen(requireQuestion),requireQuestion)
assert assertEqual(compileGen(requirements3),
                   Requirement(
                       child = Literal(text = "Foo", ),
                       requireFilled = frozenset({'Question'}),
                       requireEmpty = frozenset({'Definition3'})
                   )
)
assert assertEqual(contradictionRequirement.getNormalForm(), emptyGen)
assert assertEqual(compileGen(requiringInexistant),emptyGen)
## List Fields
assert assertEqual(fieldToPair("field"), ("field",Field("field")))
assert assertEqual(fieldToPair(("label","field")), ("label","field"))
assert assertEqual(fieldToPair(Field("field")), ("field",Field("field")))

assert assertEqual(compileGen(twoQuestionsAsList, asked ={}),
                   compileGen([["Definition", ": ", Field("Definition")],["Definition2", ": ", Field("Definition2")]]))
assert assertEqual(compileGen(twoQuestionsAsList, asked ={"Definition"}, isQuestion = False),
                   compileGen([["Definition", ": ", Field("Definition")],["Definition2", ": ", Field("Definition2")]]))
assert assertEqual(compileGen(twoQuestionsAsList, asked ={"Definition"}),
                   compileGen([["Definition", ": ", Literal("???")],["Definition2", ": ", Field("Definition2")]]))

assert assertEqual(compileGen(twoQuestionsAsNamedList, asked ={}),
                   compileGen([["Definition", ": ", Field("Definition")],["Definition2", ": ", Field("Definition2")]]))
assert assertEqual(compileGen(twoQuestionsAsNamedList, asked ={"Definition"}, isQuestion = False),
                   compileGen([["Definition", ": ", Field("Definition")],["Definition2", ": ", Field("Definition2")]]))
assert assertEqual(compileGen(twoQuestionsAsNamedList, asked ={"Definition"}),
                   compileGen([["Definition", ": ", Literal("???")],["Definition2", ": ", Field("Definition2")]]))
assert assertEqual(compileGen(twoQuestionsAsNamedList, asked ={"ListName"}),
                   compileGen([["Definition", ": ", Literal("???")],["Definition2", ": ", Literal("???")]]))

assert assertEqual(
    compileGen(
        twoQuestionsAsTable,
        asked ={}
    ),
    compileGen(
        Table(
            [
                ["Definition", Field("Definition")],
                ["Definition2", Field("Definition2")]]
        )
    )
)
                   
assert assertEqual(
    compileGen(
        twoQuestionsAsTable,
        asked ={"Definition"},
        isQuestion = False
    ),
    compileGen(
        Table(
            [
                [
                    "Definition",
                    Field("Definition")
                ],
                [
                    "Definition2",
                    Field("Definition2")
                ]
            ]
        )
    )
)
                   
assert assertEqual(compileGen(twoQuestionsAsTable, asked ={"Definition"}),
                   compileGen(Table([["Definition", Literal("???")],["Definition2", Field("Definition2")]])))


assert assertEqual(compileGen(twoQuestionsNumbered, asked ={}),
                   compileGen(["Definition", ":", UL([Field("Definition"), Field("Definition2")])]))
assert assertEqual(compileGen(twoQuestionsNumbered, asked ={"Definition"}, isQuestion = False),
                   compileGen(["Definition", ":", UL([Field("Definition"), Field("Definition2")])]))
assert assertEqual(compileGen(twoQuestionsNumbered, asked ={"Definition"}),
                   compileGen(["Definition", ":", UL([Field("???"), Field("Definition2")])]))
assert assertEqual(compileGen(twoQuestionsNumbered, asked ={"ListName"}),
                   compileGen(["Definition", ":", UL([Field("???"), Field("???")])]))

