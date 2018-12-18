from ...debug import ExceptionInverse, debug, debugFun
from ..leaf import emptyGen
from ..constants import *
from ..multipleChildren import MultipleChildren, ListElement
from ..singleChild import Question, Answer, SingleChild, Filled, Empty, Present, Absent, Asked, NotAsked
from .sugar import NotNormal
from ...utils import firstTruth
import sys



class FilledOrEmpty(ListElement):
    # def __repr__(self):
    #     return """FilledOrEmpty({self.field},{self.filledCase},{self.emptyCase})"""
    
    def __init__(self,field,filledCase = emptyGen, emptyCase = emptyGen,  **kwargs):
        self.filledCase = filledCase
        self.emptyCase = emptyCase
        self.field = field
        super().__init__([
            Filled(field = field, child = filledCase),
            Empty(field = field, child = emptyCase),],  **kwargs)
        

# class Filled(FilledOrEmpty):
#     def __init__(self, field, child,  **kwargs):
#         self.child = child
#         super().__init__(field, filledCase = child,  **kwargs)
#     # def __repr__(self):
#     #     return f"""Filled({self.field},{self.child})"""
        
# class Empty(FilledOrEmpty):
#     def __init__(self, field, child,  **kwargs):
#         self.child = child
#         super().__init__(field, emptyCase = child,  **kwargs)
#     # def __repr__(self):
#     #     return f"""Empty({self.field},{self.child})"""
    
# class Question(QuestionOrAnswer):
#     def __init__(self, child,  **kwargs):
#         self.child = child
#         super().__init__(question = child,  **kwargs)
#     # def __repr__(self):
#     #     return f"""Question({self.field},{self.child})"""

# class Answer(QuestionOrAnswer):
#     def __init__(self, child,  **kwargs):
#         self.child = child
#         super().__init__(answer = child,  **kwargs)
#     # def __repr__(self):
#     #     return f"""Answer({self.field},{self.child})"""
        
class PresentOrAbsent(ListElement):
    def __init__(self,field,presentCase = emptyGen, absentCase = emptyGen,  **kwargs):
        self.presentCase = presentCase
        self.absentCase = absentCase
        self.field = field
        super().__init__([
            Present(field = field, child = presentCase),
            Absent(field = field, child = absentCase),],  **kwargs)
    # def __repr__(self):
    #     return f"""PresentOrAbsent({self.field},{self.presentCase},{self.absentCase})"""
    
# class Present(PresentOrAbsentField):
#     def __init__(self, field, child,  **kwargs):
#         self.child = child
#         super().__init__(field, presentCase = child,  **kwargs)
#     # def __repr__(self):
#     #     return f"""Present({self.field},{self.child})"""
        
# class Absent(PresentOrAbsentField):
#     def __init__(self, field, child,  **kwargs):
#         self.child = child
#         super().__init__(field, absentCase = child,  **kwargs)
#     # def __repr__(self):
#     #     return f"""Absent({self.field},{self.child})"""


