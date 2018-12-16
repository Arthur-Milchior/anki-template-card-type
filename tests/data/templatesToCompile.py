from .models import *
from .jsons import testObjects
from ..imports import *

noTagHtml = "foo1"

noTemplateHtml = """<p>
 foo2
</p>"""

htmlTestObject = """<span name="test" template="conf">
 foo4
</span>"""
htmlTestObjectCompiled = """<span name="test" template="conf">
 test
</span>"""

htmlBarObject = """<span name="bar" template="conf">
 foo5
</span>"""
htmlBarObjectCompiled = """<span name="bar" objectabsent="bar" template="conf">
</span>"""

htmlFooObject = """<span name="foo" template="conf">
</span>"""
htmlFooObjectCompiled = """<span name="foo" template="conf">
 foo
 {{Question}}
</span>"""

htmlFront = """<span template="Front Side">
</span>"""
htmlAnswerTestCompiled = """<span template="Front Side">
 <span name="test" template="conf">
  test
 </span>
</span>"""
htmlQuestion = """<span asked="Question" name="Question" template="conf"/>"""
htmlQuestionCompiled = """<span asked="Question" name="Question" template="conf">
 {{#Question}}
 Question
 :
 ???
 {{/Question}}
</span>"""

df =DecoratedField('Question')

htmlAnswerCompiled = """<span template="Front Side">
 <span asked="Question" name="Question" template="conf">
  {{#Question}}
  Question
  :
  {{Question}}
  {{/Question}}
 </span>
</span>"""


definition1TemplateList ="""<span asked="Definition1" name='ListElement([DecoratedField("Definition1"),DecoratedField("Definition2")])' template="eval"/>"""
definition1QuestionList ="""<span asked="Definition1" name='ListElement([DecoratedField("Definition1"),DecoratedField("Definition2")])' template="eval">
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
definition1AnswerList ="""<span template="Front Side">
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

definition1TemplateEasy ="""<span asked="Definition1" name="TwoDefsEasy" template="eval"/>"""
definition1QuestionEasy ="""<span asked="Definition1" name="TwoDefsEasy" template="eval">
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
definition1AnswerEasy ="""<span template="Front Side">
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

definition1TemplateTable ="""<span asked="Definition1" name="TableFields(['Definition1', 'Definition2'])" template="eval"/>"""
definition1QuestionTable ="""<span asked="Definition1" name="TableFields(['Definition1', 'Definition2'])" template="eval">
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
definition1AnswerTable ="""<span template="Front Side">
 <span asked="Definition1" name="TableFields(['Definition1', 'Definition2'])" template="eval">
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

definition1TemplateMiddle ="""<span asked="Definition1" name="TwoDefsMiddle" template="eval"/>"""
definition1QuestionMiddle ="""<span asked="Definition1" name="TwoDefsMiddle" template="eval">
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
definition1AnswerMiddle ="""<span template="Front Side">
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

definition1TemplateHard ="""<span asked="Definition1" name="TwoDefsHard" template="eval"/>"""
definition1QuestionHard ="""<span asked="Definition1" name="TwoDefsHard" template="eval">
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
definition1AnswerHard ="""<span template="Front Side">
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

singleTest = "<test/>"
questionMarks = "???"

