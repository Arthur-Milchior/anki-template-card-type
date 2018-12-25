from ...utils import firstTruth
from .askedOrNot import AskedOrNot
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
