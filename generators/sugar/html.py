from ..singleChild import SingleChild, HTML
from ..multipleChildren import ListElement
from ..leaf import emptyGen
from ...debug import debugFun, debugInit, debug

br = HTML("br", atom = True)
hr = HTML("hr", atom = True)

class Image(HTML):
    def __init__(self,url):
        super().__init__("img", attrs = {"src":url}, atom = True)

class Table(HTML):
    @debugInit
    def __init__(self, content, trAttrs = {}, tdAttrs = {},  **kwargs):
        """
        A table with content stated. If content is emptyGen, its normal
        form is an Empty object.
        
        content -- a list of n lists of m fields. Assuming each
        element of content have the same length. """
        table = []
        for content_ in content:
            debug(f"Considering {content_}")
            line = []
            for content__ in content_:
                debug(f"Considering {content__}")
                td = HTML(tag = "td",
                          attrs = tdAttrs,
                          child = content__)
                debug(f"adding td {td}") 
                line.append(td)
            tr = HTML(tag = "tr",
                      attrs = trAttrs,
                      child = ListElement(elements = line))
            debug(f"adding tr {tr}") 
            table.append(tr)
        debug(f"super on {table}") 
        super().__init__("table",
                         child = ListElement(
                             elements = table),
                         **kwargs)

def _fixedTag(tag):
    class FIXED(HTML):
        def __init__(self,  **kwargs):
            super().__init__(tag = tag,  **kwargs)
    FIXED.__name__=tag
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
        super().__init__(enclosing, child = lis, **kwargs)
class OL(_LIST):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, enclosing = "ol", **kwargs)
class UL(_LIST):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, enclosing = "ul", **kwargs)
