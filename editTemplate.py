import copy
import collections
from .config import get
from aqt import mw
import re

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
    return templateTagParams(objName, asked,hide, isQuestion)

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
    return params

def templateTagToText(templateTag,isQuestion, model):
    params = templateTagGetParams(templateTag,isQuestion)
    obj = params.obj
    ret = obj.restrictToModel(model).template(obj.asked,obj.hide,isQuestion)
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
    return text
    
def _cleanTemplateTag(templateTag):
    """templateTag is a template tag"""
    templateTag.clear()
    if "objectAbsent" in templateTag.attrs:
        del templateTag.attrs["objectAbsent"]

def applyOnAllTemplateTag(f):
    for templateTag in soup.find_all("span", TemplateVersion = 1):
        f(templateTag)
        
def cleanSoup(soup):
    applyOnAllTemplateTag(_cleanTemplateTag)
    
def compileSoup(soup, isQuestion, model):
    applyOnAllTemplateTag(lambda templateTag:
                          _templateTagAddText(templateTag, isQuestion,model))

def soupFromTemplate(template):
    """Return the soup, with body encompassing everything to ensure it's valid xml"""
    return BeautifulSoup("""<body>template</body>""","xml")
def templateFromSoup(soup):
    """Return the text, from soup, with body removed. Assuming no other
    body tag appear in prettify."""
    t = soup.prettify()
    t= re.sub("</?body>", "", t)
    return
    
def applyOnAllTemplate(model, clean = False):
    for templateObject in model['tmpls']:
        for key,isQuestion in [("afmt",False),("qfmt",True),("bafmt",False),("bqfmt",True)]:
            if key not in templateObject or not  templateObject[key]:
                continue
            soup = soupFromTemplate(templateObject[key])
            if clean:
                cleanSoup(soup)
            else:
                compileSoup(soup, isQuestion, model)
            templateObject[key] = templateFromSoup(soup)
    mw.col.models.save(model, templates = True)
    mw.col.models.flush()
