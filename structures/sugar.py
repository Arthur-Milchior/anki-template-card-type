from .structures.children import MultipleChild
from .structures.child import SingleChild
from .structures.leaf import Empty, empty
from html import escape

class AtLeastOne(SingleChild):
    """Show the child if there is at least one condition.

    The child is repeated as many time in the card's template as they
    are conditions. So use this only for small text, such as
    <table>

    """
    def __init__(self,child, conditions):
        super().__init__(child)
        self.conditions = conditions

    def _mustache(self, *args, **kwargs):
        t = self.child.mustache(*args, **kwargs)
        if not t:
            return ""

    def _getNormalForm(self):
        super().normalize()
        actual = empty
        child = self.getNormalForm()
        for condition in self.conditions:
            actual = PresentOrAbsent(condition,
                            present = child,
                            absent = actual,
                            normalized ).getNormalForm()
        return actual
    
class PresentOrAbsent(MultipleChild):
    def __init__(self,field,present = empty,absent = empty, *args, **kwargs):
        super().__init__(children = [present,absent], *args, **kwargs)
        self.field = field

    def getPresent(self):
        return self.children[0]
    def getAbsent(self):
        return self.children[1]
        
    def _getNormalForm(self):
        super().normalize()
        return ListElement([
            Requirements(
                self.getPresent().getNormalForm(),
                required = {self.field}
                ),
            Requirements(
                self.getAbsent().getNormalForm(),
                forbidden = {self.field}
            )]).getNormalForm()
    
