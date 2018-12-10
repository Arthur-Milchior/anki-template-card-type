htmls = list()
from .models import *
from .jsons import testObjects
from ..imports import *

class TestHTML:
    def  __init__(self,source, compiled, numberOfTagToEdit = None, model = model, **kwargs):
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

htmlTestObject = """<span object="test" template="eval">
 foo4
</span>"""
htmlTestObjectCompiled = """<span object="test" template="eval">
 test
</span>"""
htmls.append(TestHTML(htmlTestObject, htmlTestObjectCompiled, numberOfTagToEdit = 1, objects = testObjects, isQuestion = True))

htmlBarObject = """<span object="bar" template="eval">
 foo5
</span>"""
htmlBarObjectCompiled = """<span object="bar" objectabsent="bar" template="eval">
</span>"""
htmls.append(TestHTML(htmlBarObject, htmlBarObjectCompiled, numberOfTagToEdit = 1, objects = testObjects, isQuestion = True))

htmlFooObject = """<span object="foo" template="eval">
</span>"""
htmlFooObjectCompiled = """<span object="foo" template="eval">
 foo
 {{Question}}
</span>"""
htmls.append(TestHTML(htmlFooObject, htmlFooObjectCompiled, numberOfTagToEdit = 1, objects = testObjects, isQuestion = True))

htmlFront = """<span template="Front Side">
</span>"""
htmlAnswerTestCompiled = """<span template="Front Side">
 <span object="test" template="eval">
  test
 </span>
</span>"""
htmls.append(TestHTML(htmlFront, htmlAnswerTestCompiled, FrontHtml = htmlTestObject, numberOfTagToEdit = 1, objects = testObjects, isQuestion = False))
htmlQuestion = """<span asked="Question" object="Question" template="eval"/>"""
htmlQuestionCompiled = """<span asked="Question" object="Question" template="eval">
 {{#Question}}
 Question
 :
 ???
 {{/Question}}
</span>"""

df =DecoratedField('Question')
print(f"df is: {df}")
modelApplied = df.restrictToModel(model)
print(f"df becomes: {modelApplied}")


htmls.append(TestHTML(htmlQuestion, htmlQuestionCompiled, objects = testObjects, isQuestion = True))
htmlAnswerCompiled = """<span template="Front Side">
 <span asked="Question" object="Question" template="eval">
  {{#Question}}
  Question
  :
  {{Question}}
  {{/Question}}
 </span>
</span>"""
htmls.append(TestHTML(htmlFront, htmlAnswerCompiled, FrontHtml = htmlQuestion, objects = testObjects, isQuestion = False))
