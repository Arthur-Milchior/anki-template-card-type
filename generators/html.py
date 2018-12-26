import bs4
from .singleChild import SingleChild
from .leaf import emptyGen
from ..debug import debugFun, debugInit, debug, assertType, assertEqual
from .generators import thisClassIsClonable, Gen, genRepr, ListElement

@thisClassIsClonable
class HTML(SingleChild):
    """A html tag, and its content.

    A tag directly closed, such as br or img, should have child emptyGen
    (default value). Values are escaped.
    If child is an Empty object, then toKeep is assumed to be
    true."""

    def __init__(self,
                 tag = None,
                 atom = False,
                 attrs={},
                 **kwargs):
        assert assertType(tag,str)
        self.tag = tag
        self.attrs = attrs
        toKeep = atom is True
        self.atom = atom
        super().__init__(toKeep = toKeep, **kwargs)

    @debugFun
    def isEmpty(self):
        return ((not self.atom) and self.getChild().isEmpty())

    def __hash__(self):
        return hash((self.tag,self.attrs,self.getChild()))

    @debugFun
    def cloneSingle(self, child):
        if child == self.getChild():
            return self
        if not child and not self.atom:
            return emptyGen
        return HTML(tag = self.tag,
                    attrs = self.attrs,
                    child = child,
                    atom = self.atom
        )
    
    # @debugFun
    # def cloneSingle(self, elements):
    #     assert len(elements)==1
    #     element = elements[0]
    #     if element == self.child:
    #         return self
    #     if not element and not self.atom:
    #         return emptyGen
    #     return HTML(tag = self.tag,
    #                 attrs = self.attrs,
    #                 child = element,
    #                 atom = self.atom
    #     )
    
    def _repr(self):
        space = "  "*Gen.indentation
        t= f"""HTML("{self.tag}","""
        if self.attrs:
            t+= "\n"+genRepr(self.attrs, label ="attrs")+","
        if self.child:
            t+= "\n"+genRepr(self.child, label ="child")+","
        if self.atom:
            t+= "\n"+genRepr(self.atom, label ="atom")+","
        t+=self.params()+")"
        return t

    def __eq__(self,other):
        return super().__eq__(other) and isinstance(other,HTML) and self.tag == other.tag and self.attrs == other.attrs

    @debugFun
    def _applyTag(self, soup):
        newtag = soup.new_tag(self.tag, **self.attrs)
        children = self.getChild().applyTag(soup)
        assert assertType(children, list)
        for child_tag in children:
            if not (isinstance(child_tag, bs4.element.NavigableString) or isinstance(child_tag, bs4.element.Tag)):
                raise Exception(f"child {child} has type {type(child)}, which can't be in a tag.")
        newtag.contents = children
        return newtag

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
            debug("Considering {content_}")
            line = []
            for content__ in content_:
                debug("Considering {content__}")
                td = HTML(tag = "td",
                          attrs = tdAttrs,
                          child = content__)
                debug("adding td {td}") 
                line.append(td)
            tr = HTML(tag = "tr",
                      attrs = trAttrs,
                      child = ListElement(elements = line))
            debug("adding tr {tr}") 
            table.append(tr)
        debug("super on {table}") 
        super().__init__("table",
                         child = ListElement(
                             elements = table),
                         **kwargs)

def _fixedTag(tag_):
    assert tag_ is not None    
    class FIXED(HTML):
        def __init__(self,
                     #tag = None,
                     child, **kwargs):
            #assert assertEqual(tag, None)
            super().__init__(tag = tag_, child = child, **kwargs)
    FIXED.__name__=tag_
    return FIXED

SPAN = _fixedTag("span")
LI = _fixedTag("li")
DIV = _fixedTag("div")
P = _fixedTag("p")
TR = _fixedTag("tr")
TD = _fixedTag("td")

class _LIST(HTML):
    def __init__(self, elements, enclosing = None, liAttrs = {}, **kwargs):
        assert enclosing is not None
        self.elements = elements
        self.enclosing = enclosing
        
        lis = [LI(child = element, attrs = liAttrs) for element in elements]
        super().__init__(enclosing, child = lis, **kwargs)
class OL(_LIST):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, enclosing = "ol", **kwargs)
class UL(_LIST):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, enclosing = "ul", **kwargs)

class CLASS(HTML):
    def __init__(self, cl, *args, attrs = {}, **kwargs):
        new_attrs = {**attrs, "class":cl}
        super().__init__("span", *args, attrs = new_attrs, **kwargs)
