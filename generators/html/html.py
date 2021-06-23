import bs4

from ...debug import assertEqual, assertType, debug, debugFun, debugInit
from ..generators import Gen, SingleChild, genRepr, thisClassIsClonable
from ..listGen import ListElement


@thisClassIsClonable
class HTML(SingleChild):
    """A html tag, with content."""

    def __init__(self,
                 tag,
                 child,
                 attrs={},
                 **kwargs):
        assert assertType(tag, str)
        self.tag = tag
        self.attrs = attrs
        super().__init__(child=child, **kwargs)

    def __hash__(self):
        return hash((self.tag, self.attrs, self.getChild()))

    @debugFun
    def _cloneSingle(self, child):
        return HTML(tag=self.tag,
                    attrs=self.attrs,
                    child=child,
                    )

    def _repr(self):
        space = "  "*Gen.indentation
        t = f"""HTML("{self.tag}","""
        if self.attrs:
            t += "\n"+genRepr(self.attrs, label="attrs")+","
        if self.child:
            t += "\n"+genRepr(self.child, label="child")+","
        t += self.params()+")"
        return t

    def _outerEq(self, other):
        return isinstance(other, HTML) and self.tag == other.tag and self.attrs == other.attrs and super()._outerEq(other)

    @debugFun
    def _createHtml(self, soup):
        newtag = soup.new_tag(self.tag, **self.attrs)
        children = self.getChild().createHtml(soup)
        assert assertType(children, list)
        for child_tag in children:
            if not (isinstance(child_tag, bs4.element.NavigableString) or isinstance(child_tag, bs4.element.Tag)):
                raise Exception(
                    f"child {child} has type {type(child)}, which can't be in a tag.")
        newtag.contents = children
        return newtag


class Table(HTML):
    @debugInit
    def __init__(self, content, trAttrs={}, tdAttrs={},  caption=None, **kwargs):
        """
        A table with content stated. If content is emptyGen, its normal
        form is an Empty object.

        content -- a list of lines.
        If the line is a list, TD is applied to its elements and TD to the line.
        Otherwise, it is added directly as is. """
        table = []
        for content_ in content:
            if isinstance(content_, list):
                line = []
                for content__ in content_:
                    td = HTML(tag="td",
                              attrs=tdAttrs,
                              child=content__)
                    debug("adding td {td}")
                    line.append(td)
                line = ListElement(elements=line)
                line = TR(line, attrs=trAttrs)
            else:
                line = content_
            table.append(line)
        if caption:
            table = [CAPTION(caption)]+table
        super().__init__("table",
                         child=ListElement(
                             elements=table),
                         **kwargs)


def _fixedTag(tag_):
    assert tag_ is not None

    class FIXED(HTML):
        def __init__(self,
                     #tag = None,
                     child, **kwargs):
            #assert assertEqual(tag, None)
            super().__init__(tag=tag_, child=child, **kwargs)
    FIXED.__name__ = tag_
    return FIXED


SPAN = _fixedTag("span")
HEADER = _fixedTag("header")
FOOTER = _fixedTag("footer")
LI = _fixedTag("li")
DIV = _fixedTag("div")
P = _fixedTag("p")
TR = _fixedTag("tr")
TH = _fixedTag("th")
TD_ = _fixedTag("td")
H1 = _fixedTag("H1")
H2 = _fixedTag("H2")
H3 = _fixedTag("H3")
H4 = _fixedTag("H4")
H5 = _fixedTag("H5")


class TD(TD_):
    # TD should not be removed from the list, else it'd destroy the
    # table. Thus it's never considered to be empty.
    def isEmpty(self):
        return False


SUP = _fixedTag("sup")
SUB = _fixedTag("sub")
CAPTION = _fixedTag("caption")


class _LIST(HTML):
    def __init__(self, elements, enclosing=None, liAttrs={}, addLi=True, **kwargs):
        assert enclosing is not None
        self.elements = elements
        self.enclosing = enclosing

        if addLi:
            elements = [LI(child=element, attrs=liAttrs)
                        for element in elements]
        super().__init__(enclosing, child=elements, **kwargs)


class OL(_LIST):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, enclosing="ol", **kwargs)


class UL(_LIST):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, enclosing="ul", **kwargs)


class CLASS(HTML):
    def __init__(self, classes, *args, attrs={}, **kwargs):
        self.classes = classes
        if isinstance(self.classes, str):
            self.classes = [self.classes]
        self.classes = " ".join([classe.replace(" ", "_")
                                 for classe in self.classes])
        new_attrs = {**attrs, "class": self.classes}
        super().__init__("span", *args, attrs=new_attrs, **kwargs)

    def _getNormalForm(self):
        if not self.classes:
            return self.getChild().getNormalForm()
        else:
            return super()._getNormalForm()

PRE = _fixedTag("pre")
CODE = _fixedTag("code")
