from ..child import SingleChild
from ..leaf import emptyGen

br = HTML("br")
hr = HTML("hr")
class Image(HTML):
    def __init__(self,url):
        super().__init__("img",{"src":url})
class Table(HTML):
    def __init__(self, content, trAttrs = [], tdAttrs = [], *args, **kwargs):
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
        table), *args, **kwargs)

def _fixedTag(tag):
    class FIXED(HTML):
        def __init__(self, *args, **kwargs):
            super().__init__(tag, *args, **kwargs)
    return FIXED
SPAN = _fixedTag("span")
DIV = _fixedTag("div")
P = _fixedTag("p")
# class SPAN(HTML):
#     def __init__(self, *args, **kwargs):
#         super().__init__("span", *args, **kwargs)
# class DIV(HTML):
#     def __init__(self, *args, **kwargs):
#         super().__init__("div", *args, **kwargs)
# class P(HTML):
#     def __init__(self, *args, **kwargs):
#         super().__init__("p", *args, **kwargs)
