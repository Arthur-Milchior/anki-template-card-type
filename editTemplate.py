from .tag import tagContent
from .templates.soupAndHtml import templateFromSoup, soupFromTemplate
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
    #debug(f"""_templateTagAddText({templateTag},{isQuestion},{model["name"]}, {recompile})""", 1)
    if templateTag.contents:
        if not recompile:
            #debug("already have content, and not asked to recompile", -1)
            return
        else:
            templateTag.contents = []




    

def shouldProcess(template,key):
    if key not in template:
        #debug(f"key not in template", -1)
        return False
    if  not template[key]:
        #debug(f"template[key] falsy", -1)
        return False
    if  template[key].isspace():
        #debug(f"template[key] is space", -1)
        template[key] == ""
        return False
    return True

def process(template, key, toClean, prettify = True, **kwargs):
    originalText = template[key]
    soup = soupFromTemplate(originalText)
    if toClean:
        clean(soup)
    else:
        compile_(soup, soup, **kwargs)
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
    #debug(f"""compileModel({model["name"]}, {objects.keys()}, {toClean}, {recompile})""", 1)
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
            
    #debug(f"", -1)
    return model

def compileAndSaveModel(*args,**kwargs):
    model = compileModel(*args,**kwargs)
    mw.col.models.save(model, templates = True)
    mw.col.models.flush()
    #debug(f"", -1)
