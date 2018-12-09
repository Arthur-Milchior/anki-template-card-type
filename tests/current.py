#print("current")
from .imports import *

decoratedField = DecoratedField("FrontField")
print(f"""decorated: {decoratedField}""")
normal = decoratedField.getNormalForm()
print(f"""normal: {normal}""")
withoutRedundance = normal.getWithoutRedundance()
print(f"""withoutRedundance: {withoutRedundance}""")
print("Compute restriction")
modelApplied = withoutRedundance.restrictToModel(model)
print(f"""modelApplied: {modelApplied}""")



