import sys
from ..debug import debug
from . import templates

def split(text):
    """None->None, string to the list, splitted at commas"""
    if text:
        return frozenset(text.split(","))
    else:
        return None

def _tagGetParams(tag):
    """The information usefull to process an object template. """
    #debug(f"_tagGetParams({tag.name})", indent=1)
    asked = split(tag.attrs.get("asked"))
    hide = split(tag.attrs.get("hide"))
    objName = tag.attrs.get("object")
    ret = (objName, asked, hide)
    #debug(f"_tagGetParams({tag.name}) returns {ret}", indent=-1)
    return ret

def tagGetParams(tag, objects):
    """
    Return everything required from the tag to add its object in it.
    The object is extracted from objects if it is present. None is returned otherwise. 
    
    add objectabsent to tag if this name is absent from Objects.
    Remove objectabsent if an object with this name is present
    """
    #debug(f"tagGetParams({tag})", indent=1)
    (objName, asked, hide) = _tagGetParams(tag)
    obj = objects.get(objName)
    if obj is None:
        #debug(f"""Adding "objectabsent ={objName}" to "{tag}".""",-1)
        tag.attrs["objectabsent"] = objName
        return None
    elif "objectAbsent" in tag.attrs:
        del tag.attrs["objectAbsent"]
    ret = (obj, asked, hide)
    #debug(f"tagGetParams() returns {ret}", indent=-1)
    return ret

def tagToText(tag, soup, isQuestion, model, objects):
    """The pair with text for the current tag according to parameters
    (without the tag). And the tag with its content.
    Edit the tag to add its content as HTML.

    If only string is important, and tag's only purpose is to have
    valid XML, then the tag is not returned.

    Keyword arguments:
    tag -- a tag, with template ="object", and every information to generate some content.
    soup -- the soup containing the tag.
    isQuestion -- whether we want to generate question side or answer side.
    model -- the model in which it must be applied.
    objects -- the dictionnary name->objects from the configuration file.

    """
    #debug(f"""tagToText({tag},{isQuestion},{model["name"]})""", indent=1)
    params = tagGetParams(tag, objects)
    if params is None:
        ret = None
    else:
        (obj, asked, hide) = params
        ret = obj.restrictToModel(model).template(tag, soup, isQuestion, asked, hide)
    #debug(f"""tagToText() returns {ret}""", indent=-1)
    return ret

def compile_(tag, soup = None, isQuestion = None, model = None, objects = None, **kwargs):
    assert isQuestion is not None
    assert model is not None
    assert objects is not None
    text = tagToText(tag,soup,isQuestion,model, objects)
    if isinstance(text,tuple):
        (text,tag) = text
    #debug(f"""compile_({templateTag.name},{isQuestion},{model["name"]}) returns "{text}".""", indent=-1)
    #return text, tag

def clean(tag):
    """Remove objectAbsent"""
    if "objectAbsent" in templateTag.attrs:
        del templateTag.attrs["objectAbsent"]
    
templates.addKindOfTemplate("object", sys.modules[__name__])
