from .data.models import *
from ..generators.constants import *
from ..generators.generators import modelToFields
from ..templates.soupAndHtml import soupFromTemplate, templateFromSoup
from ..generators.ensureGen import ensureGen

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
        #debug(f"""TestHTML: kwargs is {self.kwargs}""")
        compile_(soup, soup = soup, model = model, **self.kwargs)
        assert assertEqual(self.compiled, templateFromSoup(soup, prettify = True))

def testEachStep(gen,
                 goal = None,
                 model = model,
                 isQuestion = True,
                 asked = frozenset({"Definition"}),
                 hide = frozenset(),
                 toPrint = False,
                 html = ""):
    fields = modelToFields(model)
    soup = soupFromTemplate(html)
    tag = soup.enclose
    return gen.compile(tag = tag,
                soup = soup,
                goal = goal,
                fields = fields,
                isQuestion = isQuestion,
                asked = asked,
                hide = hide,
                toPrint = toPrint
    )

def prettifyGen(*args, **kwargs):
    soup = genToSoup(*args, **kwargs)
    return soup.prettify()
 
def compileGen(*args, goal = TEMPLATE_APPLIED, **kwargs):
    return testEachStep(*args, goal = goal, **kwargs)
 
def genToSoup(*args, **kwargs):
    return testEachStep(goal = SOUP_PRETTIFIED, *args, **kwargs)

 
