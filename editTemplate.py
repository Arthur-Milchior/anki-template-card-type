import copy
import collections
from .config import get
from aqt import mw
import re
from bs4 import BeautifulSoup
from .debug import debug

def split(text):
    if text:
        return text.split(",")
    else:
        return None



templateTagParams = collections.namedtuple("templateTagParams",["obj", "asked", "hide", "isQuestion"])

def _templateTagGetParams(templateTag, isQuestion):
    """Return templateTagParams for the given templateTag. With object
    name and not the object itself."""
    debug(f"_templateTagGetParams({templateTag.name},{isQuestion})", indent=1)
    asked = split(templateTag.attrs.get("asked"))
    hide = split(templateTag.attrs.get("hide"))
    objName = templateTag.attrs.get("object")
    params = templateTagParams(objName, asked,hide, isQuestion)
    debug(f"_templateTagGetParams({templateTag.name},{isQuestion}) returns {params}", indent=-1)
    return params

def templateTagGetParams(templateTag, isQuestion):
    """Return templateTagParams for the given templateTag with object, or None if it does not exists.
    
    add objectAbsent to templateTag if the object is absent. Remove it otherwise.
    """
    debug(f"templateTagGetParams({templateTag.name},{isQuestion})", indent=1)
    params = templateTagGetParams(templateTag,isQuestion)
    obj = get(templateTag.attrs["object"])
    if obj is None:
        templateTag.attrs["objectAbsent"] = objName
        print(f"Object {objName} requested but not in the configuration")
        return None
    elif "objectAbsent" in templateTag.attrs:
        del templateTag.attrs["objectAbsent"]
    params = _templateTagGetParams(templateTag,isQuestion)
    params.obj = obj
    debug(f"templateTagGetParams({templateTag.name},{isQuestion}) returns {params}", indent=-1)
    return params

def templateTagToText(templateTag,isQuestion, model):
    debug(f"""templateTagToText({templateTag.name},{isQuestion},model["name"])""", indent=1)
    params = templateTagGetParams(templateTag,isQuestion)
    obj = params.obj
    ret = obj.restrictToModel(model).template(obj.asked,obj.hide,isQuestion)
    debug(f"""templateTagToText({templateTag.name},{isQuestion},model["name"]) returns {ret}""", indent=-1)
    return ret
    

def _templateTagAddText(templateTag,
               isQuestion,
               model):
    """Assuming templateTag is a template tag"""
    debug(f"""_templateTagAddText({templateTag.name},{isQuestion},{model["name"]})""", indent=1)
    if copy.contents or not recompile:
        return
    text = templateTagToText(isQuestion,model)
    if isinstance(text,tuple):
        (text,tag) = text
    debug(f"""_templateTagAddText({templateTag.name},{isQuestion},{model["name"]}) returns "{text}".""", indent=-1)
    return text
    
def _cleanTemplateTag(templateTag):
    """templateTag is a template tag"""
    debug(f"_cleanTemplateTag({templateTag.name})")
    templateTag.clear()
    if "objectAbsent" in templateTag.attrs:
        del templateTag.attrs["objectAbsent"]

def applyOnAllTemplateTag(f,soup):
    debug(f"applyOnAllTemplateTag({f.__name__},soup)")
    for templateTag in soup.find_all(f"span", templateversion = 1):
        debug("found tag {templateTag}")
        f(templateTag)
        
def cleanSoup(soup):
    debug(f"cleanSoup(soup)")
    applyOnAllTemplateTag(_cleanTemplateTag, soups)
    
def compileSoup(soup, isQuestion, model):
    debug(f"""compileSoup(soup,{isQuestion},{model["name"]})""")
    applyOnAllTemplateTag(lambda templateTag:
                          _templateTagAddText(templateTag, isQuestion,model), soup)

def soupFromTemplate(template):
    """Return the soup, with enclose encompassing everything to ensure it's valid xml"""
    debug(f"soupFromTemplate({template})", indent=1)
    r= BeautifulSoup(f"""<enclose>{template}</enclose>""", "html.parser")
    debug(f"soupFromTemplate() to {r}", indent=-1)
    return r

def templateFromSoup(soup):
    """Return the text, from soup, with enclose removed. Assuming no other
    enclose tag appear in prettify."""
    debug(f"templateFromSoup(soup)", indent=1)
    t = soup.prettify()
    r= re.sub(f".*<enclose>(.*)</?enclose>.*", "\\1", t, flags = re.M|re.DOTALL)
    debug(f"templateFromSoup(soup) returns {r}", indent=-1)
    return r
    
def applyOnAllTemplate(model, clean = False):
    debug(f"""applyOnAllTemplate({model["name"]})""", indent=1)
    for templateObject in model['tmpls']:
        for key,isQuestion in [(f"afmt",False),(f"qfmt",True),(f"bafmt",False),(f"bqfmt",True)]:
            debug(f"""applyOnAllTemplate on {key}""", indent=1)
            if key not in templateObject:
                debug("key not in template", indent=-1)
                continue
            if  not templateObject[key]:
                debug("templateObject[key] falsy", indent=-1)
                continue
            if  templateObject[key].isspace():
                debug("templateObject[key] is space", indent=-1)
                templateObject[key] == ""
                continue
            debug(f"""templateObject[key] is "{templateObject[key]}" """)
            originalText = templateObject[key]
            soup = soupFromTemplate(originalText)
            if clean:
                cleanSoup(soup)
            else:
                compileSoup(soup, isQuestion, model)
            newText = templateFromSoup(soup)
            templateObject[key] = newText
            debug(f"from {originalText} to {newText}", indent=-1)
    mw.col.models.save(model, templates = True)
    mw.col.models.flush()
    debug("", indent=-1)
