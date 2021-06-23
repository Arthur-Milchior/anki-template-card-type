from ...generators import *
from .jsons import testObjects
from .models import *

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
 <span class="Question">
  {{Question}}
 </span>
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
 <span class="Question Emphasize Question">
  Question
 </span> :
 <markofquestion>
 </markofquestion> <br/>
 {{/Question}}
</span>"""

df = DecoratedField('Question')

htmlAnswerCompiled = """<span template="Front Side">
 <span asked="Question" generator="Question" template="conf">
  {{#Question}}
  <span class="Question">
   Question
  </span>  :
  <span class="Answer Emphasize Question">
   {{Question}}
  </span>  <br/>
  {{/Question}}
 </span>
</span>"""


definitionTemplateList = """<span asked="Definition" generator='ListElement([DecoratedField("Definition"),DecoratedField("Definition2")])' template="eval"/>"""
definitionQuestionList = """<span asked="Definition" generator='ListElement([DecoratedField("Definition"),DecoratedField("Definition2")])' template="eval">
 {{#Definition}}
 <span class="Question Emphasize Definition">
  Definition
 </span> :
 <markofquestion>
 </markofquestion> <br/>
 {{/Definition}}
 {{#Definition2}}
 <span class="Definition2">
  Definition2
 </span> :
 <span class="Definition2">
  {{Definition2}}
 </span> <br/>
 {{/Definition2}}
</span>"""

definitionAnswerList = """<span template="Front Side">
 <span asked="Definition" generator='ListElement([DecoratedField("Definition"),DecoratedField("Definition2")])' template="eval">
  {{#Definition}}
  <span class="Definition">
   Definition
  </span>  :
  <span class="Answer Emphasize Definition">
   {{Definition}}
  </span>  <br/>
  {{/Definition}}
  {{#Definition2}}
  <span class="Definition2">
   Definition2
  </span>  :
  <span class="Definition2">
   {{Definition2}}
  </span>  <br/>
  {{/Definition2}}
 </span>
</span>"""

definitionTemplateEasy = """<span asked="Definition" generator="TwoDefsEasy" template="eval"/>"""
definitionQuestionEasy = """<span asked="Definition" generator="TwoDefsEasy" template="eval">
 {{#Definition}}
 <span class="Question Emphasize Definition">
  Definition
 </span> :
 <markofquestion>
 </markofquestion> <br/>
 {{/Definition}}
 {{#Definition2}}
 <span class="Definition2">
  Definition2
 </span> :
 <span class="Definition2">
  {{Definition2}}
 </span> <br/>
 {{/Definition2}}
</span>"""
definitionAnswerEasy = """<span template="Front Side">
 <span asked="Definition" generator="TwoDefsEasy" template="eval">
  {{#Definition}}
  <span class="Definition">
   Definition
  </span>  :
  <span class="Answer Emphasize Definition">
   {{Definition}}
  </span>  <br/>
  {{/Definition}}
  {{#Definition2}}
  <span class="Definition2">
   Definition2
  </span>  :
  <span class="Definition2">
   {{Definition2}}
  </span>  <br/>
  {{/Definition2}}
 </span>
</span>"""


definitionTemplateTable = """<span asked="Definition" generator="TableFields(['Definition', 'Definition2'])" template="eval"/>"""
definitionQuestionTable = """<span asked="Definition" generator="TableFields(['Definition', 'Definition2'])" template="eval">
 <table>
  {{#Definition}}
  <tr>
   <td>
    <span class="Question Emphasize Definition">
     Definition
    </span>
   </td>   <td>
    <markofquestion>
    </markofquestion>
   </td>
  </tr>  {{/Definition}}
  {{#Definition2}}
  <tr>
   <td>
    <span class="Definition2">
     Definition2
    </span>
   </td>   <td>
    <span class="Definition2">
     {{Definition2}}
    </span>
   </td>
  </tr>  {{/Definition2}}
 </table>
</span>"""
definitionAnswerTable = """<span template="Front Side">
 <span asked="Definition" generator="TableFields(['Definition', 'Definition2'])" template="eval">
  <table>
   {{#Definition}}
   <tr>
    <td>
     <span class="Definition">
      Definition
     </span>
    </td>    <td>
     <span class="Answer Emphasize Definition">
      {{Definition}}
     </span>
    </td>
   </tr>   {{/Definition}}
   {{#Definition2}}
   <tr>
    <td>
     <span class="Definition2">
      Definition2
     </span>
    </td>    <td>
     <span class="Definition2">
      {{Definition2}}
     </span>
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
#  <markofquestion>
#  </markofquestion>
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

definitionTemplateHard = """<span asked="Definition" generator="TwoDefsHard" template="eval"/>"""
definitionQuestionHard = """<span asked="Definition" generator="TwoDefsHard" template="eval">
 <span class="Question Emphasize Definition">
  Definitions
 </span> :
 <ol>
  {{#Definition}}
  <li>
   <markofquestion>
   </markofquestion>
  </li>  {{/Definition}}
  {{#Definition2}}
  <li>
   <span class="Definition">
    {{Definition2}}
   </span>
  </li>  {{/Definition2}}
 </ol>
</span>"""
definitionAnswerHard = """<span template="Front Side">
 <span asked="Definition" generator="TwoDefsHard" template="eval">
  <span class="Definition">
   Definitions
  </span>  :
  <ol>
   {{#Definition}}
   <li>
    <span class="Answer Emphasize Definition">
     {{Definition}}
    </span>
   </li>   {{/Definition}}
   {{#Definition2}}
   <li>
    <span class="Definition">
     {{Definition2}}
    </span>
   </li>   {{/Definition2}}
  </ol>
 </span>
</span>"""

singleTest = "<test/>"
questionMarks = """<markofquestion>
 </markofquestion>"""
