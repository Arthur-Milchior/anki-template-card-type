from ...generators import *

# Core
# Leaf
# Empty
none = ensureGen(None)

# Literal
literalTest = Literal("test")
literalFoo = Literal("foo")

# Field
fieldFooClass = Field("foo")
fieldFooClassless = Field("foo", useClasses=False)
fieldQuestion = Field("Question", useClasses=False)
fieldFoo_ = ensureGen(Field('foo', useClasses=False))

# ToAsk
toask = ToAsk(["Definition", "Definition2"])
toaskForHtml = ToAsk(["Definition", "Definition2"])
toaskForHtmlInList = [ToAsk(["Definition", "Definition2"]), "foo"]

# SingleChild
# HTML
image = Image("http://www.foo.bar")
table = Table(
    [["00", "01"],
     ["10", "11"]
     ],
    trAttrs={"class": "trStyle"},
    tdAttrs={"class": "tdStyle"}
)

paragraph = P(child="Paragraph content")
orderedList = OL(elements=["elt1", "elt2"])
unorderedList = UL(elements=["elt1", "elt2"])

# Conditionals
filledFields = Filled(field="Question",
                      child="Question is filled")
emptyField = Empty(field="Question",
                   child="Question is empty")
questionField = Question(child="This is question side")
answerField = Answer(child="This is answer side")
presentQuestion = Present(
    field="Question",
    child="Question is present in the model")
presentAbsent = Present(
    field="Absent",
    child="Absent is present in the model")
absentQuestion = Absent(
    field="Question",
    child="Question is absent in the model")
absentAbsent = Absent(
    field="Absent",
    child="Absent is absent in the model")

# MultipleChildren
# List
listEmptyInexistingField = ListElement(
    [literalFoo, emptyGen, fieldFooClassless])  # foofo
listEmptyExistingField = ListElement(
    [literalFoo, emptyGen, fieldQuestion])  # fooQuestion
singletonList = ensureGen([Field('foo')])  # fooList
twoQuestionsListed = ListElement([DecoratedField('Definition1', emphasize=False, useClasses=False), DecoratedField(
    'Definition2', emphasize=False, useClasses=False)])  # similar to twoQuestionsListedAsFields

### Asked or Not
asked = Asked(field="asked", child="is asked")
notAsked = NotAsked(field="asked", child="is not asked")
cascadeUseless = Cascade(field="asked",
                         cascade={"cascaded"},
                         child=AskedOrNot("asked",
                                          "Asked is asked",
                                          "Asked is not asked"))
cascade = Cascade(field="asked",
                  cascade={"cascaded"},
                  child=AskedOrNot("cascaded",
                                   "Cascaded is asked",
                                   "Cascaded is not asked"))

# QuestionOrAnswer
qoa = QuestionOrAnswer(question="question side", answer="answer side")
questionsRecursive = QuestionOrAnswer(question=QuestionOrAnswer(
    question="question side", answer="deleted side"), answer="answer side")

# Sugar
parenthisedFoo = Parenthesis("foo")
emptyParenthesis = Parenthesis(None)
# Dichotomy
filledOrEmptyTest = FilledOrEmpty("Question",
                                  "Question is filled",
                                  "Question is empty")
presentOrAbsentQuestion = PresentOrAbsent(
    "Question",
    "Question is present in the model",
    "Question is absent from the model")
presentOrAbsentAbsent = PresentOrAbsent(
    "Absent",
    "Absent is present in the model",
    "Absent is absent from the model")
askedOrNotTest = AskedOrNot("askedOrNot",
                            "Asked",
                            "notAsked")


# Label
labelBarForFieldFooWithoutClass = Label(
    "bar", ["foo"], ["Class name"], alwaysUseClasses=False)
labelBarForFieldFoo = Label("bar", ["foo"], ["Class name"])
labelBarForFieldsFoos = Label("bar", ["foos", "foo", "foo2"], [
                              "Class name"], alwaysUseClasses=False)
# Hide
hideTest = HideInSomeQuestions("hide field", "Content")
# Fields
questionnedField = QuestionnedField(
    'Question', useClasses=False, emphasize=False)
decoratedField = DecoratedField('Question', useClasses=False, emphasize=False)
# FromAndTo
EnglishToFrench = FromAndTo("English", " in ", "French", " is ", "Français")

# Numbers
atLeastOneQuestion = AtLeastOneField(child="At least one",
                                     fields=(["Question", "Question2", "Question3"]))
atLeastOneDefinition = AtLeastOneField(child="At least one",
                                       fields=(["Definition", "Definition2", "Definition3"]))
