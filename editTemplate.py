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
    """Return templateTagParams for the given templateTag. With object name and not the object itself."""
    asked = split(templateTag.attrs.get("asked"))
    hide = split(templateTag.attrs.get("hide"))
    objName = templateTag.attrs.get("object")
    ret = templateTagParams(objName, asked,hide, isQuestion)
    debug("_templateTagGetParams({templateTag},{isQuestion}) = {ret}")
    return 

def templateTagGetParams(templateTag, isQuestion):
    """Return templateTagParams for the given templateTag with object, or None if it does not exists.
    
    add objectAbsent to templateTag if the object is absent. Remove it otherwise.
    """
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
    debug("templateTagGetParams({templateTag},{isQuestion}) = {params}")
    return params

def templateTagToText(templateTag,isQuestion, model):
    params = templateTagGetParams(templateTag,isQuestion)
    obj = params.obj
    ret = obj.restrictToModel(model).template(obj.asked,obj.hide,isQuestion)
    debug("_emplateTagToText({templateTag},{isQuestion},{model}) = {ret}")
    return ret
    

def _templateTagAddText(templateTag,
               isQuestion,
               model):
    """Assuming templateTag is a template tag"""
    if copy.contents or not recompile:
        return
    text = templateTagToText(isQuestion,model)
    if isinstance(text,tuple):
        (text,tag) = text
    debug("_templateTagAddText({templateTag},{isQuestion},{model}) = {text}")
    return text
    
def _cleanTemplateTag(templateTag):
    """templateTag is a template tag"""
    debug("_cleanTemplateTag({f},{soup})")
    templateTag.clear()
    if "objectAbsent" in templateTag.attrs:
        del templateTag.attrs["objectAbsent"]

def applyOnAllTemplateTag(f,soup):
    debug("applyOnAllTemplateTag({f},{soup})")
    for templateTag in soup.find_all("span", TemplateVersion = 1):
        f(templateTag)
        
def cleanSoup(soup):
    debug("cleanSoup({soup})")
    applyOnAllTemplateTag(_cleanTemplateTag, soups)
    
def compileSoup(soup, isQuestion, model):
    debug("compileSoup({soup},{isQuestion},{model})")
    applyOnAllTemplateTag(lambda templateTag:
                          _templateTagAddText(templateTag, isQuestion,model), soup)

def soupFromTemplate(template):
    """Return the soup, with enclose encompassing everything to ensure it's valid xml"""
    r= BeautifulSoup(f"""<enclose>{template}</enclose>""", "html.parser")
    debug("soupFromTemplate({template}) to {r}")
    return r

def templateFromSoup(soup):
    """Return the text, from soup, with enclose removed. Assuming no other
    enclose tag appear in prettify."""
    t = soup.prettify()
    r= re.sub(".*<enclose>(.*)</?enclose>.*", "\\1", t, flags = re.M|re.DOTALL)
    debug("templateFromSoup({t}) to {r}")
    return r
    
def applyOnAllTemplate(model, clean = False):
    for templateObject in model['tmpls']:
        for key,isQuestion in [("afmt",False),("qfmt",True),("bafmt",False),("bqfmt",True)]:
            if key not in templateObject or not  templateObject[key]:
                continue
            originalText = templateObject[key]
            soup = soupFromTemplate(originalText)
            if clean:
                cleanSoup(soup)
            else:
                compileSoup(soup, isQuestion, model)
            newText = templateFromSoup(soup)
            templateObject[key] = newText
            debug(f"from {originalText} to {newText}")
    mw.col.models.save(model, templates = True)
    mw.col.models.flush()
