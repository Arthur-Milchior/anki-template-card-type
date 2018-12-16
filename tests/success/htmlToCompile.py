from ..imports import *
from ..functions import TestHTML
from ..data.templatesToCompile import *

TestHTML(noTagHtml, noTagHtml, numberOfTagToEdit = 0, objects = testObjects, isQuestion = True)


TestHTML(noTemplateHtml,noTemplateHtml, numberOfTagToEdit = 0, objects = testObjects, isQuestion = True)


TestHTML(htmlTestObject, htmlTestObjectCompiled, numberOfTagToEdit = 1, objects = testObjects, isQuestion = True)


TestHTML(htmlBarObject, htmlBarObjectCompiled, numberOfTagToEdit = 1, objects = testObjects, isQuestion = True)


TestHTML(htmlFooObject, htmlFooObjectCompiled, numberOfTagToEdit = 1, objects = testObjects, isQuestion = True)


TestHTML(htmlFront, htmlAnswerTestCompiled, FrontHtml = htmlTestObject, numberOfTagToEdit = 1, objects = testObjects, isQuestion = False)


TestHTML(htmlQuestion, htmlQuestionCompiled, objects = testObjects, isQuestion = True)


TestHTML(htmlFront, htmlAnswerCompiled, FrontHtml = htmlQuestion, objects = testObjects, isQuestion = False)

TestHTML(definition1TemplateList, definition1QuestionList, objects = testObjects, isQuestion = True)
TestHTML(htmlFront, definition1AnswerList, FrontHtml = definition1TemplateList, objects = testObjects, isQuestion = False)

TestHTML(definition1TemplateEasy, definition1QuestionEasy, objects = testObjects, isQuestion = True)
TestHTML(htmlFront, definition1AnswerEasy, FrontHtml = definition1TemplateEasy, objects = testObjects, isQuestion = False)

TestHTML(definition1TemplateMiddle, definition1QuestionMiddle, objects = testObjects, isQuestion = True)
TestHTML(htmlFront, definition1AnswerMiddle, FrontHtml = definition1Template, objects = testObjects, isQuestion = False)

TestHTML(definition1TemplateHard, definition1QuestionHard, objects = testObjects, isQuestion = True)
TestHTML(htmlFront, definition1AnswerHard, FrontHtml = definition1TemplateHard, objects = testObjects, isQuestion = False)

TestHTML(definition1TemplateTable, definition1QuestionTable, objects = testObjects, isQuestion = True)
TestHTML(htmlFront, definition1AnswerTable, FrontHtml = definition1TemplateTable, objects = testObjects, isQuestion = False)
