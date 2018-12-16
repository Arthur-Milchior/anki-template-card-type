from ..debug import assertType, debugFun
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
    
    @debugFun
    def nextStep(self):
        ret = {
            BASIC: NORMAL,
            NORMAL: WITHOUT_REDUNDANCY,
            WITHOUT_REDUNDANCY: MODEL_APPLIED,
            MODEL_APPLIED: QUESTION_ANSWER,
            QUESTION_ANSWER: TEMPLATE_APPLIED,
        }.get(self)
        if ret is None:
            raise Exception(f"""Next step of {step} does not exists.""")
        return ret

    def __hash__(self):
        return self.step
    
    def previousStep(step):
        ret = {
            NORMAL: BASIC,
            WITHOUT_REDUNDANCY: NORMAL,
            MODEL_APPLIED: WITHOUT_REDUNDANCY,
            QUESTION_ANSWER: MODEL_APPLIED,
            TEMPLATE_APPLIED: QUESTION_ANSWER,
        }.get(step)
        if ret is None:
            raise Exception(f"""Previous step of {step} does not exists.""")
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
EMPTY = Step(10, "EMPTY")
