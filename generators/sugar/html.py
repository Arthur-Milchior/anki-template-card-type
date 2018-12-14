from ..child import SingleChild, HTML
from ..leaf import emptyGen

br = HTML("br")
hr = HTML("hr")

class Image(HTML):
    def __init__(self,url):
        super().__init__("img", attrs = {"src":url})

class Table(HTML):
    def __init__(self, content, trAttrs = {}, tdAttrs = {},  **kwargs):
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
                                 attrs = tdAttrs,
                                 child = content))
            table.append(HTML(tag = "tr",
                              attrs = trAttrs,
                              child = ListElement(elements = line)
            ))
        super().__init__("table", child = ListElement(elements =
        table),  **kwargs)

def _fixedTag(tag):
    class FIXED(HTML):
        def __init__(self,  **kwargs):
            super().__init__(tag,  **kwargs)
    return FIXED
SPAN = _fixedTag("span")
DIV = _fixedTag("div")
P = _fixedTag("p")
TR = _fixedTag("tr")
TD = _fixedTag("td")

class _LIST(HTML):
    def __init__(self, elements, enclosing = None, **kwargs):
        assert enclosing is not None
        self.elements = elements
        lis = [HTML("li",child = element) for element in elements]
        super().__init__("ul", child = lis, **kwargs)
class OL(HTML):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, enclosing = "ol", **kwargs)
class UL(HTML):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, enclosing = "ul", **kwargs)
