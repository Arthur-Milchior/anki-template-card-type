from .models import *
from .jsons import testObjects
from ...generators.imports import *

noTagHtml = "foo1"

noTemplateHtml = """<p>
 foo2
</p>"""

htmlTestObject = """<span generator="test" template="conf">
 foo4
</span>"""
htmlTestObjectCompiled = """<span generator="test" template="conf">
 test
</span>"""

htmlBarObject = """<span generator="bar" template="conf">
 foo5
</span>"""
htmlBarObjectCompiled = """<span generator="bar" objectabsent="bar" template="conf">
</span>"""

htmlFooObject = """<span generator="foo" template="conf">
</span>"""
htmlFooObjectCompiled = """<span generator="foo" template="conf">
 foo
 {{Question}}
</span>"""

htmlFront = """<span template="Front Side">
</span>"""
htmlAnswerTestCompiled = """<span template="Front Side">
 <span generator="test" template="conf">
  test
 </span>
</span>"""
htmlQuestion = """<span asked="Question" generator="Question" template="conf"/>"""
htmlQuestionCompiled = """<span asked="Question" generator="Question" template="conf">
 {{#Question}}
 Question
 :
 ???
 {{/Question}}
</span>"""

df =DecoratedField('Question')

htmlAnswerCompiled = """<span template="Front Side">
 <span asked="Question" generator="Question" template="conf">
  {{#Question}}
  Question
  :
  {{Question}}
  {{/Question}}
  <br/>
 </span>
</span>"""


definitionTemplateList ="""<span asked="Definition" generator='ListElement([DecoratedField("Definition"),DecoratedField("Definition2")])' template="eval"/>"""
definitionQuestionList ="""<span asked="Definition" generator='ListElement([DecoratedField("Definition"),DecoratedField("Definition2")])' template="eval">
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
 <span asked="Definition" generator='ListElement([DecoratedField("Definition"),DecoratedField("Definition2")])' template="eval">
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

definitionTemplateEasy ="""<span asked="Definition" generator="TwoDefsEasy" template="eval"/>"""
definitionQuestionEasy ="""<span asked="Definition" generator="TwoDefsEasy" template="eval">
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
 <span asked="Definition" generator="TwoDefsEasy" template="eval">
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

definitionTemplateTable ="""<span asked="Definition" generator="TableFields(['Definition', 'Definition2'])" template="eval"/>"""
definitionQuestionTable ="""<span asked="Definition" generator="TableFields(['Definition', 'Definition2'])" template="eval">
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
 <span asked="Definition" generator="TableFields(['Definition', 'Definition2'])" template="eval">
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

# definitionTemplateMiddle ="""<span asked="Definition" generator="TwoDefsMiddle" template="eval"/>"""
# definitionQuestionMiddle ="""<span asked="Definition" generator="TwoDefsMiddle" template="eval">
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
#  <span asked="Definition" generator="TwoDefsMiddle" template="eval">
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

definitionTemplateHard ="""<span asked="Definition" generator="TwoDefsHard" template="eval"/>"""
definitionQuestionHard ="""<span asked="Definition" generator="TwoDefsHard" template="eval">
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
 <span asked="Definition" generator="TwoDefsHard" template="eval">
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

