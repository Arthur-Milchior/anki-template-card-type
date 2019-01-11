from ...generators.imports import *
#Core
## Leaf 
### Empty
none = ensureGen(None)

### Literal
literalTest = Literal("test")
literalFoo = Literal("foo")

### Field
fieldFoo = Field("foo")
fieldQuestion = Field("Question")
fieldFoo_ = ensureGen(Field('foo'))

## SingleChild
### HTML
image = Image("http://www.foo.bar")
table = Table(
    [["00","01"],
     ["10","11"]
    ],
    trAttrs = {"class":"trStyle"},
    tdAttrs = {"class":"tdStyle"}
)

paragraph = P(child = "Paragraph content")
orderedList = OL(elements = ["elt1", "elt2"])
unorderedList = UL(elements = ["elt1", "elt2"])

### Conditionals
filledField = Filled(field = "Question",
                          child = "Question is filled")
emptyField = Empty(field = "Question",
                        child = "Question is empty")
questionField = Question(child = "This is question side")
answerField = Answer(child = "This is answer side")
presentQuestion = Present(
    field = "Question",
    child = "Question is present in the model")
presentAbsent = Present(
    field = "Absent",
    child = "Absent is present in the model")
absentQuestion = Absent(
    field = "Question",
    child = "Question is absent in the model")
absentAbsent = Absent(
    field = "Absent",
    child = "Absent is absent in the model")

## LabeledFields:
labeledFieldFromString = LabeledField("foo")
labeledFieldFromField = LabeledField(Field("foo"))
labeledFieldFromStringLabel = LabeledField("foo","bar")
labeledFieldFromFieldLabel = LabeledField(Field("foo"),"bar")

## MultipleChildren
### List
listEmptyInexistingField = ListElement([literalFoo, emptyGen, fieldFoo]) #foofo
listEmptyExistingField = ListElement([literalFoo, emptyGen, fieldQuestion]) #fooQuestion
singletonList = ensureGen([Field('foo')]) #fooList
twoQuestionsListed = ListElement([DecoratedField('Definition1'),DecoratedField('Definition2')]) #similar to twoQuestionsListedAsFields

### Asked or Not
asked = Asked(field = "asked", child = "is asked")
notAsked = NotAsked(field = "asked", child = "is not asked")
cascadeUseless = Cascade(field ="asked", cascade = ["cascaded"], child = AskedOrNot("asked", "Asked is asked","Asked is not asked"))
cascade = Cascade(field ="asked", cascade = ["cascaded"], child = AskedOrNot("cascaded", "Cascaded is asked","Cascaded is not asked"))

### QuestionOrAnswer
qoa = QuestionOrAnswer(question = "question side", answer = "answer side")
questionsRecursive = QuestionOrAnswer(question = QuestionOrAnswer(question = "question side", answer = "deleted side"), answer = "answer side")

# Sugar
parenthisedFoo = Parenthesis("foo")
emptyParenthesis = Parenthesis(None)
### Dichotomy
filledOrEmpty = FilledOrEmpty(field = "Question",
                                   filledCase = "Question is filled",
                                   emptyCase = "Question is empty")
presentOrAbsentQuestion = PresentOrAbsent(
    field = "Question",
    presentCase = "Question is present in the model",
    absentCase = "Question is absent from the model")
presentOrAbsentAbsent = PresentOrAbsent(
    field = "Absent",
    presentCase = "Absent is present in the model",
    absentCase = "Absent is absent from the model")
askedOrNot = AskedOrNot(field = "askedOrNot", asked = "Asked", notAsked = "notAsked")


##Label
labelBarForFieldFoo = Label("bar",["foo"],["foo"])
labelBarForFieldsFoos = Label("bar",["foos","foo","foo2"],["foos"])
## Fields
questionnedField =QuestionnedField('Question')
decoratedField = DecoratedField('Question')
## FromAndTo
EnglishToFrench = FromAndTo("English"," in ","French"," is ","Français")

## Numbers
atLeastOneQuestion = AtLeastOneField(child = "At least one",
                                  fields = (["Question", "Question2", "Question3"]))
atLeastOneDefinition = AtLeastOneField(child = "At least one",
                                  fields = (["Definition", "Definition2", "Definition3"]))
twoOfTwo = AtLeastTwoFields(child = "At least two",
                            fields = (["Question", "Question2"]))
atLeastTwoQuestion = AtLeastTwoFields(child = "At least two",
                                    fields = (["Question", "Question2", "Question3"]))
atLeastTwoDefinition = AtLeastTwoFields(child = "At least two",
                                    fields = (["Definition", "Definition2", "Definition3"]))

### Requirement
requireQuestion =Filled(field = "Question",
                        child = (Literal("Question")))
requirements3 = MultipleRequirement(child = "Foo",
                            requireFilled = frozenset({"Question"}),
                            requireEmpty = frozenset({"Definition3", "AbsentFromModel"}))

try:
    contradictionRequirement = MultipleRequirement(child = (Literal("Foo")),
                                                   requireFilled = frozenset({"Question"}),
                                                   requireEmpty = frozenset({"Question"}))
    assert False
except Inconsistent:
    pass
requiringInexistant = MultipleRequirement(child = (Literal("Foo")),
                                  requireFilled = frozenset({"absentfrommodel"}))

## Conditionals
#branch = Branch(name="Question", questionAsked = "???", default = Field("Question"))
## List Fields

twoQuestionsAsTable = TableFields(['Definition', 'Definition2'], name="Definitions")
tableTwoLine1 = Filled(
    field = 'Definition',
    child = HTML(
        child = ListElement([
            HTML(
                child = Literal(text = "Definition",),
                tag = 'td'),
            HTML(
                child = Field(field = "Definition"),
                tag = 'td')],),
        tag = 'tr'),)
