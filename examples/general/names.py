from ...generators import *
from .short_head import short_header
from .foot import footer

def singleRelatedInformation(i):
    return (lambda f:
            {"child":Parenthesis(DecoratedField(field=f"{f}{i}",
                                                label=f,
                                                suffix="",
                                                classes = f)),
             "filledFields":[f"{f}{i}"]})

def relatedInformations(i=""):
    field = f"Name{i}"
    return ListFields(fields = [f"Abbreviation", f"French", f"Etymology"],
                      localFun = singleRelatedInformation(i) )

def nameAndMore(i=""):
    return QuestionnedField(f"Name{i}",
                            classes=["Name"],
                            suffix = relatedInformations(i))

def singleName(i=""):
    return {"child":LI(nameAndMore(i)),
            "questions":{f"Name{i}"},
            "filledFields":[f"Name{i}"]}

listNames = [Label("Names",
                ["Name","Name2","Name3","Name4"],
                "Name"),
          ": ",
          ListFields(fields = ["","2","3","4"],
                     localFun = singleName,
                     globalFun = (lambda l: UL(l,addLi=False)))]

singleName = DecoratedField(field="Name", child=nameAndMore())

singleOrMultipleNames= Filled("Name",
                              child=[
                                  Cascade(child=FilledOrEmpty("Name2",
                                                              listNames,
                                                              singleName),
                                          field="Names",
                                          cascade={"Name","Name2","Name3","Name4"}),
                                  hr])
names = ("Name2",[short_header, listNames, footer])
