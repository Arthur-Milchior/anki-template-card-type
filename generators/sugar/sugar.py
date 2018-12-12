from ..generators import Gen
class NotNormal(Gen):
    def _getWithoutRedundance(self):
        raise Exception("_getWithoutRedundance from not normal")
    def getWithoutRedundance(self):
        raise Exception("getWithoutRedundance from not normal")
    def assumeFieldInSet(self, *args, **kwargs):
        raise Exception("assumeFieldInSet from not normal")
    def _assumeFieldInSet(self, *args, **kwargs):
        raise Exception("_assumeFieldInSet from not normal")
    def restrictToModel(self, *args, **kwargs):
        raise Exception("restrictToModel from not normal")
    def _restrictToModel(self, *args, **kwargs):
        raise Exception("_restrictToModel from not normal")
    
