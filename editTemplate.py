import collections
import copy
import re
import sys
from bs4 import BeautifulSoup
import traceback

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
    """Whether key is in template and is non-empty"""
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

def process(template, key, action, prettify = True, **kwargs):
    originalText = template[key]
    soup = soupFromTemplate(originalText)
    if action=="Clean":
        clean(soup)
    elif action=="Template":
        compile_(soup, soup, **kwargs)
    elif action=="ReTemplate":
        compile_(soup, soup, recompile=True, **kwargs)
    text =templateFromSoup(soup, prettify = prettify)
    #assert prettify or "\n" not in text
    return soup, text

def processIfRequired(template, key, *args, **kwargs):
    if shouldProcess(template, key):
        ret= process(template, key, *args, **kwargs)
    else:
        ret= None, ""
    soup,text = ret
    return ret

def compileModel(model, objects = objects, action = "Template",  prettify = True):
    """Compile the model. If a compilation raised an exception, it is captured. List of exceptions are returned with the model"""
    for templateObject in model['tmpls']:
        for questionKey, answerKey in [(f"qfmt","afmt"),(f"bqfmt","bafmt")]:
            if action=="Back to front":
                templateObject[answerKey]="""<span template="Front Side"/>"""
            else:
                frontHtml=templateObject[questionKey]
                try:
                    questionSoup, questionText = processIfRequired(templateObject, questionKey, action = action, isQuestion = True, model = model, objects = objects, prettify = prettify)
                    if questionText:
                        templateObject[questionKey] = questionText
                except Exception as e:
                    print("\n\n\n")
                    print((templateObject["name"],questionKey,e),file=sys.stderr)
                    traceback.print_exc(file=sys.stderr)
                    print("\n\n\n")
                try:
                    answerSoup, answerText = processIfRequired(templateObject, answerKey, action = action, isQuestion = False, model = model, objects = objects, FrontHtml = frontHtml, prettify = prettify)
                    if answerText: 
                        assert assertType(answerText,str)
                        templateObject[answerKey] = answerText
                except Exception as e:
                    print("\n\n\n")
                    print((templateObject["name"],answerKey,e),file=sys.stderr)
                    traceback.print_exc(file=sys.stderr)
                    print("\n\n\n")
    return model

def compileAndSaveModel(*args,**kwargs):
    model = compileModel(*args,**kwargs)
    mw.col.models.save(model, templates = True)
    mw.col.models.flush()

