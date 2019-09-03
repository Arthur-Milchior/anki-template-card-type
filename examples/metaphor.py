from ..generators import *
from .general import footer, header

numbers = [""]+[str(i) for i in range(2,6)]
sides = ["Left","Right"]
table = Table(
    [
        Filled("Left"+number,
               TR([
                   TD(QuestionnedField(side+number))
                   for side in sides])
        )
        for number in numbers
    ]
)


metaphor = [header, table, footer]
