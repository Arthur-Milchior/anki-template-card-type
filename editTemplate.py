import collections
import copy
import re
import sys
from bs4 import BeautifulSoup

from aqt import mw

from .config import objects
from .debug import debug, assertType
from .tag import tagContent
from .templates.soupAndHtml import templateFromSoup, soupFromTemplate
from .templates.templates import clean, compile_


    

def _templateTagAddText(templateTag,soup,
                        isQuestion,
                        model,
                        objects, 
                        recompile = False):
    """Assuming templateTag is a template tag. Return the text for this tag, or none if the object is missing."""
    #debug("""_templateTagAddText({templateTag},{isQuestion},{model["name"]}, {recompile})""", 1)
    if templateTag.contents:
        if not recompile:
            #debug("already have content, and not asked to recompile", -1)
            return
        else:
            templateTag.contents = []




    

def shouldProcess(template,key):
    if key not in template:
        #debug("key not in template", -1)
        return False
    if  not template[key]:
        #debug("template[key] falsy", -1)
        return False
    if  template[key].isspace():
        #debug("template[key] is space", -1)
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
    #debug("""processIfRequired({template.get(key)})""",1)
    if shouldProcess(template, key):
        #debug("Process is required")
        ret= process(template, key, *args, **kwargs)
    else:
        #debug("Process is not required")
        ret= None, ""
    soup,text = ret
    #assert prettify or "\n" not in text
    #debug("",-1)
    return ret

def compileModel(model, objects = objects, toClean = False, recompile = True, prettify = True):
    #debug("""compileModel({model["name"]}, {objects.keys()}, {toClean}, {recompile})""", 1)
    for templateObject in model['tmpls']:
        for questionKey, answerKey in [(f"qfmt","afmt"),(f"bqfmt","bafmt")]:
            questionSoup, questionText = processIfRequired(templateObject, questionKey, toClean = toClean, isQuestion = True, model = model, objects = objects, prettify = prettify)
            if questionText:
 #debug("from {templateObject[questionKey]} to {questionText}. Soup is {str(questionSoup)}.")
                templateObject[questionKey] = questionText
            answerSoup, answerText = processIfRequired(templateObject, answerKey, toClean = toClean, isQuestion = False, model = model, objects = objects, FrontSoup = questionSoup, prettify = prettify)
            if answerText: 
 #debug("from {templateObject[answerKey]} to {answerText}. Soup is {str(answerSoup)}.")
                #assert prettify or "\n" not in answerText
                assert assertType(answerText,str)
                templateObject[answerKey] = answerText
            
    #debug("", -1)
    return model

def compileAndSaveModel(*args,**kwargs):
    model = compileModel(*args,**kwargs)
    mw.col.models.save(model, templates = True)
    try:
        mw.col.models.flush()
    except TypeError:
        print(f"model is {model}")
        raise
        
        #debug("", -1)
