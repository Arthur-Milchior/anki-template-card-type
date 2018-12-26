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

## MultipleChildren
### List
listEmptyInexistingField = ListElement([literalFoo, emptyGen, fieldFoo]) #foofo
listEmptyExistingField = ListElement([literalFoo, emptyGen, fieldQuestion]) #fooQuestion
singletonList = ensureGen([Field('foo')]) #fooList
twoQuestionsListed = ListElement([DecoratedField('Definition1'),DecoratedField('Definition2')]) #similar to twoQuestionsListedAsFields

### Asked or Not
asked = Asked(field = "asked", child = "is asked")
notAsked = NotAsked(field = "asked", child = "is not asked")

### QuestionOrAnswer
qoa = QuestionOrAnswer(question = "question side", answer = "answer side")
questionsRecursive = QuestionOrAnswer(question = QuestionOrAnswer(question = "question side", answer = "deleted side"), answer = "answer side")

# Sugar
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

## Fields
questionnedField =QuestionnedField('Question')
decoratedField = DecoratedField('Question')

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

contradictionRequirement = MultipleRequirement(child = (Literal("Foo")),
                                       requireFilled = frozenset({"Question"}),
                                       requireEmpty = frozenset({"Question"}))
requiringInexistant = MultipleRequirement(child = (Literal("Foo")),
                                  requireFilled = frozenset({"absentfrommodel"}))

## Conditionals
#branch = Branch(name="Question", questionAsked = "???", default = Field("Question"))
## List Fields

#twoQuestionsAsList = ListFields(fields = ['Definition', 'Definition2'])
#twoQuestionsAsNamedList = ListFields(['Definition', 'Definition2'], "ListName")
twoQuestionsAsTable = TableFields(['Definition', 'Definition2'])
tableTwoShown= HTML(
        child = ListElement([
            Filled(
                field = 'Definition',
                child = HTML(
                    child = ListElement([
                        HTML(
                            child = Literal(text = "Definition",),
                            tag = 'td'),
                        HTML(
                            child = Field(field = "Definition"),
                            tag = 'td')],),
                    tag = 'tr'),),
            Filled(
                field = 'Definition2',
                child = HTML(
                    child = ListElement([
                        HTML(
                            child = Literal(text = "Definition2",),
                            tag = 'td'),
                        HTML(
                            child = Field(field = "Definition2"),
                            tag = 'td')],),
                    tag = 'tr'),)],),
        tag = 'table')
tableTwoQuestionned= HTML(
        child = ListElement([
            Filled(
                field = 'Definition',
                child = HTML(
                    child = ListElement([
                        HTML(
                            child = Literal(text = "Definition",),
                            tag = 'td'),
                        HTML(
                            child = Literal(text = "???",),
                            tag = 'td')],),
                    tag = 'tr'),),
            Filled(
                field = 'Definition2',
                child = HTML(
                    child = ListElement([
                        HTML(
                            child = Literal(text = "Definition2",),
                            tag = 'td'),
                        HTML(
                            child = Field(field = "Definition2"),
                            tag = 'td')],),
                    tag = 'tr'),)],),
        tag = 'table')

twoQuestionsNumbered = NumberedFields('Definition', 2)
twoQuestionsNumberedShown = ListElement([
  Literal(text = "Definitions",),
  Literal(text = ": ",),
  HTML("ul",
    child = ListElement([
      HTML("li",
        child = Filled(
          field = 'Definition',
          child = Field(field = "Definition",),),),
      HTML("li",
        child = Filled(
          field = 'Definition2',
          child = Field(field = "Definition2",),),)],),)],)
twoQuestionsNumberedAskDefinition = ListElement([
  Literal(text = "Definitions",),
  Literal(text = ": ",),
  HTML("ul",
    child = ListElement([
      HTML("li",
        child = Filled(
          field = 'Definition',
          child = Literal("???"),),),
      HTML("li",
        child = Filled(
          field = 'Definition2',
          child = Field(field = "Definition2",),),)],),)],)

twoQuestionsNumberedAskDefinitionMandatory = Filled(
    field = 'Definition',
    child = ListElement([
        Literal(text = "Definitions",),
        Literal(text = ": ",),
        HTML("ul",
             child = ListElement([
                 HTML("li",
                      child = Literal("???"),),
                 HTML("li",
                      child = Filled(
                          field = 'Definition2',
                          child = Field(field = "Definition2",),),)],),)],))
    
twoQuestionsNumberedAllAsked = ListElement([
  Literal(text = "Definitions",),
  Literal(text = ": ",),
  HTML("ul",
    child = ListElement([
      HTML("li",
        child = Filled(
          field = 'Definition',
          child = Literal("???"),),),
      HTML("li",
        child = Filled(
          field = 'Definition2',
          child = Literal("???"),),)],),)],)