class ListFields(MultipleChild):#(RecursiveFields)
    """If no field is present, return empty string. Otherwise, as follows:

    keyword arguments:
    globalPrefix/suffix  -- the prefix/suffix for the whole
    set. Assuming at least one element is present. For example <table>
    or <p>. 

    globalSeparator -- text separating two fields. For example
    <br/>. If possible, avoid it, because it requires to write long
    code. (The square of the number of field). Most of the time, you
    can put the separator in a local suffix. For example, an extra
    <br/> after the las present field would be acceptable.

    localPrefix/Suffix -- the prefix/suffix of each field.  For
    example <tr><td>, <li>. It is added as prefix/suffix of fields

    localSeparator -- the separator between the field name and the answer. For example :, or </td><td>

    hideSuccessor -- if False (default), all present elements are shown.
                     if True, each element which are not asked and are the successor of a asked element are not shown
                     if string, the presence of the fields is similar to True, its absence to False.

    fields -- A list whose elements are either:
           --- A field name, in which case 
           --- A Field object (in which case, local separator is not used, the other local things are used) or,
           --- A pair with a the description to use and the field name (e.g. ("Variable", variable1)

    """
    # fields is normalized and contains only Field objectc
    # Currently, we don't use the fact that it is RecursiveFields
    def __init__(self,
                 fields,
                 globalPrefix = empty,
                 globalSeparator = empty,
                 globalSuffix = empty,
                 localPrefix = empty,
                 localSeparator = empty,
                 localSuffix = empty,
                 hideSuccessor = False,
                 *args,
                 **kwargs):
        self.globalPrefix = globalPrefix
        self.globalsuffix = globalSuffix
        self.globalSeparator = globalSeparator
        self.localPrefix = localPrefix
        self.localSuffix = localSuffix
        self.localSeparator = localSeparator
        self.hideSuccessor = hideSuccessor
        self.fields = []
        for field in fields:
            self._addField(field)
        super().__init__(fields,
                         # descriptions = [
                         #     {"prefix": globalPrefix,
                         #      "suffix": globalSuffix,
                         #      "separator": globalSeparator},
                         #     {"prefix": localPrefix,
                         #      "suffix": localSuffix,
                         #      "separator": localSeparator},
                         # ] ,
                         *args, **kwargs)

            
    def _addField(self,field):
        if isinstance(field,Field):
            field = copy.deepcopy(field)
            field.prefix = self.localPrefix + field.prefix
            field.suffix = field.suffix + self.localSuffix
            self.fields.append(field)
        elif isinstance(field,tuple):
            symbol,fieldName = field
            if not isinstance(prefix,str):
                raise Exception(prefix, "first element of a pair, is not a string")
            if not isinstance(fieldName,str):
                raise Exception(prefix, "second element of a pair, is not a string")
            self.fields.append(Field(fieldName,prefix = localPrefix, symbol = prefix,separator = localSeparator, suffix = localSuffix))
        elif isinstance(field, str):
            self.fields.append(Field(field,prefix = localPrefix,suffix = localSuffix, separator = localSeparator))
        else:
            raise Exception(field, "is neither a field name, a Field
        nor a pair")

    def _getNormalForm(self):
        elements = []
        if self.globalPrefix:
            elements.append(AtLeastOne(child = self.globalPrefix,
                                       conditions = fields))
        seen = {}
        for fieldObject in self.fields:
            if self.globalSeparator:
                elements.append(
                    AtLeastOne(child =
                               self.globalSeparator,
                               conditions = seen))
                seen.add(fieldObject)
            elements.append(fieldObject)
        if self.globalSuffix:
            elements.append(AtLeastOne(child = self.globalSuffix,
                                       conditions = fields))
        return ListElement(elements).getNormalForm()

# class EnumerateFields(ListFields):
#     """A set of fields, having the same prefix, and a suffix from 1 to n."""
#     def __init__(self,field,numbers):
#         """Numbers is a list of ... list of fields.
        
#         For example, [[1,2,3,4],[5,6,7,8],[9,10,11,12], [13,14,15,16]]
#         represents a list of 4 groups of fields. 

#         Questions are of a form (l,succ), with l a list, and succ a
#         Boolean, stating whether the successor of this element should
#         be seen. For example:
#         - ([a,b],False) means that the b-th element of the a-th group
#         is asked. 
#         - ([a],False) means that the whole a-th group is asked. Question
#         - ([1],True) means that the first two groups are asked.
#         - ([1,4],True) means that the fourth element of the 1rst group
#         is asked, and its successor is also asked. That is, first
#         element of second group.
#         - ([],False) means: ask everything.
#         """

class NumberedFields(ListFields):
    #can not be normal
    """Similar to ListFields, where the fields are of the form
    fieldPrefix, followed by an integer between 1 and greater. """
    def __init__(fieldPrefix, greater, *args, **kwargs):
        fields = [f"""{fieldPrefix}{i}""" for i in range(1,greater+1)]
        super.__init__(fields, *args, **kwargs)

class HTML(SingleChild):
    """A html tag, and its content.

    A tag directly closed, such as br or img, should have child empty
    (default value). Values are escaped.
    If child is an Empty object, then toKeep is assumed to be
    true."""

    def __init__(self, tag, params=[],child = empty, toKeep = None
                 *args, **kwargs):
        self.tag = tag
        self.params = params
        if toKeep is None and child == empty:
            toKeep = True
        super().__init__(child , toKeep = toKeep, *args, **kwargs)

    def _getNormalForm(self):
        tag = f"""<{self.tag}"""
        for (param, value) in self.params:
            tag+= f""" {param}="{escape(value)}\""""
        if child == empty:
            return Literal(f"""{tag}/>""", toKeep = self.toKeep)
        else:
            return ListElement([Literal(f"""{tag}>"""),self.child,Literal(f"""</{self.tag}>""")], toKeep=self.toKeep).getNormalForm()

br = HTML("br")
hr = HTML("hr")
class Image(HTML):
    def __init__(self,url):
        super().__init__("img",["src",url])
class Table(HTML):
    def __init__(self, content, trParams = [], tdParams = [] *args, **kwargs):
        """
        A table with content stated. If content is empty, its normal
        form is an Empty object.
        
        content -- a list of n lists of m fields. Assuming each
        element of content have the same length. """
        table = []
        for content_ in content:
            line = []
            for content__ in content_:
                line.append(HTML(tag = "td",
                                 params = tdParams,
                                 child = content))
            table.append(HTML(tag = "tr",
                              params = trParams,
                              child = ListElement(elements = line)
            ))
        super().__init__("table", child = ListElement(elements =
        table), *args, **kwargs)

def _fixedTag(tag):
    class FIXED(HTML):
        def __init__(self,*args, **kwargs):
            super().__init__(tag,*args, **kwargs)
    return FIXED
SPAN = _fixedTag("span")
DIV = _fixedTag("div")
P = _fixedTag("p")
# class SPAN(HTML):
#     def __init__(self,*args, **kwargs):
#         super().__init__("span",*args, **kwargs)
# class DIV(HTML):
#     def __init__(self,*args, **kwargs):
#         super().__init__("div",*args, **kwargs)
# class P(HTML):
#     def __init__(self,*args, **kwargs):
#         super().__init__("p",*args, **kwargs)
