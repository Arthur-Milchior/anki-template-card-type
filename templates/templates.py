from ..debug import debug, assertType, ExceptionInverse
import bs4

class Template:
    kindOfTemplate = dict()
    def __init__(self, names, compile_, clean):
        for name in names:
            Template.kindOfTemplate[name.lower()] = self
        self.compile_=compile_
        self.clean = clean

# def addKindOfTemplate(name, f):
#     """If template as argument "name", then f is applied to the tag.

#     t should take as first argument: tag, potentially other arguments."""
#     #debug("Adding {name}")
#     kindOfTemplate[name.lower()]=f

def getFunctionFromKind(kind):
    """Given a kind, the method to call to generate the content."""
    r = Template.kindOfTemplate.get(kind.lower())
    if r is None:
        raise ExceptionInverse(f"""Kind "{kind}" is called, but not present in templates.template.kindOfTemplate. It contains only Template {Template.kindOfTemplate}""")
    return r


def tagsToEdit(tag):
    """List of tag having a "template" attribute with a non-empty value."""
    #debug("tagsToEdit({tag})",1)
    assert assertType(tag, [bs4.element.Tag, bs4.BeautifulSoup])
    ret = tag.find_all(template = (lambda x: x))
    if tag.attrs.get("template"):
        ret.insert(0,self)
    #debug("{ret}",-1)
    return ret

def getKind(tag):
    """The kind of template from this tag."""
    return tag.get("template")

def getModule(tag):
    """The module object according to the template name from this tag.""" 
    return getFunctionFromKind(getKind(tag))

def compile_(tag, soup, **kwargs):
    """For each tag having a template non-empty attribute, apply the
    generator according to this value.

    """
    #debug("compile_({tag})",+1)
    assert soup is not None
    assert assertType(tag, [bs4.element.Tag, bs4.BeautifulSoup])
    #debug("""templates.compile_: kwargs is {kwargs}""")
    for tag_ in tagsToEdit(tag):
        #debug("found {tag_} to compile",+1)
        tag_.contents = []
        getModule(tag_).compile_(tag = tag_, soup = soup, **kwargs)
        #debug("",-1)
    #debug("",-1)

def clean(tag):
    for tag_ in tagsToEdit(tag):
        getModule(tag_).clean(tag_)


    