class Requirement(SingleChild, NotNormal):
    """Conditional. Both about the content of the field. And the existence of the field in the model. Also allow to remove a child. And request that this is a question side.


    requireFilled -- the fields which must have some content, (and thus be present in the model)
    requireEmpty -- the field must be either requireEmpty or absentOfModel of the model
    requireInModel -- the field must be present in the model. 
    requireAbsentOfModel -- the field must not belong to the model
    remove -- named descendant to remove.

    requirements -- the map of set to use if the other value is not explicitly given.
    """
    def __init__(self,
                 requirements = None,
                 
                 requireFilled = None,
                 requireEmpty = None,
                 requireInModel = None,
                 requireAbsentOfModel = None,
                 remove = None,
                 
                 state = BASIC,
                 **kwargs):
        self.requirements = dict()
        for (name, param) in[("requireFilled", requireFilled),
                             ("remove", remove),
                             ("requireEmpty", requireEmpty),
                             ("requireInModel", requireInModel),
                             ("requireAbsentOfModel", requireAbsentOfModel)]:
            default = frozenset()
            fun = frozenset
            if param is not None:
                self.requirements[name] = fun(param)
            elif requirements is not None:
                self.requirements[name] = fun(requirements.get(name,default))
            else:
                self.requirements[name] = default
        inconsistent = self.isInconsistent()
        if inconsistent:
            print("Inconsistent requirements.",file=sys.stderr)
            state = EMPTY
        super().__init__(state = state,
                         **kwargs)

    @debugFun
    def _getNormalForm(self):
        current = self.getChild()
        assoc = {"requireFilled":Filled,
                 "remove": None,
                 "requireEmpty":Empty,
                 "requireInModel":Present,
                 "requireAbsentOfModel":Absent}
        for key in assoc:
            debug(f"  Considering key {key}")
            gen = assoc[key]
            for field in self.requirements[key]:
                debug(f"    Considering field {field}")
                current = gen(field = field, child = current)
                debug(f"    current now is {current}")

        return current.getNormalForm()
    # def clone(self, elements):
    #     assert len(elements) ==1
    #     element = elements[0]
    #     if element == self.child:
    #         return self
    #     return Requirement(requirements = self.requirements,
    #                        child = element)
        
    
    # def __repr__(self):
    #     t = f"""Requirement(child = {self.child}"""
    #     for key in self.requirements:
    #         set_ = self.requirements[key]
    #         if set_:
    #             t+=f", {key}={self.requirements[key]}"
    #     t+=f", {self.params()})"
    #     return t

    def __eq__(self,other):
        return super().__eq__(other) and isinstance(other,Requirement) and self.requirements == other.requirements
    
    def isInconsistent(self):
        #debug(f"""isInconsistent("{self}")""",1)
        for left, right in [("requireFilled", "requireEmpty"), ("requireFilled", "requireAbsentOfModel"), ("requireInModel", "requireAbsentOfModel")]:
            intersection = self.requirements[left] & self.requirements[right]
            #debug(f"""Computing intersection of {left} and {right}, ie. "{self.requirements["requireFilled"]}" & "{self.requirements["requireEmpty"]}".""")
            if intersection:
                #debug(f"is not empty, thus {filledAndEmpty}, thus returning True", -1)
                return True
        #debug(f"""isInconsistent() returns False""",-1)
        return False
            
        
    # def _getWithoutRedundance(self):
    #     child = self.child
    #     for requirementName in ["requireFilled", "remove", "requireEmpty", "requireInModel", "requireAbsentOfModel"]:
    #         for field in self.requirements[requirementName]:
    #             child = child.assumeFieldInSet(field, requirementName)
    #     if child == self.child:
    #         self.setState(WITHOUT_REDUNDANCY)
    #         return self
    #     if not child:
    #         return emptyGen
    #     return Requirement(child = child,
    #                        requirements = self.requirements,
    #                        state = WITHOUT_REDUNDANCY)
        
    # def _assumeFieldInSet(self, field, setName):
    #     contradictorySets = {"RequireAbsentOfModel":{"requireFilled", "requireInModel"},
    #                          "requireInModel":{"requireAbsentOfModel"},
    #                          "requireEmpty":{"requireFilled"},
    #                          "requireFilled": {"requireEmpty", "requireAbsentOfModel"},
    #                          "remove": frozenset()}
    #     for contradictorySet in contradictorySets[setName]:
    #         if field in contradictorySet:
    #             return emptyGen
        
    #     redudantSets = {"RequireAbsentOfModel":"requireEmpty",
    #                     "requireInModel": None,
    #                     "requireEmpty": None,
    #                     "requireFilled": "requireInModel",
    #                     "remove": None}
    #     redudantSet = redudantSets[setName]
    #     requirements = copy.copy(self.requirements)
    #     change = False
    #     if redudantSet and field in self.requirements[redudantSet]:
    #         requirements[redudantSet] = requirements[redudantSet]-{field}
    #         change = True
    #     if field in self.requirements[setName]:
    #         requirements[setName] = requirements[setName]-{field}
    #         change = True
    #     if change: #since self is not redundant, the removed requirement was already taken in consideration.
    #         child = self.child
    #     else:
    #         child = self.child.assumeFieldInSet(field,setName)
    #         if not child:
    #             return emptyGen
    #         if child == self.child:
    #             return self
    #     if (requirements["requireFilled"] or
    #         requirements["requireEmpty"] or
    #         requirements["requireInModel"] or
    #         requirements["requireAbsentOfModel"] or
    #         requirements["remove"]):
    #         return Requirement(child = child,
    #                            requirements = self.requirements)
    #     else:
    #         return child

    # @debugFun
    # def _restrictToModel(self,model):
    #     fields = modelToFields(model)
    #     #debug(f"""Requirement._restrictToModel({self},{model},{fields})""",1)
    #     if fields is None:
    #         fields =  modelToFields(model)
    #         #debug(f"""Fields become {fields} """)
    #     shouldBeInModel = self.requirements["requireInModel"] - fields
    #     if shouldBeInModel:
    #         #debug(f"""should be in model: {shouldBeInModel}. Thus empty.""")
    #         return emptyGen
    #     cantBiFilledIfAbsent = self.requirements["requireFilled"] - fields
    #     if cantBiFilledIfAbsent:
    #         #debug(f"""should be in model: {cantBiFilledIfAbsent}. Thus empty.""")
    #         return emptyGen
    #     shouldBeAbsent = self.requirements["requireAbsentOfModel"]&fields
    #     if shouldBeAbsent:
    #         #debug(f"""should be absent: {shouldBeAbsent}. Thus empty.""")
    #         return emptyGen
    #     child = self.child.restrictToModel(model)
    #     if not child:
    #         #debug(f"""Child false: {child}, thus empty""")
    #         return emptyGen
    #     ret = Requirement(child = child,
    #                       requireFilled = self.requirements["requireFilled"],
    #                       requireEmpty = self.requirements["requireEmpty"] & fields,
    #                       remove =  self.requirements["remove"])
    #     #debug(f"Requirement._restrictToModel() returns {ret}",-1)
    #     return ret

    # def _applyTag(self, tag, soup):
    #     assert soup is not None
    #     conditional_span = soup.new_tag(f"span", createdBy="conditionals")
    #     self.child.applyTag(conditional_span, soup)
    #     for (set, symbol) in [
    #             (self.requirements["requireFilled"],"#"),
    #             (self.requirements["requireEmpty"],"^")
    #     ]:
    #         for element in set:
    #             before = NavigableString(f"""{{{{{symbol}{element}}}}}""")
    #             after = NavigableString(f"""{{{{/{element}}}}}""")
    #             #debug(f"Enclosing {conditional_span} by {before}/{after}")
    #             conditional_span.insert(0,before)
    #             conditional_span.append(after)
    #     #debug(f"Extending {tag} by {conditional_span}")
    #     tag.contents.extend(conditional_span.contents)
    #     if self.requirements["remove"]:
    #         raise ExceptionInverse(f"Asking to require to remove something")
    #     if  self.requirements["requireInModel"]:
    #         raise ExceptionInverse(f"Asking to require the presence of a thing in model")
    #     if self.requirements["requireAbsentOfModel"]:
    #         raise ExceptionInverse(f"Asking to require the absence of a thing in model")
