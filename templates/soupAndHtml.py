import re
from ..tag import tagContent
from bs4 import BeautifulSoup

def addEnclose(content):
    return tagContent("enclose", content = content)
def removeEnclose(html):
    withoutEnclose = re.sub(r".*<enclose>(.*)</?enclose>.*", r"\1", html, flags = re.M|re.DOTALL)
    lineRemoved = re.sub(r"^ ","",withoutEnclose, flags = re.M)[1:-1]
    return lineRemoved
def soupFromTemplate(template):
    """Return the soup, with enclose encompassing everything to ensure it's valid xml"""
    #debug(f"soupFromTemplate({template})", indent=1)
    r= BeautifulSoup(addEnclose(template), "html.parser")
    #debug(f"soupFromTemplate() to {r}", indent=-1)
    return r

def templateFromSoup(soup, prettify = True):
    """Return the text, from soup, with enclose removed. Assuming no other
    enclose tag appear in prettify."""
 #debug(f"""templateFromSoup("{soup}","{prettify}")""", indent=1)
    if prettify:
 #debug("Prettify")
        text = soup.prettify()
    else:
 #debug("str")
        text = str(soup)
 #debug(f"""soup as text is "{text}".""")
    #assert prettify or "\n" not in text
    text= removeEnclose(text)
 #debug(f"""soup as text without enclosed is "{text}" """)
    #assert prettify or "\n" not in text
 #debug(f"templateFromSoup() returns {text}", indent=-1)
    return text