twoOfTwo = AtLeastTwoFields(child="At least two",
                            fields=(["Question", "Question2"]))
atLeastTwoQuestion = AtLeastTwoFields(child="At least two",
                                      fields=(["Question", "Question2", "Question3"]))
atLeastTwoDefinition = AtLeastTwoFields(child="At least two",
                                        fields=(
                                            ["Definition4", "Definition2", "Definition3"]),
                                        asked=frozenset())

# Requirement
requireQuestion = Filled(field="Question",
                         child=(Literal("Question")))
requirements3 = MultipleRequirement(child="Foo",
                                    requireFilled=frozenset({"Question"}),
                                    requireEmpty=frozenset({"Definition3", "AbsentFromModel"}))

try:
    contradictionRequirement = MultipleRequirement(child=(Literal("Foo")),
                                                   requireFilled=frozenset(
                                                       {"Question"}),
                                                   requireEmpty=frozenset({"Question"}))
    assert False
except Inconsistent:
    pass
requiringInexistant = MultipleRequirement(child=(Literal("Foo")),
                                          requireFilled=frozenset({"absentfrommodel"}))

# Conditionals
#branch = Branch(name="Question", questionAsked = markOfQuestion, default = Field("Question", useClasses=False))
# List Fields

twoQuestionsAsTable = TableFields(['Definition', 'Name'],
                                  name="Definitions",

                                  )
fieldDef = HTML("span",
                attrs={'class': 'Definition'},
                child=Field(field="Definition",
                            isMandatory=True,
                            useClasses=False,),)
tableTwoLine1 = Filled(
    field='Definition',
    child=HTML(
        child=ListElement([
            HTML(
                child=HTML("span",
                           attrs={'class': 'Definition'},
                           child=Literal(text="Definition",),),
                tag='td'),
            HTML(child=fieldDef,
                 tag='td')],),
        tag='tr'),)

tableTwoLine1Answered = Filled(
    field='Definition',
    child=HTML(
        child=ListElement([
            HTML(
                child=HTML("span",
                           attrs={'class': 'Definition'},
                           child=Literal(text="Definition",),),
                tag='td'),
            HTML(
                child=CLASS(["Answer", "Emphasize", "Definition"],
                            Field(field="Definition",
                                  useClasses=False,
                                  isMandatory=True)),
                tag='td')],),
        tag='tr'),)
tableTwoLine2Answered = Filled(
    field='Name',
    child=HTML(
        child=ListElement([
            HTML(
                child=HTML("span",
                           attrs={'class': 'Name'},
                           child=Literal(text="Name",),),
                tag='td'),
            HTML(
                child=CLASS(["Answer", "Emphasize", "Name"],
                            Field(field="Name",
                                  isMandatory=True,
                                  useClasses=False)),
                tag='td')],),
        tag='tr'),)
tableTwoLine1Question = Filled(
    field='Definition',
    child=HTML(
        child=ListElement([
            HTML(
                child=CLASS(["Question", "Emphasize", "Definition"],
                            Literal(text="Definition",)),
                tag='td'),
            HTML(
                child=markOfQuestion,
                tag='td')],),
        tag='tr'),)
tableTwoLine2Question = Filled(
    field='Name',
    child=HTML(
        child=ListElement([
            HTML(
                child=CLASS(["Question", "Emphasize", "Name"],
                            Literal(text="Name",)),
                tag='td'),
            HTML(
                child=markOfQuestion,
                tag='td')],),
        tag='tr'),)
tableTwoLine2 = Filled(
    field='Name',
    child=HTML(
        child=ListElement([
            HTML(
                child=HTML("span",
                           attrs={'class': 'Name'},
                           child=Literal(text="Name",),),
                tag='td'),
            HTML(
                child=HTML("span",
                           attrs={'class': 'Name'},
                           child=Field(field="Name",
                                       isMandatory=True,
                                       useClasses=False,),),
                tag='td')],),
        tag='tr'),)

tableTwoShown = ListElement(
    [HTML(
        child=ListElement([
            tableTwoLine1,
            tableTwoLine2
        ]),
        tag='table'),
     ToAsk(['Definition', 'Name'])])

tableTwoShownQuestion1 = ListElement([
    HTML(
        child=ListElement([
            tableTwoLine1Question,
            tableTwoLine2
        ]),
        tag='table'),
    ToAsk({'Definition': {None}, 'Name': set()})])

tableTwoShownQuestionAll = ListElement([
    HTML(
        child=ListElement([
            tableTwoLine1Question,
            tableTwoLine2Question
        ]),
        tag='table'),
    ToAsk({'Definition': set(), 'Name': set()})])
