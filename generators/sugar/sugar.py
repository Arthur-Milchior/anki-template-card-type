from ..generators import Gen
from ...debug import ExceptionInverse
class NotNormal(Gen):
    def _getWithoutRedundance(self):
        raise ExceptionInverse("_getWithoutRedundance from not normal")
    # def getWithoutRedundance(self):
    #     raise ExceptionInverse("getWithoutRedundance from not normal")
    # def assumeFieldInSet(self, *args, **kwargs):
    #     raise ExceptionInverse("assumeFieldInSet from not normal")
    def _assumeFieldFilled(self, field):
        assert False
    def _assumeFieldEmpty(self, field):
        assert False
    def _assumeFieldPresent(self, field):
        assert False
    def _assumeAnswer(self, changeStep = False):
        assert False
    def _assumeFieldAbsent(self, field):
        assert False
    # def _assumeFieldInSet(self, *args, **kwargs):
    #     raise ExceptionInverse("_assumeFieldInSet from not normal")
    def _assumeQuestion(self, *args, **kwargs):
        raise ExceptionInverse("_assumeQuestion from not normal")
    def _applyTag(self, *args, **kwargs):
        raise ExceptionInverse("_applyTag from not normal")
    def _restrictToModel(self, *args, **kwargs):
        raise ExceptionInverse("_restrictToModel from not normal")
    
    def _questionOrAnswer(self, *args, **kwargs):
        raise ExceptionInverse("_questionOrAnswer from not normal")
