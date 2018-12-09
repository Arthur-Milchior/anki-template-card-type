#print("current")
from .imports import *
from .data.htmls import TestHTML
htmls = []


htmlQuestion = """<span object="Question" template="object"/>"""
htmlQuestionCompiled = """<span object="Question" template="object">
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


htmls.append(TestHTML(htmlQuestion, htmlQuestionCompiled, objects = testObjects, isQuestion = True, asked = {"question"}))
htmlAnswerCompiled = """<span template="Front Side">
 <span object="Question" template="object">
 Question
 :
  {{Question}}
 </span>
</span>"""
htmls.append(TestHTML(htmlQuestion, htmlAnswerCompiled, FrontHtml = htmlQuestion, objects = testObjects, isQuestion = False, asked = {"question"}))

# for htmlObject in htmls:
#     htmlObject.test()

