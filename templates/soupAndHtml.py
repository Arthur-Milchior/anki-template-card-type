import re
from ..tag import tagContent
from bs4 import BeautifulSoup
from ..debug import debug, debugFun, debugOnlyThisMethod

def addEnclose(content):
    return tagContent("enclose", content = content)


def removeEnclose(html):
    assert "enclose" in html
    step = html
    step = re.sub(r".*<enclose>(.*)</?enclose>.*", r"\1", step, flags = re.M|re.DOTALL)
    step = re.sub(r"^ ","",step, flags = re.M)[1:-1]
    return step

def soupFromTemplate(template):
    """Return the soup, with enclose encompassing everything to ensure it's valid xml"""
    r= BeautifulSoup(template, "html.parser")
    #r= BeautifulSoup(addEnclose(template), "html.parser")
    return r

@debugFun
def templateFromSoup(soup, prettify = True):
    """Return the text, from soup, with enclose removed. Assuming no other
    enclose tag appear in prettify."""
    debug("""templateFromSoup("{soup}","{prettify}")""", 1)
    if prettify:
        debug("Using Prettify")
        ret = soup.prettify()
        if not ret:
            return ""
        if ret[-1]=="\n":
            ret = ret[:-1]
        return ret
        #text = soup.prettify()
    else:
        debug("Using str")
    #     debug("""soup as text is "{text}".""")
    # assert prettify or "\n" not in text
    # text= removeEnclose(text)
    # debug("""soup as text without enclosed is "{text}" """)
    # assert prettify or "\n" not in text
    # return text
