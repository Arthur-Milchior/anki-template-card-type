from .imports import *
from .data.htmls import TestHTML
from bs4 import BeautifulSoup
from html import escape
from .data.templates import testTemplate, emptyHtml
debug("current")

# def test(source, model = model, objects = testObjects, isQuestion = True, asked = frozenset(), hide = frozenset(), **kwargs):
#     soup = soupFromTemplate("<test/>")
#     source.getNormalForm().getWithoutRedundance().restrictToModel(model).template(soup.test, soup = soup, isQuestion = isQuestion, asked = asked, hide = hide, **kwargs)
#     return templateFromSoup(soup, prettify = True)
# tf = TableFields(['Definition1', 'Definition2'])


startDebug()
# tableFieldsTemplate = testTemplate(TableFields(["Question","Back","Absent"]))
# tableFieldsHtml = """<test>
#  <table>
#   <tr>
#    <td>
#     Question
#    </td>
#    <td>
#     {{Question}}
#    </td>
#   </tr>
#   <tr>
#    <td>
#     Back
#    </td>
#    <td>
#     {{Back}}
#    </td>
#   </tr>
#  </table>
# </test>"""


# tableFieldsTemplate = testTemplate(
#     HTML(tag = "table",
#          child = ListElement(
#              elements = [
#                  Requirement(
#                      child = HTML(tag = "tr",
#                                   child = ListElement(elements = [HTML(child = "Question", tag = "td"), HTML(child = Field(field = "Question", ), tag = "td")], )
#                      ),
#                      requireFilled = frozenset({Field(field = "Question", )})
#                  ),
#                  Requirement(
#                      child = HTML(
#                          tag = "tr",
#                          child = ListElement(elements = [HTML(child = "Back", tag = "td"), HTML(child = Field(field = "Back", ), tag = "td")], )),
#                      requireFilled = frozenset({Field(field = "Back", )})),
#                  Requirement(
#                      child = HTML(tag = "tr",
#                                   child = ListElement(elements = [HTML(child = "Absent", tag = "td"), HTML(child = Field(field = "Absent", ), tag = "td")], )),
#                      requireFilled = frozenset({Field(field = "Absent", )})),
#              ],
#          ),
#     )
# )
# tableFieldsHtml = """<test>
#  <table>
#   <tr>
#    <td>
#     Question
#    </td>
#    <td>
#     {{Question}}
#    </td>
#   </tr>
#   <tr>
#    <td>
#     Back
#    </td>
#    <td>
#     {{Back}}
#    </td>
#   </tr>
#  </table>
# </test>"""


# tableFieldsTemplate = testTemplate(
#     ListElement(
#         elements = [
#             Requirement(
#                 child = HTML(tag = "tr",
#                              child = ListElement(elements = [HTML(child = "Question", tag = "td"), HTML(child = Field(field = "Question", ), tag = "td")], )
#                 ),
#                 requireFilled = frozenset({Field(field = "Question", )})
#             ),
#             Requirement(
#                 child = HTML(
#                     tag = "tr",
#                     child = ListElement(elements = [HTML(child = "Back", tag = "td"), HTML(child = Field(field = "Back", ), tag = "td")], )),
#                 requireFilled = frozenset({Field(field = "Back", )})),
#             Requirement(
#                 child = HTML(tag = "tr",
#                              child = ListElement(elements = [HTML(child = "Absent", tag = "td"), HTML(child = Field(field = "Absent", ), tag = "td")], )),
#                 requireFilled = frozenset({Field(field = "Absent", )})),
#         ],
#     ),
# )
# tableFieldsHtml = """<test>
#  <table>
#   {{#Question}}
#   <tr>
#    <td>
#     Question
#    </td>
#    <td>
#     {{Question}}
#    </td>
#   </tr>
#   {{/Question}}
#   {{#Back}}
#   <tr>
#    <td>
#     Back
#    </td>
#    <td>
#     {{Back}}
#    </td>
#   </tr>
#   {{/Back}}
#  </table>
# </test>"""


# assert assertEqual("tableFieldsHtml","tableFieldsTemplate")

endDebug()

# tf_ = test(tf)
# print(tf_)
raise Exception
