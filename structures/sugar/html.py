from .structures.child import SingleChild
from .structures.leaf import emptyGen

class HTML(SingleChild):
    """A html tag, and its content.

    A tag directly closed, such as br or img, should have child emptyGen
    (default value). Values are escaped.
    If child is an Empty object, then toKeep is assumed to be
    true."""

    def __init__(self, tag, params=[],child = emptyGen, toKeep = None
                 *args, **kwargs):
        self.tag = tag
        self.params = params
        if toKeep is None and not child:
            toKeep = True
        super().__init__(child , toKeep = toKeep, *args, **kwargs)

    def _getNormalForm(self):
        tag = f"""<{self.tag}"""
        for (param, value) in self.params:
            tag+= f""" {param}="{escape(value)}\""""
        if not child:
            return Literal(f"""{tag}/>""", toKeep = self.toKeep)
        else:
            return ListElement([Literal(f"""{tag}>"""),self.child,Literal(f"""</{self.tag}>""")], toKeep=self.toKeep).getNormalForm()

br = HTML("br")
hr = HTML("hr")
class Image(HTML):
    def __init__(self,url):
        super().__init__("img",["src",url])
class Table(HTML):
    def __init__(self, content, trParams = [], tdParams = [] *args, **kwargs):
        """
        A table with content stated. If content is emptyGen, its normal
        form is an Empty object.
        
        content -- a list of n lists of m fields. Assuming each
        element of content have the same length. """
        table = []
        for content_ in content:
            line = []
            for content__ in content_:
                line.append(HTML(tag = "td",
                                 params = tdParams,
                                 child = content))
            table.append(HTML(tag = "tr",
                              params = trParams,
                              child = ListElement(elements = line)
            ))
        super().__init__("table", child = ListElement(elements =
        table), *args, **kwargs)

def _fixedTag(tag):
    class FIXED(HTML):
        def __init__(self,*args, **kwargs):
            super().__init__(tag,*args, **kwargs)
    return FIXED
SPAN = _fixedTag("span")
DIV = _fixedTag("div")
P = _fixedTag("p")
# class SPAN(HTML):
#     def __init__(self,*args, **kwargs):
#         super().__init__("span",*args, **kwargs)
# class DIV(HTML):
#     def __init__(self,*args, **kwargs):
#         super().__init__("div",*args, **kwargs)
# class P(HTML):
#     def __init__(self,*args, **kwargs):
#         super().__init__("p",*args, **kwargs)
