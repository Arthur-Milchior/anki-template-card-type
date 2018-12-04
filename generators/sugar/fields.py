from ..children import MultipleChild, ListElement
from ..child import SingleChild, Requirement
from ..leaf import Empty, emptyGen, Leaf, Literal, Field
from .conditionals import PresentOrAbsent 
from html import escape

class Question(Leaf):
    def __init__(self,
                 field,
                 prefix = emptyGen,
                 suffix = emptyGen,
                 symbol = None,
                 answer = None,
                 question = None,
                 empty = None,
                 separator = ": ",
                 toKeep = True,
                 absenceCase = emptyGen,
                 emptyCase = emptyGen,
                 *args, **kwargs):
        """
        keyword arguments:
        field -- a field name. Corresponding to the information requested here.
        separator -- Text to show between prefix and field value. Never emphazed.
        prefix/suffix -- Text with which to start/end everything.
        symbol -- Text to show before the field content. If not provided, it's value is "field". Emphasized on uqestions.
        absenceCase -- the text to show if the field is emptyGen
        answer -- what to show for the answer of this question.

        * Normal form of answer is: "symbol separator emphasize({{field}})" 
        * Normal form of everything else is: "symbol separator {{field}}".
        """
    
        self.field = field
        self.separator = separator
        self.suffix = suffix
        self.prefix = prefix 
        self.symbol = symbol if symbol else field
        self.question = question
        self.answer = answer
        self.absenceCase = absenceCase
        self.emptyCase = emptyCase
        super().__init__(*args,
                         toKeep = toKeep,
                         **kwargs)

    def _getNormalForm(self):
        children = dict()
        longPrefix = f"{self.prefix}{self.symbol}{self.separator}"
        default = ListElement([Literal(longPrefix),Field(field),Literal(self.suffix)])
        questionAsked = self.question if self.question is not None else Literal(f"""{longPrefix}???{self.suffix}""")#TODO Emphasize
        answerAsked = self.answer if self.answer is not None else default#TODO Emphasize
        cases = Branch(name = self.field,
                       default = default,
                       questionAsked = questionAsked,
                       answerAsked = answerAsked,
                       toClone = self,
                       normalized = True)
        requirement = Requirement(child = cases,
                                  requirement = self.field,
                                  toClone = self,
                                  normalized = True)
        r = requirement
        if self.emptyCase:
            r = FilledOrEmpty(field = self.field,
                                filledCase = r,
                                emptyCase = self.emptyCase,
                                toClone = self,
                                normalized = True)
        if self.absenceCase:
            r = PresentOrAbsent(field = self.field,
                                presentCase = r,
                                absenceCase = self.absenceCase,
                                toClone = self,
                                normalized = True)
        return r.getNormalForm()

    
class ListFields(MultipleChild):#(RecursiveFields)
    """If no field is present, return emptyGen string. Otherwise, as follows:

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
                 globalPrefix = emptyGen,
                 globalSeparator = emptyGen,
                 globalSuffix = emptyGen,
                 localPrefix = emptyGen,
                 localSeparator = emptyGen,
                 localSuffix = emptyGen,
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
        super().__init__(fields, *args, **kwargs)

            
    def _addField(self,field):
        #from pure field
        if isinstance(field,Field):
            symbol = field.field
        #from field name
        elif isinstance(field,str):
            symbol = field
            field = Field(field)
        #from pair with symbol and field
        elif isinstance(field,tuple):
            symbol,field = field
            if isinstance(field,str):
                field = Field(field)
        else:
            raise Exception(field, """is neither a field name, a Field nor a pair""")
        self.fields.append(Question(field,
                                    symbol = symbol,
                                    prefix = self.localPrefix,
                                    separator = self.localSeparator,
                                    suffix = self.localSuffix))
            

    def _getNormalForm(self):
        elements = []
        if self.globalPrefix:
            elements.append(AtLeastOne(child = self.globalPrefix,
                                       conditions = self.fields))
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
    def __init__(self,fieldPrefix, greater, *args, **kwargs):
        fields = []
        assert(isinstance(fieldPrefix, str))
        assert(isinstance(greater, int))
        for i in range(1,greater+1):
            s = f"""{fieldPrefix}{i}"""
            fields.append(s)
        super().__init__(fields, *args, **kwargs)