tableTwoLine1Answered = Filled(
    field = 'Definition',
    child = HTML(
        child = ListElement([
            HTML(
                child = Literal(text = "Definition",),
                tag = 'td'),
            HTML(
                child = CLASS(["Answer", "Definition"],Field(field = "Definition")),
                tag = 'td')],),
        tag = 'tr'),)
tableTwoLine2Answered = Filled(
    field = 'Definition2',
    child = HTML(
        child = ListElement([
            HTML(
                child = Literal(text = "Definition2",),
                tag = 'td'),
            HTML(
                child = CLASS(["Answer", "Definition2"],Field(field = "Definition2")),
                tag = 'td')],),
        tag = 'tr'),)
tableTwoLine1Question = Filled(
    field = 'Definition',
    child = HTML(
        child = ListElement([
            HTML(
                child = CLASS(["Question", "Definition"],Literal(text = "Definition",)),
                tag = 'td'),
            HTML(
                child = Literal("???"),
                tag = 'td')],),
        tag = 'tr'),)
tableTwoLine2Question = Filled(
    field = 'Definition2',
    child = HTML(
        child = ListElement([
            HTML(
                child = CLASS(["Question", "Definition2"],Literal(text = "Definition2",)),
                tag = 'td'),
            HTML(
                child = Literal("???"),
                tag = 'td')],),
        tag = 'tr'),)
tableTwoLine2 = Filled(
    field = 'Definition2',
    child = HTML(
        child = ListElement([
            HTML(
                child = Literal(text = "Definition2",),
                tag = 'td'),
            HTML(
                child = Field(field = "Definition2"),
                tag = 'td')],),
        tag = 'tr'),)

tableTwoShown= HTML(
        child = ListElement([
            tableTwoLine1,
            tableTwoLine2
        ]),
    tag = 'table')

tableTwoShownQuestion1= HTML(
        child = ListElement([
            tableTwoLine1Question,
            tableTwoLine2
        ]),
    tag = 'table')
tableTwoShownQuestionAll= HTML(
        child = ListElement([
            tableTwoLine1Question,
            tableTwoLine2Question
        ]),
    tag = 'table')
tableTwoShownAnswer1= HTML(
        child = ListElement([
            tableTwoLine1Answered,
            tableTwoLine2
        ]),
    tag = 'table')
tableTwoShownAnswerAll= HTML(
        child = ListElement([
            tableTwoLine1Answered,
            tableTwoLine2Answered
        ]),
    tag = 'table')

### Numbered
twoQuestionsNumbered = NumberedFields('Definition', 2)
twoQuestionsNumberedLine1 = Filled(
    field = 'Definition',
    child = HTML("li",
                 child =Field(field = "Definition",),),)
twoQuestionsNumberedLine1Question = Filled(
    field = 'Definition',
    child = HTML("li",
                 child =Literal("???",),),)
twoQuestionsNumberedLine2Question = Filled(
    field = 'Definition2',
    child = HTML("li",
                 child =Literal("???",),),)
twoQuestionsNumberedLine1Answer = Filled(
    field = 'Definition',
    child = HTML("li",
                 child =CLASS(["Answer","Definition"],Field(field = "Definition",),),))
twoQuestionsNumberedLine2Answer = Filled(
    field = 'Definition2',
    child = HTML("li",
                 child =CLASS(["Answer","Definition"],Field(field = "Definition2",),),))
twoQuestionsNumberedLine2 = Filled(
    field = 'Definition2',
    child = HTML("li",
                 child =Field(field = "Definition2",),),)

twoQuestionsNumberedShown = ListElement([
  Literal(text = "Definitions",),
  Literal(text = ": ",),
    HTML("ol",
         child = ListElement([
             twoQuestionsNumberedLine1,
             twoQuestionsNumberedLine2
         ],),)],)
labelQuestion=CLASS(["Question", "Definitions"],
                    Literal(text = "Definitions",)
                    )
labelNormal= Literal(text = "Definitions",)
twoQuestionsNumberedShown1Question = ListElement([
  labelQuestion,
  Literal(text = ": ",),
    HTML("ol",
         child = ListElement([
             twoQuestionsNumberedLine1Question,
             twoQuestionsNumberedLine2
         ],),)],)
twoQuestionsNumberedShown1Answer = ListElement([
  labelNormal,
  Literal(text = ": ",),
    HTML("ol",
         child = ListElement([
             twoQuestionsNumberedLine1Answer,
             twoQuestionsNumberedLine2
         ],),)],)

twoQuestionsNumberedAskDefinitionMandatory = Filled(
  field = 'Definition',
  child = ListElement([
    HTML("span",
      attrs = {'class': 'Question Definitions'},
      child = Literal(text = "Definitions",),),
    Literal(text = ": ",),
    HTML("ol",
      child = ListElement([
        HTML("li",
          child = Literal(text = "???",),),
        Filled(
          field = 'Definition2',
          child = HTML("li",
            child = Field(field = "Definition2",),),)],),)],),)

twoQuestionsNumberedAllAsked = ListElement([
  labelQuestion,
  Literal(text = ": ",),
  HTML("ol",
    child = ListElement([
      twoQuestionsNumberedLine1Question,
      twoQuestionsNumberedLine2Question,
    ],),)],)
twoQuestionsNumberedAllAnswer = ListElement([
  labelNormal,
  Literal(text = ": ",),
  HTML("ol",
    child = ListElement([
      twoQuestionsNumberedLine1Answer,
      twoQuestionsNumberedLine2Answer,
    ],),)],)