tableTwoShownAnswer1 = ListElement(
    [HTML(
        child=ListElement([
            tableTwoLine1Answered,
            tableTwoLine2
        ]),
        tag='table'),
     ToAsk({'Definition': {None}, 'Name': set()})])

tableTwoShownAnswerAll = ListElement([
    HTML(
        child=ListElement([
            tableTwoLine1Answered,
            tableTwoLine2Answered
        ]),
        tag='table'),
    ToAsk({'Definition': set(), 'Name': set()})])

# Table 3 columns
fourQuestionsAsTable = TableFields(
    ['Definition', 'Name'], name="Definitions", greater=2)
literalDef = HTML("span",
                  attrs={'class': 'Definition'},
                  child=Literal(text="Definition",),)
literalName = HTML("span",
                   attrs={'class': 'Name'},
                   child=Literal(text="Name",),)
fieldName = HTML("span",
                 attrs={'class': 'Name'},
                 child=Field(field="Name",
                             isMandatory=True,
                             useClasses=False,),)
fieldDef2 = HTML("span",
                 attrs={'class': 'Definition'},
                 child=Field(field="Definition2",
                             isMandatory=True,
                             useClasses=False,),)
fieldName2 = HTML("span",
                  attrs={'class': 'Name'},
                  child=Field(field="Name2",
                              isMandatory=True,
                              useClasses=False,),)

tableFourLine1 = ListElement([
    Filled(
        field='Definition2',
        child=HTML("tr",
                   child=ListElement([
                       HTML("td",
                             child=literalDef,),
                       HTML("td",
                            child=fieldDef,),
                       HTML("td",
                            child=fieldDef2,)],),),),
    Empty(
        field='Definition2',
        child=Filled(
            field='Definition',
            child=HTML("tr",
                       child=ListElement([
                           HTML("td",
                                child=literalDef,),
                           HTML("td",
                                child=fieldDef,)],),),),)],)

tableFourLine1Answered = ListElement([
    Filled(
        field='Definition2',
        child=HTML("tr",
                   child=ListElement([
                       HTML("td",
                            child=literalDef,),
                       HTML("td",
                            child=HTML("span",
                                       attrs={
                                           'class': 'Answer Emphasize Definition'},
                                       child=Field(field="Definition",
                                                   isMandatory=True,
                                                   useClasses=False,),),),
                       HTML("td",
                            child=fieldDef2,)],),),),
    Empty(
        field='Definition2',
        child=Filled(
            field='Definition',
            child=HTML("tr",
                       child=ListElement([
                           HTML("td",
                                child=literalDef,),
                           HTML("td",
                                child=HTML("span",
                                           attrs={
                                               'class': 'Answer Emphasize Definition'},
                                           child=Field(field="Definition",
                                                       isMandatory=True,
                                                       useClasses=False,),),)],),),),)],)

tableFourLine1Answereds = ListElement([
    Filled(
        field='Definition2',
        child=HTML("tr",
                   child=ListElement([
                       HTML("td",
                            child=literalDef,),
                       HTML("td",
                            child=HTML("span",
                                       attrs={
                                           'class': 'Answer Emphasize Definition'},
                                       child=Field(field="Definition",
                                                   isMandatory=True,
                                                   useClasses=False,),),),
                       HTML("td",
                            child=HTML("span",
                                       attrs={
                                           'class': 'Answer Emphasize Definition'},
                                       child=Field(field="Definition2",
                                                   isMandatory=True,
                                                   useClasses=False,),),)],),),),
    Empty(
        field='Definition2',
        child=Filled(
            field='Definition',
            child=HTML("tr",
                       child=ListElement([
                           HTML("td",
                                child=literalDef,),
                           HTML("td",
                                child=HTML("span",
                                           attrs={
                                               'class': 'Answer Emphasize Definition'},
                                           child=Field(field="Definition",
                                                       isMandatory=True,
                                                       useClasses=False,),),)],),),),)],)

tableFourLine2Answered = Filled(
    field='Name',
    child=HTML(
        child=ListElement([
            HTML(
                child=literalName,
                tag='td'),
            HTML(
                child=CLASS(["Answer", "Emphasize", "Name"],
                            Field(field="Name",
                                  isMandatory=True,
                                  useClasses=False)),
                tag='td'),
            HTML(
                child=fieldName2,
                tag='td'),
        ],),
        tag='tr'),)

