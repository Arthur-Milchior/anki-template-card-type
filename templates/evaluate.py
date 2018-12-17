import sys
from ..debug import assertType
from ..imports import *
from ..debug import ExceptionInverse
from . import templates
from ..config import evaluate
from ..generators.generators import ensureGen
from .templates import Template

def split(text):
    """None->None, string to the list, splitted at commas"""
    if isinstance(text,str):
        return frozenset(text.split(","))
    else:
        return frozenset()

def _tagGetParams(tag):
    """The information usefull to process an object template. """
    #debug(f"_tagGetParams({tag})", 1)
    asked = split(tag.attrs.get("asked"))
    hide = split(tag.attrs.get("hide"))
    objName = tag.attrs.get("name")
    if objName is None:
        raise ExceptionInverse(f"""Name missing in {tag}.""")
    ret = (objName, asked, hide)
    #debug(f"_tagGetParams({tag.name}) returns {ret}", -1)
    return ret

def tagGetParamsConfig(tag, objects):
    """
    Return everything required from the tag to add its object in it.
    The object is extracted from objects. None is returned otherwise. 
    
    add objectabsent to tag if this name is absent from Objects.
    Remove objectabsent if an object with this name is present
    """
    #debug(f"tagGetParamsConfig({tag})",1)
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
    #debug(f"tagGetParamsConfig() returns {ret}",-1)
    return ret

def tagGetParamsEval(tag, objects):
    """
    Return everything required from the tag to add its object in it.
    The object is evaluated, and python error may rise
    """
    #debug(f"tagGetParamsEval({tag})",1)
    (objName, asked, hide) = _tagGetParams(tag)
    assert asked is not None
    assert hide is not None
    #debug(f"objName is {objName}")
    obj = ensureGen(evaluate(objName, objects = objects))
    ret = (obj, asked, hide)
    #debug(f"tagGetParamsEval() returns {ret}",-1)
    return ret

def compile_(tag, soup, *, isQuestion = None, model = None, objects = None, inConfig = True, **kwargs):
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
    inConfig -- whether object is in config. Otherwise this value must be evaluated.
    """
    assert assertType(isQuestion, bool)
    assert model is not None
    assert isinstance(objects, dict)
    assert soup is not None
    if inConfig:
        params = tagGetParamsConfig(tag, objects)
    else:
        params = tagGetParamsEval(tag, objects)
    if params is not None:
        tag.clear()
        (obj, asked, hide) = params
        obj.allAndTag(tag = tag,
                      soup = soup,
                      model = model,
                      isQuestion = isQuestion,
                      asked = asked,
                      hide = hide)

def compile_eval(*args, **kwargs):
    compile_(*args, inConfig=False, **kwargs)

def compile_config(*args, **kwargs):
    compile_(*args, inConfig=True, **kwargs)

    
    
def clean(tag):
    """Remove objectAbsent"""
    tag.clear()
    if "objectAbsent" in templateTag.attrs:
        del templateTag.attrs["objectAbsent"]

#mod = sys.modules[__name__]
Template(["eval", "evaluate"], compile_eval, clean)
Template(["config","conf"], compile_config, clean)
