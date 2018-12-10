import sys
from ..debug import debug
from . import templates

def split(text):
    """None->None, string to the list, splitted at commas"""
    if isinstance(text,str):
        return frozenset(text.split(","))
    else:
        return frozenset()

def _tagGetParams(tag):
    """The information usefull to process an object template. """
    #debug(f"_tagGetParams({tag.name})", 1)
    asked = split(tag.attrs.get("asked"))
    hide = split(tag.attrs.get("hide"))
    objName = tag.attrs.get("name")
    ret = (objName, asked, hide)
    #debug(f"_tagGetParams({tag.name}) returns {ret}", -1)
    return ret

def tagGetParams(tag, objects):
    """
    Return everything required from the tag to add its object in it.
    The object is extracted from objects if it is present. None is returned otherwise. 
    
    add objectabsent to tag if this name is absent from Objects.
    Remove objectabsent if an object with this name is present
    """
    #debug(f"tagGetParams({tag})",1)
    (objName, asked, hide) = _tagGetParams(tag)
    assert asked is not None
    assert hide is not None
    obj = objects.get(objName)
    if obj is None:
        #debug(f"""Adding "objectabsent ={objName}" to "{tag}".""",-1)
        tag.attrs["objectabsent"] = objName
        return None
    elif "objectAbsent" in tag.attrs:
        del tag.attrs["objectAbsent"]
    ret = (obj, asked, hide)
    #debug(f"tagGetParams() returns {ret}",-1)
    return ret

def tagToText(tag, soup, isQuestion, model, objects, **kwargs):
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
    kwargs -- unused for this kind of template.
    """
    #debug(f"""tagToText({tag},{isQuestion},{model["name"]})""", 1)
    assert soup is not None
    #debug(f"""obects.tagToText: kwargs is {kwargs}""")
    params = tagGetParams(tag, objects)
    if params is None:
        ret = None
    else:
        (obj, asked, hide) = params
        ret = obj.restrictToModel(model).template(tag, soup, isQuestion = isQuestion, asked = asked, hide = hide)
    #debug(f"""tagToText() returns {ret}""", -1)
    return ret

def compile_(tag, soup, isQuestion = None, model = None, objects = None, **kwargs):
    #debug(f"""obects.compile_: kwargs is {kwargs}""")
    assert isQuestion is not None
    assert model is not None
    assert objects is not None
    assert soup is not None
    text = tagToText(tag,soup,isQuestion,model, objects, **kwargs)
    if isinstance(text,tuple):
        (text,tag) = text
    #debug(f"""compile_({templateTag.name},{isQuestion},{model["name"]}) returns "{text}".""", -1)
    #return text, tag

def clean(tag):
    """Remove objectAbsent"""
    tag.clear()
    if "objectAbsent" in templateTag.attrs:
        del templateTag.attrs["objectAbsent"]
    
templates.addKindOfTemplate("config", sys.modules[__name__])
templates.addKindOfTemplate("eval", sys.modules[__name__])
