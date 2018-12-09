from . import templates
from ..debug import debug, assertType
import bs4

kindOfTemplate = dict()
def addKindOfTemplate(name, f):
    """If template as argument "name", then f is applied to the tag.

    t should take as first argument: tag, potentially other arguments."""
    #debug(f"Adding {name}")
    kindOfTemplate[name.lower()]=f

def getFunctionFromKind(kind):
    return kindOfTemplate.get(kind.lower())


def tagsToEdit(tag):
    #debug(f"tagsToEdit({tag})",1)
    assert assertType(tag, [bs4.element.Tag, bs4.BeautifulSoup])
    ret = tag.find_all(template = (lambda x: x))
    if tag.attrs.get("template"):
        ret.insert(0,self)
    #debug(f"{ret}",-1)
    return ret

def getKind(tag):
    return tag.get("template")

def getModule(tag):
    return templates.getFunctionFromKind(getKind(tag))

def compile_(tag, **kwargs):
    #debug(f"compile_({tag})",+1)
    assert assertType(tag, [bs4.element.Tag, bs4.BeautifulSoup])
    for tag_ in tagsToEdit(tag):
        #debug(f"found {tag_} to compile",+1)
        tag_.contents = []
        getModule(tag_).compile_(tag_, **kwargs)
        #debug(f"",-1)
    #debug(f"",-1)

def clean(tag):
    for tag_ in tagsToEdit(tag):
        tag_.contents = []
        getModule(tag_).clean(tag_)


    

