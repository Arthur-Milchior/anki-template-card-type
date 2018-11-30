import copy
from .structures.child import Requirement
from .structures.generator import Gen

class Leaf(Gen):
    pass

class Empty(Leaf):
    """A generator without any content"""
    def __init__(self):
        super().__init__(normalized = True, toKeep = False)
    def __bool__(self):
        return False
    def _mustache(self, *args, **kwargs):
        return ""
    def _restrictFields(self,fields,empty,hasContent):
        return self
    
empty = Empty()

class Literal(Leaf):
    """A text to be printed, as-is, unconditionally."""
    def __init__(self,
                 questionSide,
                 answerSide = None,
                 normalized = True,
                 toKeep = False,
                 *args,
                 **kwargs):
        super.__init__(*args, toKeep = toKeep, **kwargs)
        self.questionSide = questionSide
        self.answerSide = answerSide or questionSide

    def _mustache(self, asked = None, question = None):
        return self.questionSide if question else self.answerSide
    def _restrictFields(self,fields,empty,hasContent):
        return self

class Field(Leaf):
    def __init__(self,
                 field,
                 question = None,
                 prefix = empty,
                 suffix = empty,
                 symbol = None,
                 separator = " : ",
                 toKeep = True,
                 absence = empty,
                 *args, **kwargs)
        """
        keyword arguments:
        field -- a field name. Corresonding to the information requested here.
        separator -- Text to show between prefix and field value. Never emphazed.
        prefix/suffix -- Text with which to start/end everything.
        symbol -- Text to show before the field content. If not provided, it's value is "field". Emphasized on uqestions.
        question -- Text to show on the question side when field is asked. By default it is "emphasize(symbol) separator ???"
        absence -- the text to show if the field is empty

        * Normal form of answer is: "symbol separator emphasize({{field}})" 
        * Normal form of everything else is: "symbol separator {{field}}".
        """
    
        super().__init__(*args, toKeep = toKeep, **kwargs)
        self.field = field
        self.separator = separator
        self.suffix = suffix
        self.prefix = prefix 
        self.symbol = symbol if symbol else f"""{field}"""
        self.question = question if question else f"""self.emphasize({self.prefix}){self.separator}???"""
        self.text = f"""{self.prefix}{{{{{field}}}}}{self.suffix}"""
        self.answer = f"""{self.prefix}self.emphasize({{{{{field}}}}}){self.suffix}"""
        self.absence = absence

    def _getNormalForm(self):
        field = copy.deepcopy(self)#I can deepcopy, because it's a
        #field, thus shallow
        
        field.normalized = True
        return Requirement(self, required = {self.field})
        
    def isAsked(self, asked):
        """Whether current field is an asked field"""
        return asked and self.field in asked
    
    def _mustache(self,asked = None, question = None):
        if self.isAsked(asked):
            if question:
                return self.question
            else:#answer
                return self.answer
        else: #normal field            
            return self.text

    def _restrictFields(self,fields,empty,hasContent):
        if self.field in hasContent and self.field not in empty:
            return self
        else:
            return empty
