
imageHtml = """<img src="http://www.foo.bar"/>"""
emptyHtml = ""

literalHtml = """foo"""

fieldHtml = """{{Question}}"""

requirementHtml = """{{#Question}}
Question
{{/Question}}"""

requirement2Html = """{{^Definition3}}
{{#Question}}
Foo
{{/Question}}
{{/Definition3}}"""

listHtml = """foo
{{Question}}"""

# tableFieldsTemplate = testTemplate(
#             MultipleRequirement(
#                 child = HTML(tag = "tr",
#                              child = ListElement(elements = [HTML(child = "Question", tag = "td"), HTML(child = Field(field = "Question", ), tag = "td")], )
#                 ),
#                 requireFilled = frozenset({"Question"})
#             ))
# tableFieldsHtml = """{{#Question}}
# <tr>
#  <td>
#   Question
#  </td>
#  <td>
#   {{Question}}
#  </td>
# </tr>
# {{/Question}}"""

chooseHtml = """<span choose="yes" generator="toaskForHtml" template="eval" />"""
chooseHtml1 = """<span askedmandatory="Definition" choose="yes" generator="toaskForHtml" template="eval">
</span>"""
chooseHtml2 = """<span askedmandatory="Definition2" choose="yes" generator="toaskForHtml" template="eval">
</span>"""
chooseHtmlInList = """<span choose="yes" generator="toaskForHtmlInList" template="eval" />"""
chooseHtml1InList = """<span askedmandatory="Definition" choose="yes" generator="toaskForHtmlInList" template="eval">
 foo
</span>"""
chooseHtml2InList = """<span askedmandatory="Definition2" choose="yes" generator="toaskForHtmlInList" template="eval">
 foo
</span>"""
