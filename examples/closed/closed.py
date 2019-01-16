from ..general import short_header, footer
from ...generators.imports import *

label=[Field("Name", isMandatory = True)," is"]
def no(i):
    filled=Filled(f"Not{i}",
                  "not ")
    alo=AtLeastOneField(fields=[f"Condition{i}",f"Case{i}",f"Cases","Conditions"],
                        asked=True,
                        child="???",
                        otherwise=filled)
    return QuestionOrAnswer(alo,
                            filled)

def when(i):
    df=DecoratedField(field=f"Condition{i}",
                      label="when ",
                      classes="Condition",
                      infix="",
                      suffix="",
                      isMandatory = True)
    question=[Label("when",
                    fields=[f"Conditions",f"Condition{i}",f"Case{i}"],
                    classes=["Condition"]),
              " ???"]
    alo=AtLeastOneField(fields=[f"Conditions",f"Condition{i}",f"Case{i}"],
                        asked=True,
                        child=question,
                        otherwise=df)
    return QuestionOrAnswer(alo,
                            df)
    
def closedUnder(i):
    return DecoratedField(field=f"Case{i}",
                          label="closed under ",
                          classes="Case",
                          infix="",
                          suffix="",
                          isMandatory = True)
def line(i):
    return [no(i),closedUnder(i),when(i)]
    
_closed = NumberedFields(fieldPrefix = "Case",
                         greater=11,
                         label=label,
                         localFun=(lambda i:{"child":LI(line(str(i))),
                                             "questions":{f"Case{i}"},
                                             "filledFields":[f"Case{i}"]}),
                         unordered=True,
)


closeds = [short_header, _closed, hr,footer]
def closed(i=""):
    return [short_header,
            label,
            line(str(i)),
            hr,
            footer]
            
