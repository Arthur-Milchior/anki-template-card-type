from ..debug import assertType, debugFun, ExceptionInverse
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
        ret = {
            BASIC: NORMAL,
            NORMAL: WITHOUT_REDUNDANCY,
            WITHOUT_REDUNDANCY: QUESTION_ANSWER,
            QUESTION_ANSWER: MODEL_APPLIED,
            MODEL_APPLIED: TEMPLATE_APPLIED,
            TEMPLATE_APPLIED: TAG,
        }.get(self)
        if ret is None:
            raise ExceptionInverse(f"""Next step of {self} does not exists.""")
        return ret

    def __hash__(self):
        return self.step
    
    def previousStep(step):
        ret = {
            TAG: TEMPLATE_APPLIED,
            TEMPLATE_APPLIED: MODEL_APPLIED,
            MODEL_APPLIED: QUESTION_ANSWER,
            QUESTION_ANSWER: WITHOUT_REDUNDANCY,
            WITHOUT_REDUNDANCY: NORMAL,
            NORMAL: BASIC,
        }.get(step)
        if ret is None:
            raise ExceptionInverse(f"""Previous step of {step} does not exists.""")
        return ret
    
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
TEMPLATE_APPLIED = Step(5, "TEMPLATE_APPLIED")
QUESTIONS = Step(6, "QUESTIONS")
TAG = Step(7, "TAG")#used for debugging
EMPTY = Step(10, "EMPTY")
