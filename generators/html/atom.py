import bs4
from ...debug import assertEqual, assertType, debug, debugFun, debugInit
from ..generators import Gen, SingleChild, genRepr, thisClassIsClonable
from ..leaf import Leaf


@thisClassIsClonable
class HTMLAtom(Leaf):
    """A html tag, without content."""

    def __init__(self,
                 tag=None,
                 attrs={},
                 **kwargs):
        assert assertType(tag, str)
        for key in attrs:
            assert assertType(key, str)
            assert assertType(attrs[key], str)
        self.tag = tag
        self.attrs = attrs
        super().__init__(**kwargs)

    def __hash__(self):
        return hash((self.tag, self.attrs))

    def _repr(self):
        space = "  "*Gen.indentation
        t = f"""HTMLAtom("{self.tag}","""
        if self.attrs:
            t += "\n"+genRepr(self.attrs, label="attrs")+","
        t += self.params()+")"
        return t

    def _innerEq(self, other):
        return isinstance(other, HTMLAtom) and self.tag == other.tag and self.attrs == other.attrs

    @debugFun
    def _createHtml(self, soup: bs4.BeautifulSoup):
        newtag = soup.new_tag(self.tag, **self.attrs)
        return newtag


br = HTMLAtom("br")
hr = HTMLAtom("hr")

class CSS(HTMLAtom):
    def __init__(self, path):
        super().__init__("link", {"rel": "stylesheet", "href": path})

class SCRIPT(HTMLAtom):
    def __init__(self, path):
        super().__init__("script", {"src": path})

class Image(HTMLAtom):
    def __init__(self, url):
        super().__init__("img", attrs={"src": url})


markOfQuestion = HTMLAtom("markofquestion")
