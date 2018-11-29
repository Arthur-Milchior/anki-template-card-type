
class context:
    def __init__(self,fieldsInModel):
        self.fieldsInModel = fieldsInModel
        
class gen:
    """
    present: the set of fields requested by ancestors
    absent: the set of fields requested to be absent by ancestors
    parent: the class from which this class is called
    """
    def __init__(self,present = frozenset(),absent = frozenset(),parent = None):
        """

        keyword arguments:
        present -- element requested here, and not by the parents
        absent -- element requested here, and not by the parents
        parent -- the object calling this.
        """
        self.params = dict()
        self.params["present"] = present | self.presentInParent()
        self.params["absent"] = absent | self.absentInParent()
        self.params["parent"] = parent
        self.params["context"] = parent.params["context"] if parent else None
        self.params["contradiction"] = False

    def presentInParent(self):
        return parent.present if parent else frozenset()

    def absentInParent(self):
        return parent.absent if parent else frozenset()

    def presentFixedInParent(self):
        """The set of elements in parent, which are either assured to be present or absent."""
        return self.absentInParent() | self.presentFixed()
        
    def _mustache(self,asked = None, question = None):
        """The text for the template.  

        Assuming no contradiction.
        
        keyword arguments:
        question -- None if indifferent, True for question side, False for answer side
        asked -- the set of element asked in this card.
        """
        assert false

    def mustache(self,asked = None, question = None):
        """The text for the template. Or empty string in case of contradiction.

        keyword arguments:
        question -- None if indifferent, True for question side, False for answer side
        asked -- the set of element asked in this card.
        """
        if self.params["contradiction"]:
            return ""
        return self._mustache(asked = asked, question = question)
        
    def getFieldsInModel(self):
        return self.params["context"].fieldsInModel

    def formatImportantField(self,field):
        return formatImportantText(f"""{{{{{field}}}}}""")
    
    def formatImportantText(self,text):
        return f"""<emph>{{text}}</emph>"""

class SingleChild(gen):
    def addChild(self,child):
        self.params["child"] = child
        self.params["contradiction"]|= child.params["contradiction"]
        return self
        
class Root(SingleChild):
    def __init__(self,fieldsInModel,*args):
        super().__init__(*args)
        self.params["context"].fieldsInModel= fieldsInModel
        

class Requirement(singleChild):
    """Ask child, if all elements of present are present, and those of absent are absent.

    An element of present already parent's present

    """
    def __init__(self,requireds = frozenset(), forbidden = frozenset(),*args):
        newPresent =requireds  - self.presentFixedInParent()
        newAbsent = absent - self.presentFixedInParent()
        super().__init__(present = newPresent, absent = newAbsent, *args)
        self.params["requireds"] = newRequired 
        self.params["forbidden"] = newAbsent 
        self.params["contradiction"] = (requireds & self.absentInParent()) or (forbidden & self.presentInParent())
        
    def _mustache(self,asked = None, question = None):
        t = self.params["child"].mustache(asked = asked, question = question)
        if not t:
            return ""
        for (set, symbol) in [
                (self.params["requireds"],"#"),
                (self.params["rejecteds"],"^")
        ]:
            for element in set:
                t = f"{{{{{symbol}{element}}}}}{t}{{{{/{element}}}}}"
        return t
        
class askedField(gen):
    def __init__(self,field, question = None, prefix = None, suffix = None, *args)
        """

        * Normal form is: "prefix field suffix".
        * If this field is asked:
        ** if it's the question side, then:
        *** "question" if its present
        *** emphasize(prefix) ??? suffix
        ** If its the answer side, then:
        ***prefix emphasize(field) suffix
        """
    
        super().__init__(*args)
        self.params["field"] = field
        self.params["question"] = question
        self.params["prefix"] = prefix
        self.params["suffix"] = suffix
        self.params["contradiction"] = field in self.params["forbidden"]
        
        
    def isAsked(self, asked):
        """Whether current field is an asked field"""
        return asked and self.params["field"] in asked
    
    def _mustache(self,asked = None, question = None):
        if self.isAsked(asked):
            if question:
                if self.params.get("question") :
                    return self.params["question"]
                return f"""{self.formatImportantText(text=self.params["prefix"])} ??? {self.params[suffix]}"""
            else:#answer
                return f"""{self.params["prefix"]} {self.formatImportantField(field=self.params["field"])} {{self.params["suffix"]}}"""
        else: #normal field            
            return f"""{self.params["prefix"]} {{{{{self.params["field"]}}}}} {{self.params["suffix"]}}"""

class MultipleChildren(gen):
    def addChildren(self,children):
        self.params["children"] = children
        for child in children:
            if not child.params["contradiction"]:
                self.params["contradiction"] = False
        
        
class List(MultipleChildren):
    def __init__(self, prefix, separator, suffix, *args):
        super().__init__(*args)
        self.params["prefix"]=prefix
        self.params["separator"]=separator
        self.params["suffix"]=suffix

    def 
    




        
        #self.params[""]=
