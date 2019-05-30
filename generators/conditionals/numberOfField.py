from ...debug import debugFun, debugInit, debug
from ..leaf import emptyGen
from .filledOrEmpty import FilledOrEmpty
from ..constants import *
from ..generators import Gen, NotNormal, SingleChild, genRepr
from ..conditionals.askedOrNot import AskedOrNot
from ...utils import checkField


# class AtMostNField(SingleChild, NotNormal):
#     """Show the child if at most n of the fields have content.

#     If there are m fields, then the length of the text generated is
#     O(m choose n). For n=1, it means the text is linear in the number
#     of fields. For n=2, it means the text is square in the number of fields.

#     So use this only for small text, such as
#     <table>.
#     """

class AtLeastNField(SingleChild, NotNormal):
    """Show the child if at least n of the fields satisfy a property.

    By default, the property is that those fields have content. In
    this case, if there are m fields, then the length of the text
    generated is O(m choose n). For n=1, it means the text is linear
    in the number of fields. For n=2, it means the text is square in
    the number of fields.

    So use this only for small texts.

    If asked is set to True, instead of checking for content, it is
    checked whether at least n fields are asked.

    """
    #@debugInit
    def __init__(self, child, fields, otherwise = None, asked = False, n=1):
        self.n = n
        self.asked = asked
        self.setOfRequiredFields = fields
        for field in fields:
            checkField(field)
        assert assertType(fields,list)
        self.otherwise=otherwise
        super().__init__(child)
        self.child = self._ensureGen(child)
        self.otherwise = self._ensureGen(otherwise)

    def _repr(self):
        t="""AtLeastNField(\n"""
        t+=f"""{genRepr(self.child, label ="child")},\n"""
        t+=f"""{genRepr(self.setOfRequiredFields, label="fields")},\n"""
        if self.otherwise is not None:
            t+=genRepr(self.otherwise,label= "otherwise")+",\n"
        if self.otherwise is not False:
            t+=genRepr(self.asked,label= "asked")+",\n"
        if self.n is not 1:
            t=",\n"+genRepr(self.n,label= "n")+"\n"
        t+=")"
        return t

    @debugFun
    def _getNormalForm(self):
        if self.n == 0:
            return self.child.getNormalForm()
        if self.n> len(self.setOfRequiredFields):
            return self.otherwise.getNormalForm()
        element = self.setOfRequiredFields[-1]
        remaining = self.setOfRequiredFields[:-1]
        positiveCase = AtLeastNField(child = self.child,
                                     fields = remaining,
                                     otherwise = self.otherwise,
                                     asked = self.asked,
                                     n = self.n-1)
        negativeCase = AtLeastNField(child = self.child,
                                     fields = remaining,
                                     otherwise = self.otherwise,
                                     asked = self.asked,
                                     n = self.n)
        clas = AskedOrNot if self.asked else FilledOrEmpty
        dichotomy = clas(element,
                         positiveCase,
                         negativeCase,
        )
        return dichotomy.getNormalForm()


class AtLeastOneField(AtLeastNField):
    def __init__(self,*args,**kwargs):
        super().__init__(*args, n=1,**kwargs)

class AtLeastTwoFields(AtLeastNField):
    def __init__(self,*args,**kwargs):
        super().__init__(*args, n=2,**kwargs)
