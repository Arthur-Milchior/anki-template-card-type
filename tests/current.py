#print("current")
from .imports import *
from .data.htmls import TestHTML
htmls = []


htmlQuestion = """<span object="Question" template="object"/>"""
htmlQuestionCompiled = """<span object="Question" template="object">
 {{#Question}}
 ???
 {{/Question}}
</span>"""
htmls.append(TestHTML(htmlQuestion, htmlQuestionCompiled, objects = testObjects, isQuestion = True))
htmlAnswerCompiled = """<span template="Front Side">
 <span object="Question" template="object">
  {{Question}}
 </span>
</span>"""
htmls.append(TestHTML(htmlQuestion, htmlAnswerCompiled, FrontHtml = htmlQuestion, objects = testObjects, isQuestion = False))

# for htmlObject in htmls:
#     htmlObject.test()