tableFourLine2Answereds = ListElement([
    Filled(
        field='Name2',
        child=HTML("tr",
                   child=ListElement([
                       HTML("td",
                            child=literalName,),
                       HTML("td",
                            child=HTML("span",
                                       attrs={
                                           'class': 'Answer Emphasize Name'},
                                       child=Field(field="Name",
                                                   isMandatory=True,
                                                   useClasses=False,),),),
                       HTML("td",
                            child=HTML("span",
                                       attrs={
                                           'class': 'Answer Emphasize Name'},
                                       child=Field(field="Name2",
                                                   isMandatory=True,
                                                   useClasses=False,),),)],),),),
    Empty(
        field='Name2',
        child=Filled(
            field='Name',
            child=HTML("tr",
                       child=ListElement([
                           HTML("td",
                                child=literalName,),
                           HTML("td",
                                child=HTML("span",
                                           attrs={
                                               'class': 'Answer Emphasize Name'},
                                           child=Field(field="Name",
                                                       isMandatory=True,
                                                       useClasses=False,),),)],),),),)],)

tableFourLine1Question = ListElement([
    Filled(
        field='Definition2',
        child=HTML("tr",
                   child=ListElement([
                       HTML("td",
                            child=HTML("span",
                                       attrs={
                                           'class': 'Question Emphasize Definition'},
                                       child=Literal(text="Definition",),),),
                       HTML("td",
                            child=markOfQuestion,),
                       HTML("td",
                            child=fieldDef2,)],),),),
    Empty(
        field='Definition2',
        child=Filled(
            field='Definition',
            child=HTML("tr",
                       child=ListElement([
                           HTML("td",
                                child=HTML("span",
                                           attrs={
                                               'class': 'Question Emphasize Definition'},
                                           child=Literal(text="Definition",),),),
                           HTML("td",
                                child=markOfQuestion,)],),),),)],)

tableFourLine1Questions = ListElement([
    Filled(
        field='Definition2',
        child=HTML("tr",
                   child=ListElement([
                       HTML("td",
                            child=HTML("span",
                                       attrs={
                                           'class': 'Question Emphasize Definition'},
                                       child=Literal(text="Definition",),),),
                       HTML("td",
                            child=markOfQuestion,),
                       HTML("td",
                            child=markOfQuestion,)],),),),
    Empty(
        field='Definition2',
        child=Filled(
            field='Definition',
            child=HTML("tr",
                       child=ListElement([
                           HTML("td",
                                child=HTML("span",
                                           attrs={
                                               'class': 'Question Emphasize Definition'},
                                           child=Literal(text="Definition",),),),
                           HTML("td",
                                child=markOfQuestion,),
                           HTML("td",
                                child=markOfQuestion,)],),),),)],)

tableFourLine2Question = Filled(
    field='Name',
    child=HTML(
        child=ListElement([
            HTML(
                child=CLASS(["Question", "Emphasize", "Name"], literalName),
                tag='td'),
            HTML(
                child=markOfQuestion,
                tag='td'),
            HTML(
                child=fieldName2,
                tag='td')
        ]),
        tag='tr'
    ))

tableFourLine2Questions = ListElement([
    Filled(
        field='Name2',
        child=HTML("tr",
                   child=ListElement([
                       HTML("td",
                            child=HTML("span",
                                       attrs={
                                           'class': 'Question Emphasize Name'},
                                       child=Literal(text="Name",),),),
                       HTML("td",
                            child=markOfQuestion,),
                       HTML("td",
                            child=markOfQuestion,)],),),),
    Empty(
        field='Name2',
        child=Filled(
            field='Name',
            child=HTML("tr",
                       child=ListElement([
                           HTML("td",
                                child=HTML("span",
                                           attrs={
                                               'class': 'Question Emphasize Name'},
                                           child=Literal(text="Name",),),),
                           HTML("td",
                                child=markOfQuestion,),
                           HTML("td",
                                child=markOfQuestion,)],),),),)],)

tableFourLine2 = ListElement([
    Filled(
        field='Name2',
        child=HTML("tr",
                   child=ListElement([
                       HTML("td",
                             child=literalName,),
                       HTML("td",
                            child=fieldName,),
                       HTML("td",
                            child=fieldName2,)],),),),
    Empty(
        field='Name2',
        child=Filled(
            field='Name',
            child=HTML("tr",
                       child=ListElement([
                           HTML("td",
                                child=literalName,),
                           HTML("td",
                                child=fieldName,)],),),),)],)

tableFourShown = ListElement(
    [HTML(
        child=ListElement([
            tableFourLine1,
            tableFourLine2
        ]),
        tag='table'),
     ToAsk(['Definition', 'Name'])])

