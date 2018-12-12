htmls = list()
from .models import *
from .jsons import testObjects
from ..imports import *

class TestHTML:
    def  __init__(self,source, compiled, *, numberOfTagToEdit = None, model = model, **kwargs):
        self.source = source
        self.model = model
        self.compiled = compiled
        self.kwargs = kwargs
        self.numberOfTagToEdit = numberOfTagToEdit
    #     self.test()

    # def test(self):
        soup = soupFromTemplate(self.source)
        if self.numberOfTagToEdit is not None:
            assert self.numberOfTagToEdit == len(tagsToEdit(soup))
        #debug(f"""TestHTML: kwargs is {self.kwargs}""")
        compile_(soup, soup = soup, model = model, **self.kwargs)
        assert assertEqual("self.compiled", "templateFromSoup(soup, prettify = True)")

noTagHtml = "foo1"
htmls.append(TestHTML(noTagHtml, noTagHtml, numberOfTagToEdit = 0, objects = testObjects, isQuestion = True))

noTemplateHtml = """<p>
 foo2
</p>"""
htmls.append(TestHTML(noTemplateHtml,noTemplateHtml, numberOfTagToEdit = 0, objects = testObjects, isQuestion = True))

htmlTestObject = """<span name="test" template="conf">
 foo4
</span>"""
htmlTestObjectCompiled = """<span name="test" template="conf">
 test
</span>"""
htmls.append(TestHTML(htmlTestObject, htmlTestObjectCompiled, numberOfTagToEdit = 1, objects = testObjects, isQuestion = True))

htmlBarObject = """<span name="bar" template="conf">
 foo5
</span>"""
htmlBarObjectCompiled = """<span name="bar" objectabsent="bar" template="conf">
</span>"""
htmls.append(TestHTML(htmlBarObject, htmlBarObjectCompiled, numberOfTagToEdit = 1, objects = testObjects, isQuestion = True))

htmlFooObject = """<span name="foo" template="conf">
</span>"""
htmlFooObjectCompiled = """<span name="foo" template="conf">
 foo
 {{Question}}
</span>"""
htmls.append(TestHTML(htmlFooObject, htmlFooObjectCompiled, numberOfTagToEdit = 1, objects = testObjects, isQuestion = True))

htmlFront = """<span template="Front Side">
</span>"""
htmlAnswerTestCompiled = """<span template="Front Side">
 <span name="test" template="conf">
  test
 </span>
</span>"""
htmls.append(TestHTML(htmlFront, htmlAnswerTestCompiled, FrontHtml = htmlTestObject, numberOfTagToEdit = 1, objects = testObjects, isQuestion = False))
htmlQuestion = """<span asked="Question" name="Question" template="conf"/>"""
htmlQuestionCompiled = """<span asked="Question" name="Question" template="conf">
 {{#Question}}
 Question
 :
 ???
 {{/Question}}
</span>"""

df =DecoratedField('Question')
modelApplied = df.restrictToModel(model)


htmls.append(TestHTML(htmlQuestion, htmlQuestionCompiled, objects = testObjects, isQuestion = True))
htmlAnswerCompiled = """<span template="Front Side">
 <span asked="Question" name="Question" template="conf">
  {{#Question}}
  Question
  :
  {{Question}}
  {{/Question}}
 </span>
</span>"""
htmls.append(TestHTML(htmlFront, htmlAnswerCompiled, FrontHtml = htmlQuestion, objects = testObjects, isQuestion = False))


definition1Template ="""<span asked="Definition1" name='ListElement([DecoratedField("Definition1"),DecoratedField("Definition2")])' template="eval"/>"""
definition1Question ="""<span asked="Definition1" name='ListElement([DecoratedField("Definition1"),DecoratedField("Definition2")])' template="eval">
 {{#Definition1}}
 Definition1
 :
 ???
 {{/Definition1}}
 {{#Definition2}}
 Definition2
 :
 {{Definition2}}
 {{/Definition2}}
</span>"""
definition1Answer ="""<span template="Front Side">
 <span asked="Definition1" name='ListElement([DecoratedField("Definition1"),DecoratedField("Definition2")])' template="eval">
  {{#Definition1}}
  Definition1
  :
  {{Definition1}}
  {{/Definition1}}
  {{#Definition2}}
  Definition2
  :
  {{Definition2}}
  {{/Definition2}}
 </span>
</span>"""
TestHTML(definition1Template, definition1Question, objects = testObjects, isQuestion = True)
TestHTML(htmlFront, definition1Answer, FrontHtml = definition1Template, objects = testObjects, isQuestion = False)

