from ..debug import ExceptionInverse, assertType, debugFun


class Step:
    def __init__(self, step, name):
        assert assertType(step, int)
        self.step = step
        self.name = name

    def __hash__(self):
        return self.step

    def __repr__(self):
        return f"Step({self.step},{self.name})"

    def __eq__(self, other):
        return self.step == other.step

    #@debugFun
    def nextStep(self):
        return posToStep[stepToPos[self]+1]

    def __hash__(self):
        return self.step

    def previousStep(self):
        return posToStep[stepToPos[self]-1]

    def union(self, other):
        return max(self,other)

    def __le__(self, other):
        return self.step <= other.step
    def __lt__(self, other):
        return self.step < other.step

BASIC = Step(0, "BASIC")
NORMAL = Step(1, "NORMAL")
WITHOUT_REDUNDANCY = Step(2, "WITHOUT_REDUNDANCY")
QUESTION_ANSWER = Step(3, "QUESTION_ANSWER")
MODEL_APPLIED = Step(4, "MODEL_APPLIED")
HIDE = Step(5, "HIDE")
ASKED = Step(6, "ASKED")
MANDATORY = Step(7, "MANDATORY")
FORBIDDEN = Step(8,"FORBIDDEN")
#QUESTIONS = Step(8, "QUESTIONS")
LAST_GEN_STEP = FORBIDDEN

TAG = Step(9, "TAG")#used for debugging
EMPTY = Step(100, "EMPTY")
l = [BASIC,NORMAL, WITHOUT_REDUNDANCY, QUESTION_ANSWER, MODEL_APPLIED, HIDE, ASKED, MANDATORY, FORBIDDEN#, QUESTIONS
     , TAG]
posToStep = {i:l[i] for i in range(len(l))}
stepToPos = {l[i]:i for i in range(len(l))}