tableFourShownQuestion1 = ListElement([
    HTML(
        child=ListElement([
            tableFourLine1Question,
            tableFourLine2
        ]),
        tag='table'),
    ToAsk({'Definition': {None}, 'Name': set()})])

tableFourShownQuestionAll = ListElement([
    HTML(
        child=ListElement([
            tableFourLine1Questions,
            tableFourLine2Questions
        ]),
        tag='table'),
    ToAsk({'Definition': set(), 'Name': set()})])
tableFourShownAnswer1 = ListElement(
    [HTML(
        child=ListElement([
            tableFourLine1Answered,
            tableFourLine2
        ]),
        tag='table'),
     ToAsk({'Definition': {None}, 'Name': set()})])

tableFourShownAnswerAll = ListElement([
    HTML(
        child=ListElement([
            tableFourLine1Answereds,
            tableFourLine2Answereds
        ]),
        tag='table'),
    ToAsk({'Definition': set(), 'Name': set()})])


# Numbered
twoQuestionsNumbered = NumberedFields('Definition', 2, numbered_field)
twoQuestionsNumberedLine1 = Filled(
    field='Definition',
    child=HTML("li",
               child=fieldDef,),)
twoQuestionsNumberedLine1Question = Filled(
    field='Definition',
    child=HTML("li",
               child=markOfQuestion,),)
twoQuestionsNumberedLine2Question = Filled(
    field='Definition2',
    child=HTML("li",
               child=markOfQuestion,),)
twoQuestionsNumberedLine1Answer = Filled(
    field='Definition',
    child=HTML("li",
               child=CLASS(["Answer", "Emphasize", "Definition"],
                           Field(isMandatory=True, useClasses=False, field="Definition",),),))
twoQuestionsNumberedLine2Answer = Filled(
    field='Definition2',
    child=HTML("li",
               child=CLASS(["Answer", "Emphasize", "Definition"], Field(isMandatory=True, useClasses=False, field="Definition2",),),))
twoQuestionsNumberedLine2 = Filled(
    field='Definition2',
    child=HTML("li",
               child=fieldDef2,),)

labelNormal = HTML("span",
                   attrs={'class': 'Definition'},
                   child=Literal(text="Definitions",),)
twoQuestionsNumberedShown = ListElement([
    ListElement([
        labelNormal,
        Literal(text=": ",),
        HTML("ol",
             child=ListElement([
                 twoQuestionsNumberedLine1,
                 twoQuestionsNumberedLine2
             ],),)],),
    ToAsk({'Definition': set(), 'Definition2': set()})])
labelQuestion = CLASS(["Question", "Emphasize", "Definition"],
                      Literal(text="Definitions",)
                      )

twoQuestionsNumberedShown1Question = ListElement([
    ListElement([
        labelQuestion,
        Literal(text=": ",),
        HTML("ol",
             child=ListElement([
                 twoQuestionsNumberedLine1Question,
                 twoQuestionsNumberedLine2
             ],),)],),
    ToAsk({'Definition': {None}, 'Definition2': set()})])
twoQuestionsNumberedShown1Answer = ListElement([
    ListElement([
        labelNormal,
        Literal(text=": ",),
        HTML("ol",
             child=ListElement([
                 twoQuestionsNumberedLine1Answer,
                 twoQuestionsNumberedLine2
             ],),)],),
    ToAsk({'Definition': {None}, 'Definition2': set()})])

twoQuestionsNumberedAskDefinitionMandatory = Filled(
    field='Definition',
    child=ListElement([
        ListElement([
            HTML("span",
                 attrs={'class': 'Question Emphasize Definition'},
                 child=Literal(text="Definitions",),),
            Literal(text=": ",),
            HTML("ol",
                 child=ListElement([
                     HTML("li",
                          child=markOfQuestion,),
                     Filled(
                         field='Definition2',
                         child=HTML("li",
                                    child=fieldDef2,),)],),)],),
        ToAsk({'Definition': {None}, 'Definition2': set()})]))

twoQuestionsNumberedAllAsked = ListElement([
    ListElement([
        labelQuestion,
        Literal(text=": ",),
        HTML("ol",
             child=ListElement([
                 twoQuestionsNumberedLine1Question,
                 twoQuestionsNumberedLine2Question,
             ],),)],),
    ToAsk({'Definition': set(), 'Definition2': set()})])

twoQuestionsNumberedAllAnswer = ListElement([
    ListElement([
        labelNormal,
        Literal(text=": ",),
        HTML("ol",
             child=ListElement([
                 twoQuestionsNumberedLine1Answer,
                 twoQuestionsNumberedLine2Answer,
             ],),)],),
    ToAsk({'Definition': set(), 'Definition2': set()})])