class QuestionOrAnswer(ListElement):
    """The class which expands differently in function of the question/answer side."""
    def __init__(self,
                 question = None,
                 answer = None,
                 **kwargs):
        self.question = question
        self.answer = answer
        super().__init__([Question(question), Answer(answer)], **kwargs)

class AskedOrNot(ListElement):
    """The class which expands differently in function of whether a name is asked or not."""
    def __init__(self,
                 field,
                 asked = None,
                 notAsked = None,
                 **kwargs):
        self.asked = asked
        self.notAsked = notAsked
        super().__init__([Asked(field = field, child = asked), NotAsked(field = field,child = notAsked)], **kwargs)

class Branch(AskedOrNot):
    """The class which expands differently in function of the question/hidden value.

    name -- the name of this question.
    children[isQuestion][isAsked] -- the field to show on the side question/answer of card (depending on isQuestion). Depending on whether this value is asked or not.
"""

    def __init__(self,
                 name = None,
                 default = None,
                 question = None,
                 answerAsked = None,
                 answerNotAsked = None,
                 answer = None,
                 asked = None,
                 notAsked = None,
                 questionAsked = None,
                 questionNotAsked = None,
                 children = dict(),
                 **kwargs):
        """
        The value of self.children[isQuestion,isAsked] is:
        {isQuestion}{IsAsked} if it exists.
        {isAsked} if it exists
        {isQuestion} if it exists
        children[isQuestion,isAsked]
        {default} if it exists
        empty otherwise.

        """
        self.inputs = dict()
        def addIfNotNone(key, value):
            if value is not None:
                self.inputs[key] = value
        addIfNotNone("default", default)
        addIfNotNone("question", question)
        addIfNotNone("answerAsked", answerAsked)
        addIfNotNone("answerNotAsked", answerNotAsked)
        addIfNotNone("answer", answer)
        addIfNotNone("asked", asked)
        addIfNotNone("notAsked", notAsked)
        addIfNotNone("questionAsked", questionAsked)
        addIfNotNone("questionNotAsked", questionNotAsked)
        addIfNotNone("children", children)
        addIfNotNone("name", name)
 
        questionAsked = firstTruth([questionAsked, asked, question, children.get((True,True)), default, emptyGen])
        questionNotAsked = firstTruth([questionNotAsked, notAsked, question, children.get((True,False)), default, emptyGen])
        answerAsked = firstTruth([answerAsked, asked, answer, children.get((False,True)), default, emptyGen])
        answerNotAsked = firstTruth([answerNotAsked, notAsked, answer, children.get((False,False)), default, emptyGen])
        
        asked = questionAsked if questionAsked == answerAsked else QuestionOrAnswer(questionAsked, answerAsked, **kwargs)
        notAsked = questionNotAsked if questionNotAsked == answerNotAsked else QuestionOrAnswer(questionNotAsked, answerNotAsked, **kwargs)

        super().__init__(field = name,
                         asked = asked,
                         notAsked = notAsked,
                         **kwargs)

    # def __repr__(self):
    #     t= f"Branch("
    #     for key in self.inputs:
    #         t+=f"{key}: {self.inputs[key]}, "
    #     t+=")"
    #     return t
