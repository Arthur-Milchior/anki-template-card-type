from ..generators import Gen
class NotNormal(Gen):
    def _getWithoutRedundance(self):
        raise Exception("_getWithoutRedundance from not normal")
    # def getWithoutRedundance(self):
    #     raise Exception("getWithoutRedundance from not normal")
    # def assumeFieldInSet(self, *args, **kwargs):
    #     raise Exception("assumeFieldInSet from not normal")
    def _assumeFieldInSet(self, *args, **kwargs):
        raise Exception("_assumeFieldInSet from not normal")
    def _assumeQuestion(self, *args, **kwargs):
        raise Exception("_assumeQuestion from not normal")
    def _applyTag(self, *args, **kwargs):
        raise Exception("_applyTag from not normal")
    def _template(self, *args, **kwargs):
        raise Exception("_template from not normal")
    def _restrictToModel(self, *args, **kwargs):
        raise Exception("_restrictToModel from not normal")
    
