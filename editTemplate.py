import copy
import collections
from .config import getObject
from aqt import mw
import re
from bs4 import BeautifulSoup
from .debug import debug

def split(text):
    if text:
        return text.split(",")
    else:
        return None


def _templateTagGetParams(templateTag, isQuestion):
    """Return templateTagParams for the given templateTag. With object
    name and not the object itself."""
    debug(f"_templateTagGetParams({templateTag.name},{isQuestion})", indent=1)
    asked = split(templateTag.attrs.get("asked"))
    hide = split(templateTag.attrs.get("hide"))
    objName = templateTag.attrs.get("object")
    ret = (objName, asked, hide, isQuestion)
    debug(f"_templateTagGetParams({templateTag.name},{isQuestion}) returns {ret}", indent=-1)
    return ret

def templateTagGetParams(templateTag, isQuestion, objects):
    """Return templateTagParams for the given templateTag with object, or None if it does not exists.
    
    add objectAbsent to templateTag if the object is absent. Remove it otherwise.
    """
    debug(f"templateTagGetParams({templateTag},{isQuestion})", indent=1)
    (objName, asked, hide, isQuestion) = _templateTagGetParams(templateTag,isQuestion)
    obj = objects.get(objName)
    if obj is None:
        debug(f"""Adding "objectabsent ={objName}" to "{templateTag}".""",-1)
        templateTag.attrs["objectabsent"] = objName
        return None
    elif "objectAbsent" in templateTag.attrs:
        del templateTag.attrs["objectAbsent"]
    ret = (obj, asked, hide, isQuestion)
    debug(f"templateTagGetParams() returns {ret}", indent=-1)
    return ret

def templateTagToText(templateTag,soup, isQuestion, model, objects):
    """
    
    """
    debug(f"""templateTagToText({templateTag},{isQuestion},{model["name"]})""", indent=1)
    params = templateTagGetParams(templateTag, isQuestion, objects)
    if params is None:
        ret = None
    else:
        (obj, asked, hide, isQuestion) = params
        ret = obj.restrictToModel(model).template(templateTag, soup, isQuestion, asked, hide)
    debug(f"""templateTagToText() returns {ret}""", indent=-1)
    return ret
    

def _templateTagAddText(templateTag,soup,
                        isQuestion,
                        model,
                        objects, 
                        recompile = False):
    """Assuming templateTag is a template tag. Return the text for this tag, or none if the object is missing."""
    #debug(f"""_templateTagAddText({templateTag},{isQuestion},{model["name"]}, {recompile})""", indent=1)
    if templateTag.contents:
        if not recompile:
            #debug("already have content, and not asked to recompile", -1)
            return
        else:
            templateTag.contents = []
    text = templateTagToText(templateTag,soup,isQuestion,model, objects)
    if isinstance(text,tuple):
        (text,tag) = text
    #debug(f"""_templateTagAddText({templateTag.name},{isQuestion},{model["name"]}) returns "{text}".""", indent=-1)
    return text
    
def _cleanTemplateTag(templateTag):
    """templateTag is a template tag"""
    #debug(f"_cleanTemplateTag({templateTag.name})")
    templateTag.clear()
    if "objectAbsent" in templateTag.attrs:
        del templateTag.attrs["objectAbsent"]

def tagsToEdit(soup):
    return soup.find_all(f"span", templateversion = 1)
    

def applyOnAllTemplateTag(f,soup):
    #debug(f"applyOnAllTemplateTag({f.__name__},soup)")
    for templateTag in findTagToEdit(soup):
        #debug("found tag {templateTag}")
        f(templateTag)
        
def cleanSoup(soup):
    #debug(f"cleanSoup(soup)")
    applyOnAllTemplateTag(_cleanTemplateTag, soups)
    
def compileSoup(soup, isQuestion, model,objects):
    #debug(f"""compileSoup(soup,{isQuestion},{model["name"]})""")
    applyOnAllTemplateTag(lambda templateTag:
                          _templateTagAddText(templateTag, soup, isQuestion,model,objects), soup)


def addEnclose(html):
    return f"""<enclose>{html}</enclose>"""

def removeEnclose(html):
    return re.sub(f".*<enclose>(.*)</?enclose>.*", "\\1", html, flags = re.M|re.DOTALL).strip()

    
def soupFromTemplate(template):
    """Return the soup, with enclose encompassing everything to ensure it's valid xml"""
    #debug(f"soupFromTemplate({template})", indent=1)
    r= BeautifulSoup(addEnclose(template), "html.parser")
    #debug(f"soupFromTemplate() to {r}", indent=-1)
    return r

def templateFromSoup(soup,prettify = True):
    """Return the text, from soup, with enclose removed. Assuming no other
    enclose tag appear in prettify."""
    #debug(f"templateFromSoup(soup)", indent=1)
    t = soup.prettify() if prettify else str(soup)
    r= removeEnclose(t)
    #debug(f"templateFromSoup(soup) returns {r}", indent=-1)
    return r
    
def applyOnAllTemplate(model, objects, clean = False):
    debug(f"""applyOnAllTemplate({model["name"]})""", indent=1)
    for templateObject in model['tmpls']:
        for key,isQuestion in [(f"afmt",False),(f"qfmt",True),(f"bafmt",False),(f"bqfmt",True)]:
            if key not in templateObject:
                #debug("key not in template", indent=-1)
                continue
            if  not templateObject[key]:
                #debug("templateObject[key] falsy", indent=-1)
                continue
            if  templateObject[key].isspace():
                #debug("templateObject[key] is space", indent=-1)
                templateObject[key] == ""
                continue
            debug(f"""applyOnAllTemplate on {key}""", indent=1)
            debug(f"""templateObject[key] is "{templateObject[key]}" """)
            originalText = templateObject[key]
            soup = soupFromTemplate(originalText)
            if clean:
                cleanSoup(soup)
            else:
                compileSoup(soup, isQuestion, model, objects)
            newText = templateFromSoup(soup)
            templateObject[key] = newText
            debug(f"from {originalText} to {newText}", indent=-1)
    mw.col.models.save(model, templates = True)
    mw.col.models.flush()
    debug("", indent=-1)
