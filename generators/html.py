import bs4
from .leaf import emptyGen, Leaf
from ..debug import debugFun, debugInit, debug, assertType, assertEqual
from .generators import thisClassIsClonable, Gen, genRepr, SingleChild
from .list import ListElement

@thisClassIsClonable
class HTMLAtom(Leaf):
    """A html tag, without content."""

    def __init__(self,
                 tag = None,
                 attrs={},
                 **kwargs):
        assert assertType(tag,str)
        self.tag = tag
        self.attrs = attrs
        super().__init__(**kwargs)

    def __hash__(self):
        return hash((self.tag,self.attrs))
    
    def _repr(self):
        space = "  "*Gen.indentation
        t= f"""HTMLAtom("{self.tag}","""
        if self.attrs:
            t+= "\n"+genRepr(self.attrs, label ="attrs")+","
        t+=self.params()+")"
        return t

    def __eq__(self,other):
        return isinstance(other,HTMLAtom) and self.tag == other.tag and self.attrs == other.attrs

    @debugFun
    def _applyTag(self, soup):
        newtag = soup.new_tag(self.tag, **self.attrs)
        return newtag

@thisClassIsClonable
class HTML(SingleChild):
    """A html tag, with content."""

    def __init__(self,
                 tag,
                 child,
                 attrs={},
                 **kwargs):
        assert assertType(tag,str)
        self.tag = tag
        self.attrs = attrs
        super().__init__(child = child, **kwargs)

    def __hash__(self):
        return hash((self.tag,self.attrs,self.getChild()))

    @debugFun
    def _cloneSingle(self, child):
        return HTML(tag = self.tag,
                    attrs = self.attrs,
                    child = child,
        )
    
    def _repr(self):
        space = "  "*Gen.indentation
        t= f"""HTML("{self.tag}","""
        if self.attrs:
            t+= "\n"+genRepr(self.attrs, label ="attrs")+","
        if self.child:
            t+= "\n"+genRepr(self.child, label ="child")+","
        t+=self.params()+")"
        return t

    def _outerEq(self,other):
        return isinstance(other,HTML) and self.tag == other.tag and self.attrs == other.attrs

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
    
br = HTMLAtom("br")
hr = HTMLAtom("hr")

class Image(HTMLAtom):
    def __init__(self,url):
        super().__init__("img", attrs = {"src":url})

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
HEADER = _fixedTag("header")
FOOTER = _fixedTag("footer")
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
        if isinstance(cl,list):
            cl= " ".join(cl)
        new_attrs = {**attrs, "class":cl}
        super().__init__("span", *args, attrs = new_attrs, **kwargs)
