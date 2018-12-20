from .models import *
from .jsons import testObjects
from ...generators.imports import *

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
  <br/>
 </span>
</span>"""


definitionTemplateList ="""<span asked="Definition" name='ListElement([DecoratedField("Definition"),DecoratedField("Definition2")])' template="eval"/>"""
definitionQuestionList ="""<span asked="Definition" name='ListElement([DecoratedField("Definition"),DecoratedField("Definition2")])' template="eval">
 {{#Definition}}
 Definition
 :
 ???
 {{/Definition}}
  <br/>
 {{#Definition2}}
 Definition2
 :
 {{Definition2}}
 {{/Definition2}}
  <br/>
</span>"""
definitionAnswerList ="""<span template="Front Side">
 <span asked="Definition" name='ListElement([DecoratedField("Definition"),DecoratedField("Definition2")])' template="eval">
  {{#Definition}}
  Definition
  :
  {{Definition}}
  {{/Definition}}
  <br/>
  {{#Definition2}}
  Definition2
  :
  {{Definition2}}
  {{/Definition2}}
  <br/>
 </span>
</span>"""

definitionTemplateEasy ="""<span asked="Definition" name="TwoDefsEasy" template="eval"/>"""
definitionQuestionEasy ="""<span asked="Definition" name="TwoDefsEasy" template="eval">
 {{#Definition}}
 Definition
 :
 ???
 {{/Definition}}
  <br/>
 {{#Definition2}}
 Definition2
 :
 {{Definition2}}
 {{/Definition2}}
  <br/>
</span>"""
definitionAnswerEasy ="""<span template="Front Side">
 <span asked="Definition" name="TwoDefsEasy" template="eval">
  {{#Definition}}
  Definition
  :
  {{Definition}}
  {{/Definition}}
  <br/>
  {{#Definition2}}
  Definition2
  :
  {{Definition2}}
  {{/Definition2}}
  <br/>
 </span>
</span>"""

definitionTemplateTable ="""<span asked="Definition" name="TableFields(['Definition', 'Definition2'])" template="eval"/>"""
definitionQuestionTable ="""<span asked="Definition" name="TableFields(['Definition', 'Definition2'])" template="eval">
 <table>
  {{#Definition}}
  <tr>
   <td>
    Definition
   </td>   <td>
    ???
   </td>
  </tr>  {{/Definition}}
  {{#Definition2}}
  <tr>
   <td>
    Definition2
   </td>   <td>
    {{Definition2}}
   </td>
  </tr>  {{/Definition2}}
 </table>
</span>"""
definitionAnswerTable ="""<span template="Front Side">
 <span asked="Definition" name="TableFields(['Definition', 'Definition2'])" template="eval">
  <table>
   {{#Definition}}
   <tr>
    <td>
     Definition
    </td>    <td>
     {{Definition}}
    </td>
   </tr>   {{/Definition}}
   {{#Definition2}}
   <tr>
    <td>
     Definition2
    </td>    <td>
     {{Definition2}}
    </td>
   </tr>   {{/Definition2}}
  </table>
 </span>
</span>"""

# definitionTemplateMiddle ="""<span asked="Definition" name="TwoDefsMiddle" template="eval"/>"""
# definitionQuestionMiddle ="""<span asked="Definition" name="TwoDefsMiddle" template="eval">
#  {{#Definition}}
#  Definition
#  :
#  ???
#  {{/Definition}}
#  {{#Definition2}}
#  Definition2
#  :
#  {{Definition2}}
#  {{/Definition2}}
# </span>"""
# definitionAnswerMiddle ="""<span template="Front Side">
#  <span asked="Definition" name="TwoDefsMiddle" template="eval">
#   {{#Definition}}
#   Definition
#   :
#   {{Definition}}
#   {{/Definition}}
#   {{#Definition2}}
#   Definition2
#   :
#   {{Definition2}}
#   {{/Definition2}}
#  </span>
# </span>"""

definitionTemplateHard ="""<span asked="Definition" name="TwoDefsHard" template="eval"/>"""
definitionQuestionHard ="""<span asked="Definition" name="TwoDefsHard" template="eval">
 Definitions
 :
 <ul>
  <li>
   {{#Definition}}
   ???
   {{/Definition}}
  </li>  <li>
   {{#Definition2}}
   {{Definition2}}
   {{/Definition2}}
  </li>
 </ul>
</span>"""
definitionAnswerHard ="""<span template="Front Side">
 <span asked="Definition" name="TwoDefsHard" template="eval">
  Definitions
  :
  <ul>
   <li>
    {{#Definition}}
    {{Definition}}
    {{/Definition}}
   </li>   <li>
    {{#Definition2}}
    {{Definition2}}
    {{/Definition2}}
   </li>
  </ul>
 </span>
</span>"""

singleTest = "<test/>"
questionMarks = "???"

