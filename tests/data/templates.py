from ..imports import *

def testTemplate(initial, toPrint = False):
    if toPrint: print(f"""initial is {initial}""")
    normal = initial.getNormalForm()
    if toPrint: print(f"""normal is {normal}""")
    wr = normal.getWithoutRedundance()
    if toPrint: print(f"""wr is {wr}""")
    rest = wr.restrictToModel(model)
    if toPrint: print(f"""restricted by Model is {rest}""")
    soup = soupFromTemplate("<test/>")
    templ = rest.template(isQuestion = True, asked = frozenset({"Definition1"}), hide = frozenset())
    if toPrint: print(f"""restricted by Template is {templ}""")
    templ.applyTag(tag = soup, soup = soup)
    if toPrint: print(soup.prettify())
    return templateFromSoup(soup)

imageTemplated = testTemplate(Image("http://www.foo.bar"))
imageHtml = """<test>
 <img attrs="{'src': 'http://www.foo.bar'}"/>
</test>"""

emptyHtml = """<test>
</test>"""
emptyTemplated = testTemplate(emptyGen)

literalHtml = """<test>
 foo
</test>"""
literalTemplated = testTemplate(Literal("foo"))

fieldHtml = """<test>
 {{Question}}
</test>"""
fieldTemplated = testTemplate(Field("Question"))

requirementHtml = """<test>
 {{#Question}}
 Foo
 {{/Question}}
</test>"""
requirementTemplated = testTemplate(
    Requirement(child = (Literal("Foo")),
                requireFilled = frozenset({"Question"})))

requirementHtml = """<test>
 {{^Definition3}}
 {{#Question}}
 Foo
 {{/Question}}
 {{/Definition3}}
</test>"""
requirementTemplated = testTemplate(
    Requirement(child = (Literal("Foo")),
                requireFilled = frozenset({"Question"}),
                requireEmpty = frozenset({"Definition3", "AbsentFromModel"})))


contradictionTemplated = testTemplate(
    Requirement(child = (Literal("Foo")),
                requireFilled = frozenset({"Question"}),
                requireEmpty = frozenset({"Question"})))
requiringInexistantTemplated = testTemplate(
    Requirement(child = (Literal("Foo")),
                requireFilled = frozenset({"absentfrommodel"})))
listTemplate = testTemplate(ListElement(["foo1","foo2"]))
listHtml ="""<test>
 foo1
 foo2
</test>"""

tableFieldsTemplate = testTemplate(
            Requirement(
                child = HTML(tag = "tr",
                             child = ListElement(elements = [HTML(child = "Question", tag = "td"), HTML(child = Field(field = "Question", ), tag = "td")], )
                ),
                requireFilled = frozenset({"Question"})
            ))
tableFieldsHtml = """<test>
 {{#Question}}
 <tr>
  <td>
   Question
  </td>
  <td>
   {{Question}}
  </td>
 </tr>
 {{/Question}}
</test>"""
