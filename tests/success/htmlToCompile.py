from ..data import *
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

TestHTML(definitionTemplateList, definitionQuestionList, objects = testObjects, isQuestion = True)
TestHTML(htmlFront, definitionAnswerList, FrontHtml = definitionTemplateList, objects = testObjects, isQuestion = False)

TestHTML(definitionTemplateEasy, definitionQuestionEasy, objects = testObjects, isQuestion = True)
TestHTML(htmlFront, definitionAnswerEasy, FrontHtml = definitionTemplateEasy, objects = testObjects, isQuestion = False)

# TestHTML(definitionTemplateMiddle, definitionQuestionMiddle, objects = testObjects, isQuestion = True)
# TestHTML(htmlFront, definitionAnswerMiddle, FrontHtml = definitionTemplate, objects = testObjects, isQuestion = False)

TestHTML(definitionTemplateTable, definitionQuestionTable, objects = testObjects, isQuestion = True)
TestHTML(htmlFront, definitionAnswerTable, FrontHtml = definitionTemplateTable, objects = testObjects, isQuestion = False)

TestHTML(definitionTemplateHard, definitionQuestionHard, objects = testObjects, isQuestion = True)
TestHTML(htmlFront, definitionAnswerHard, FrontHtml = definitionTemplateHard, objects = testObjects, isQuestion = False)


TestHTML(chooseHtml, chooseHtml1,objects={"toaskForHtml":toaskForHtml})
TestHTML(chooseHtml, chooseHtml2,objects={"toaskForHtml":toaskForHtml})
TestHTML(chooseHtmlInList, chooseHtml1InList,objects={"toaskForHtmlInList":toaskForHtmlInList})
TestHTML(chooseHtmlInList, chooseHtml2InList,objects={"toaskForHtmlInList":toaskForHtmlInList})
