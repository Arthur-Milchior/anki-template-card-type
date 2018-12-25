
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

listHtml ="""foo
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
