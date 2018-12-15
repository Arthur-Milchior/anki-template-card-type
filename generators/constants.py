from ..debug import assertType, debugFun
class Step:
    def __init__(self, step, name):
        assert assertType(step, int)
        self.step = step
        self.name = name

    def __repr__(self):
        return f"Step({self.step},{self.name})"

    @debugFun
    def nextStep(self):
        ret = {
            BASIC: NORMAL,
            NORMAL: WITHOUT_REDUNDANCY,
            WITHOUT_REDUNDANCY: MODEL_APPLIED,
            MODEL_APPLIED: TEMPLATE_APPLIED,
        }.get(self)
        assert ret is not None
        return ret

    def __hash__(self):
        return self.step
    
    def previousStep(step):
        ret = {
            NORMAL: BASIC,
            WITHOUT_REDUNDANCY: NORMAL,
            MODEL_APPLIED: WITHOUT_REDUNDANCY,
            TEMPLATE_APPLIED: MODEL_APPLIED,
        }.get(step)
        assert ret is not None
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
MODEL_APPLIED = Step(3, "MODEL_APPLIED")
TEMPLATE_APPLIED = Step(4, "TEMPLATE_APPLIED")
EMPTY = Step(10, "EMPTY")
