import bs4
from .data.models import *
from ..debug import assertEqual, debugOnlyThisMethod
from ..generators.constants import *
from ..generators.generators import modelToFields
from ..templates.soupAndHtml import soupFromTemplate, templateFromSoup
from ..generators.ensureGen import ensureGen
from ..templates.templates import tagsToEdit, compile_


class TestHTML:
    def  __init__(self,source, compiled, *, numberOfTagToEdit = None, model = model, **kwargs):
        self.source = source
        self.model = model
        self.compiled = compiled
        self.kwargs = kwargs
        self.numberOfTagToEdit = numberOfTagToEdit
    #     self.test()

    # def test(self):
        soup = soupFromTemplate(self.source)
        if self.numberOfTagToEdit is not None:
            assert self.numberOfTagToEdit == len(tagsToEdit(soup))
        #debug("""TestHTML: kwargs is {self.kwargs}""")
        compile_(soup, soup = soup, model = model, **self.kwargs)
        assert assertEqual(templateFromSoup(soup, prettify = True),self.compiled)


def testEachStep(gen,
                 goal = None,
                 model = model,
                 isQuestion = True,
                 asked = frozenset({"Definition"}),
                 hide = frozenset(),
                 mandatory = frozenset(),
                 toPrint = False,
                 html = ""):
    """Main interest is changing the default value for ones useful for the test"""
    fields = modelToFields(model)
    soup = soupFromTemplate(html)
    return gen.compile(
        soup = soup,
        goal = goal,
        fields = fields,
        isQuestion = isQuestion,
        asked = asked,
        mandatory = mandatory,
        hide = hide,
        toPrint = toPrint
    )

def prettifyGen(*args, **kwargs):
    soup = genToSoup(*args, **kwargs)
    return templateFromSoup(soup)
 
def compileGen(*args, goal = TEMPLATE_APPLIED, **kwargs):
    return testEachStep(*args, goal = goal, **kwargs)
 
def genToTags(*args, **kwargs):
    return genToSoup(goal = TAG, *args, **kwargs)


def genToSoup(*args, **kwargs):
    bs = bs4.BeautifulSoup("", "html.parser")
    bs.contents = testEachStep(goal = TAG, *args, **kwargs)
    return bs

 
