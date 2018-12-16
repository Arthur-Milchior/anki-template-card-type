from ..imports import *
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
table = Table([["00","01"],["10","11"]], trAttrs = {"class":"trStyle"}, tdAttrs = {"class":"tdStyle"})
paragraph = P("Paragraph content")
htmlList = List(["elt1", "elt2"])

### Requirement
requireQuestion =Requirement(child = (Literal("Question")),
                             requireFilled = frozenset({"Question"}))
requirements3 = Requirement(child = (Literal("Foo")),
                            requireFilled = frozenset({"Question"}),
                            requireEmpty = frozenset({"Definition3", "AbsentFromModel"}))

contradictionRequirement = Requirement(child = (Literal("Foo")),
                                       requireFilled = frozenset({"Question"}),
                                       requireEmpty = frozenset({"Question"}))
requiringInexistant = Requirement(child = (Literal("Foo")),
                                  requireFilled = frozenset({"absentfrommodel"}))

## MultipleChildren
### List
listEmptyInexistingField = ListElement([literalFoo, emptyGen, fieldFoo]) #foofo
listEmptyExistingField = ListElement([literalFoo, emptyGen, fieldQuestion]) #fooQuestion
singletonList = ensureGen([Field('foo')]) #fooList
twoQuestionsListed = ListElement([DecoratedField('Definition1'),DecoratedField('Definition2')]) #similar to twoQuestionsListedAsFields

### Name
name = Name(name = "name", asked = "Asked", notAsked = "notAsked")
recursiveName = Name(name = "name", asked = ["prefix", Name(name = "recursiveName", asked = "Asked", notAsked = "notAskedRecursive", cascadeAsked = frozenset({"recu"})), "suffix"], notAsked = "notAsked", cascadeAsked = frozenset({"recu"}))

### QuestionOrAnswer
qoa = QuestionOrAnswer(question = "question side", answer = "answer side")
questionsRecursive = QuestionOrAnswer(question = QuestionOrAnswer(question = "question side", answer = "deleted side"), answer = "answer side")

# Sugar
## Numbers
filleOrEmpty = FilledOrEmptyField(field = "Question",
                                  filledCase = "Filled",
                                  emptyCase = "Empty")
atLeastOneField = AtLeastOneField(child = "At least one",
                                  fields = frozenset({Question1, Question2, Question3}))
atLeastTwoField = AtLeastOneField(child = "At least two",
                                  fields = frozenset({Question1, Question2, Question3}))

## Conditionals
branch = Branch(name="Question", questionAsked = "???", default = Field("Question"))
filledOrEmpty = FilledOrEmptyField(field = "Question",
                                   filledCase = "Question is filled",
                                   emptyCase = "Question is empty")
filledField = FilledField(field = "Question",
                          child = "Question is filled")
emptyField = EmptyField(field = "Question",
                        child = "Question is empty")
questionField = QuestionField(field = "Question",
                              child = "This is question side")
answerField = AnswerField(field = "Answer",
                          child = "This is answer side")
presentOrAbsentQuestion = PresentOrAbsentField(
    field = "Question",
    presentCase = "Question is present in the model",
    presentCase = "Question is absent from the model")
presentOrAbsentAbsent = PresentOrAbsentField(
    field = "Absent",
    presentCase = "Absent is present in the model",
    presentCase = "Absent is absent from the model")
presentQuestion = presentField(
    field = "Question",
    child = "Question is present in the model")
presentAbsent = presentField(
    field = "Absent",
    child = "Absent is present in the model")
absentQuestion = absentField(
    field = "Question",
    child = "Question is absent in the model")
absentAbsent = absentField(
    field = "Absent",
    child = "Absent is absent in the model")

## Fields
questionnedField =QuestionnedField('Question')
decoratedField = DecoratedField('Question')

## List Fields
assert assertEqual("""fieldToPair("field")""", """("field",Field("field"))""")
assert assertEqual("""fieldToPair(("label","field"))""", """("label","field")""")
assert assertEqual("""fieldToPair(Field("field"))""", """("field",Field("field"))""")

twoQuestionsAsList = ListFields(['Definition1', 'Definition2'])
twoQuestionsAsNamedList = ListFields(['Definition1', 'Definition2'], "ListName")
twoQuestionsAsTable = TableFields(['Definition1', 'Definition2'])
twoQuestionsNumbered = NumberedFields('Definition', 2)
