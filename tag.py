from html import escape
def startOpenTag(tag,attrs= dict()):
    tag = f"""<{tag}"""
    for attr in attrs:
        value = attrs[attr]
        tag+= f""" {attr}="{escape(value)}" """
    return tag

def openTag(tag,attrs= dict()):
    return f"""{startOpenTag(tag,attrs)}>"""
def singleTag(tag,attrs= dict()):
    return f"""{startOpenTag(tag,attrs)}>"""
def closeTag(tag):
    return f"""</{tag}>"""

def tagContent(tag, attrs = dict(), content = None):
    if content is None:
        return singleTag(tag,attrs)
    return f"""{openTag(tag,attrs)}{content}{closeTag(tag)}"""
