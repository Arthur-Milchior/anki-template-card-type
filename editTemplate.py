from .tag import tagContent
import copy
import collections
import sys
from .config import objects
from aqt import mw
import re
from bs4 import BeautifulSoup
from .debug import debug
from .templates.templates import clean, compile_


    

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


def addEnclose(content):
    return tagContent("enclose", content = content)

def removeEnclose(html):
    withoutEnclose = re.sub(r".*<enclose>(.*)</?enclose>.*", r"\1", html, flags = re.M|re.DOTALL)
    lineRemoved = re.sub(r"^ ","",withoutEnclose, flags = re.M)[1:-1]
    return lineRemoved

    
def soupFromTemplate(template):
    """Return the soup, with enclose encompassing everything to ensure it's valid xml"""
    #debug(f"soupFromTemplate({template})", indent=1)
    r= BeautifulSoup(addEnclose(template), "html.parser")
    #debug(f"soupFromTemplate() to {r}", indent=-1)
    return r

def templateFromSoup(soup, prettify = True):
    """Return the text, from soup, with enclose removed. Assuming no other
    enclose tag appear in prettify."""
 #debug(f"""templateFromSoup("{soup}","{prettify}")""", indent=1)
    if prettify:
 #debug("Prettify")
        text = soup.prettify()
    else:
 #debug("str")
        text = str(soup)
 #debug(f"""soup as text is "{text}".""")
    #assert prettify or "\n" not in text
    text= removeEnclose(text)
 #debug(f"""soup as text without enclosed is "{text}" """)
    #assert prettify or "\n" not in text
 #debug(f"templateFromSoup() returns {text}", indent=-1)
    return text

def shouldProcess(template,key):
    if key not in template:
        #debug(f"key not in template", indent=-1)
        return False
    if  not template[key]:
        #debug(f"template[key] falsy", indent=-1)
        return False
    if  template[key].isspace():
        #debug(f"template[key] is space", indent=-1)
        template[key] == ""
        return False
    return True

def process(template, key, toClean, prettify = True, **kwargs):
    originalText = template[key]
    soup = soupFromTemplate(originalText)
    if toClean:
        clean(soup)
    else:
        compile_(soup, **kwargs)
    text =templateFromSoup(soup, prettify = prettify)
    #assert prettify or "\n" not in text
    return soup, text

def processIfRequired(template, key, *args, **kwargs):
    #debug(f"""processIfRequired({template.get(key)})""",1)
    if shouldProcess(template, key):
        #debug(f"Process is required")
        ret= process(template, key, *args, **kwargs)
    else:
        #debug(f"Process is not required")
        ret= None, ""
    soup,text = ret
    #assert prettify or "\n" not in text
    #debug(f"",-1)
    return ret

def compileModel(model, objects = objects, toClean = False, recompile = True, prettify = True):
    #debug(f"""compileModel({model["name"]}, {objects.keys()}, {toClean}, {recompile})""", indent=1)
    for templateObject in model['tmpls']:
        for questionKey, answerKey in [(f"qfmt","afmt"),(f"bqfmt","bafmt")]:
            questionSoup, questionText = processIfRequired(templateObject, questionKey, toClean = toClean, isQuestion = True, model = model, objects = objects, prettify = prettify)
            if questionText:
 #debug(f"from {templateObject[questionKey]} to {questionText}. Soup is {str(questionSoup)}.")
                templateObject[questionKey] = questionText
            answerSoup, answerText = processIfRequired(templateObject, answerKey, toClean = toClean, isQuestion = False, model = model, objects = objects, FrontSoup = questionSoup, prettify = prettify)
            if answerText: 
 #debug(f"from {templateObject[answerKey]} to {answerText}. Soup is {str(answerSoup)}.")
                #assert prettify or "\n" not in answerText
                templateObject[answerKey] = answerText
            
    #debug(f"", indent=-1)
    return model

def compileAndSaveModel(*args,**kwargs):
    model = compileModel(*args,**kwargs)
    mw.col.models.save(model, templates = True)
    mw.col.models.flush()
    #debug(f"", indent=-1)
