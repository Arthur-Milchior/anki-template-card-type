from . import templates
from ..debug import debug

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
    parent = tag.parent
    tagToUse = parent if parent else tag
    ret = tagToUse.find_all(template = (lambda x: x))
    #debug(f"{ret}",-1)
    return ret

def getKind(tag):
    return tag.get("template")

def getModule(tag):
    return templates.getFunctionFromKind(getKind(tag))

def compile_(tag, **kwargs):
    #debug(f"compile_({tag})",+1)
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


    

