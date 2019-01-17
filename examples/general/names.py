from ...generators import *
from .short_head import short_header
from .foot import footer

def localFunExtra(i):
    return (lambda f:
            {"child":Parenthesis(DecoratedField(field=f"{f}{i}",
                                                label=f,
                                                suffix="",
                                                classes = f)),
             "filledFields":[f"{f}{i}"]})

def _name_extra(i=""):
    field = f"Name{i}"
    relatedInformation = ListFields(fields = [f"Abbreviation", f"French", f"Etymology"],
                                    localFun = localFunExtra(i) )
    return relatedInformation

def localFun(i=""):
    return {"child":LI([QuestionnedField(f"Name{i}",classes=["Name"]),
                        NotAsked(f"Name{i}",_name_extra(i))]),
            "questions":f"Name{i}",
            "filledFields":[f"Name{i}"]}

_names = ["Names: ",
          ListFields(fields = ["","2","3","4"],
                     localFun = localFun,
                     globalFun = (lambda l: UL(l,addLi=False)))]

singleName = DecoratedField("Name",suffix=[_name_extra(),br])

name_s= Filled("Name",
               child=[
                   Cascade(child=FilledOrEmpty("Name2",
                                               _names,
                                               singleName),
                           field="Names",
                           cascade=["Name","Name2","Name3","Name4"]),
                   hr])
names = ("Name2",[short_header,_names, footer])

