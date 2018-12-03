import copy
import collections
from config import get

def split(text):
    if text:
        return text.split(",")
    else:
        return None



xmlParams = collections.nametuple("xmlParams",["obj", "asked", "hide", "isQuestion"])
def _xmlGetParams(xml, isQuestion):
    """Return xmlParams for the given xml. With object name and not the object itself."""
    asked = split(xml.attrib.get("asked"))
    hide = split(xml.attrib.get("hide"))
    objName = xml.attrib.get("object")
    return xmlParams(objName, asked,hide, isQuestion)

def xmlGetParams(xml, isQuestion):
    """Return xmlParams for the given xml with object, or None if it does not exists.
    
    add objectAbsent to xml if the object is absent. Remove it otherwise.
    """
    params = xmlGetParams(xml,isQuestion)
    obj = get(xml.attrib["object"])
    if obj is None:
        xml.attrib["objectAbsent"] = objName
        print(f"Object {objName} requested but not in the configuration")
        return None
    elif "objectAbsent" in xml.attrib:
        del xml.attrib["objectAbsent"]
    params = _xmlGetParams(xml,isQuestion)
    params.obj = obj
    return params

def xmlToText(xml,isQuestion):
    params = xmlGetParams(xml,isQuestion)
    obj = params.obj
    
    

def xmlToCompiled(xml,
                  isQuestion,
                  model):
    if copy.text or not recompile:
        return
    params = xmlGetParams
    obj = params.obj
    if fields is None:
        assert model is not None
        fields =getFields(model)
    obj = obj.restrictToModel(fields)
    (obj, isQuestion, asked = None, hide = None):
    
def compiledToObject(xml):
    """xml is a span tag"""
    xml = copy.copy(xml)
    xml.text = ""
    if "objectAbsent" in xml.attrib:
        del xml.attrib["objectAbsent"]
    return xml
    