definition1Template ="""<span asked="Definition1" name="TwoDefsEasy" template="eval"/>"""
definition1Question ="""<span asked="Definition1" name="TwoDefsEasy" template="eval">
 {{#Definition1}}
 Definition1
 :
 ???
 {{/Definition1}}
 {{#Definition2}}
 Definition2
 :
 {{Definition2}}
 {{/Definition2}}
</span>"""
definition1Answer ="""<span template="Front Side">
 <span asked="Definition1" name="TwoDefsEasy" template="eval">
  {{#Definition1}}
  Definition1
  :
  {{Definition1}}
  {{/Definition1}}
  {{#Definition2}}
  Definition2
  :
  {{Definition2}}
  {{/Definition2}}
 </span>
</span>"""
TestHTML(definition1Template, definition1Question, objects = testObjects, isQuestion = True)
TestHTML(htmlFront, definition1Answer, FrontHtml = definition1Template, objects = testObjects, isQuestion = False)

definition1Template ="""<span asked="Definition1" name="ListFields(['Definition1', 'Definition2'])" template="eval"/>"""
definition1Question ="""<span asked="Definition1" name="ListFields(['Definition1', 'Definition2'])" template="eval">
 {{#Definition1}}
 Definition1
 :
 ???
 {{/Definition1}}
 {{#Definition2}}
 Definition2
 :
 {{Definition2}}
 {{/Definition2}}
</span>"""
definition1Answer ="""<span template="Front Side">
 <span asked="Definition1" name="ListFields(['Definition1', 'Definition2'])" template="eval">
  {{#Definition1}}
  Definition1
  :
  {{Definition1}}
  {{/Definition1}}
  {{#Definition2}}
  Definition2
  :
  {{Definition2}}
  {{/Definition2}}
 </span>
</span>"""
TestHTML(definition1Template, definition1Question, objects = testObjects, isQuestion = True)
TestHTML(htmlFront, definition1Answer, FrontHtml = definition1Template, objects = testObjects, isQuestion = False)

definition1Template ="""<span asked="Definition1" name="TwoDefsMiddle" template="eval"/>"""
definition1Question ="""<span asked="Definition1" name="TwoDefsMiddle" template="eval">
 {{#Definition1}}
 Definition1
 :
 ???
 {{/Definition1}}
 {{#Definition2}}
 Definition2
 :
 {{Definition2}}
 {{/Definition2}}
</span>"""
definition1Answer ="""<span template="Front Side">
 <span asked="Definition1" name="TwoDefsMiddle" template="eval">
  {{#Definition1}}
  Definition1
  :
  {{Definition1}}
  {{/Definition1}}
  {{#Definition2}}
  Definition2
  :
  {{Definition2}}
  {{/Definition2}}
 </span>
</span>"""
TestHTML(definition1Template, definition1Question, objects = testObjects, isQuestion = True)
TestHTML(htmlFront, definition1Answer, FrontHtml = definition1Template, objects = testObjects, isQuestion = False)

definition1Template ="""<span asked="Definition1" name="TwoDefsHard" template="eval"/>"""
definition1Question ="""<span asked="Definition1" name="TwoDefsHard" template="eval">
 {{#Definition1}}
 Definition1
 :
 ???
 {{/Definition1}}
 {{#Definition2}}
 Definition2
 :
 {{Definition2}}
 {{/Definition2}}
</span>"""
definition1Answer ="""<span template="Front Side">
 <span asked="Definition1" name="TwoDefsHard" template="eval">
  {{#Definition1}}
  Definition1
  :
  {{Definition1}}
  {{/Definition1}}
  {{#Definition2}}
  Definition2
  :
  {{Definition2}}
  {{/Definition2}}
 </span>
</span>"""
TestHTML(definition1Template, definition1Question, objects = testObjects, isQuestion = True)
TestHTML(htmlFront, definition1Answer, FrontHtml = definition1Template, objects = testObjects, isQuestion = False)

