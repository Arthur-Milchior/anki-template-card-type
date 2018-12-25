import sys
from ..debug import assertType
from ..imports import *
from ..debug import ExceptionInverse
from . import templates
from ..config import evaluate
from ..generators.generators import ensureGen, modelToFields
from .templates import Template

def split(text):
    """None->None, string to the list, splitted at commas"""
    if isinstance(text,str):
        return frozenset(text.split(","))
    else:
        return frozenset()

def _tagGetParams(tag):
    """The information usefull to process an object template. """
    asked = split(tag.attrs.get("asked"))
    hide = split(tag.attrs.get("hide"))
    objGenerator = tag.attrs.get("generator")
    mandatory = split(tag.attrs.get("mandatory"))
    if objGenerator is None:
        raise ExceptionInverse(f"""Generator missing in {tag}.""")
    ret = (objGenerator, asked, hide, mandatory)
    return ret

def tagGetParamsConfig(tag, objects):
    """
    Return everything required from the tag to add its object in it.
    The object is extracted from objects. None is returned otherwise. 
    
    add objectabsent to tag if this generator is absent from Objects.
    Remove objectabsent if an object with this generator is present
    """
    (objGenerator, asked, hide, mandatory) = _tagGetParams(tag)
    assert asked is not None
    assert hide is not None
    obj = objects.get(objGenerator)
    if obj is None:
        #debug("""Adding "objectabsent ={objGenerator}" to "{tag}".""",-1)
        tag.attrs["objectabsent"] = objGenerator
        return None
    elif "objectAbsent" in tag.attrs:
        del tag.attrs["objectAbsent"]
    ret = (obj, asked, hide, mandatory)
    return ret

def tagGetParamsEval(tag, objects):
    """
    Return everything required from the tag to add its object in it.
    The object is evaluated, and python error may rise
    """
    (objGenerator, asked, hide, mandatory) = _tagGetParams(tag)
    assert asked is not None
    assert hide is not None
    #debug("objGenerator is {objGenerator}")
    obj = ensureGen(evaluate(objGenerator, objects = objects))
    ret = (obj, asked, hide, mandatory)
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
    objects -- the dictionnary generator->objects from the configuration file.
    kwargs -- unused for this kind of template.
    inConfig -- whether object is in config. Otherwise this value must be evaluated.
    """
    assert assertType(isQuestion, bool)
    assert model is not None
    fields = modelToFields(model)
    assert isinstance(objects, dict)
    assert soup is not None
    if inConfig:
        params = tagGetParamsConfig(tag, objects)
    else:
        params = tagGetParamsEval(tag, objects)
    if params is not None:
        (obj, asked, hide, mandatory) = params
        new_tags = obj.compile(soup = soup,
                               fields = fields,
                               isQuestion = isQuestion,
                               asked = asked,
                               hide = hide,
                               mandatory = mandatory)
        tag.contents = new_tags

def compile_eval(*args, **kwargs):
    """Do the compilation, assuming the string is a Python object"""
    compile_(*args, inConfig=False, **kwargs)

def compile_config(*args, **kwargs):
    """Do the compilation, assuming the string is an element from the
    configuration"""
    compile_(*args, inConfig=True, **kwargs)

    
    
def clean(tag):
    """Remove objectAbsent"""
    tag.clear()
    if "objectAbsent" in templateTag.attrs:
        del templateTag.attrs["objectAbsent"]

#mod = sys.modules[__generator__]
Template(["eval", "evaluate"], compile_eval, clean)
Template(["config","conf"], compile_config, clean)
