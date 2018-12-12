from .imports import *
from .data.htmls import TestHTML
from bs4 import BeautifulSoup
from html import escape 
debug("current")

# lf = ListFields(['Definition1', 'Definition2'])
# # print(f"Initial lf is {lf}")
# normal = lf.getNormalForm()
# # print(f"Normal lf is {normal}")
# withoutRedundance = lf.getWithoutRedundance()
# # print(f"withoutRedundance lf is {withoutRedundance}")

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

# test = definition1Template%("""ListElement([DecoratedField(&quot;Definition1&quot;),DecoratedField(&quot;Definition2&quot;)])""")
# b = BeautifulSoup(test,"html.parser")
# print(test)
# print(b)


