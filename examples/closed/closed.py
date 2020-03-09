from ...generators import *
from ..general import footer, short_header

label = [Field("Name", isMandatory=True), " "]


def no(i):
    filled = Filled(f"Not{i}",
                    "not ")
    alo = AtLeastOneField(fields=[f"Condition{i}", f"Under{i}", f"Unders", "Conditions"],
                          asked=True,
                          child=markOfQuestion,
                          otherwise=filled)
    return QuestionOrAnswer(alo,
                            filled)


def when(i):
    df = DecoratedField(field=f"Condition{i}",
                        label="when ",
                        classes="Condition",
                        infix="",
                        suffix="",
                        isMandatory=True)
    question = [Label("when",
                      fields=[f"Conditions", f"Condition{i}", f"Under{i}"],
                      classes=["Condition"]),
                markOfQuestion]
    alo = AtLeastOneField(fields=[f"Conditions", f"Condition{i}", f"Under{i}"],
                          asked=True,
                          child=question,
                          otherwise=df)
    return QuestionOrAnswer(alo,
                            df)


def closedUnder(i):
    filled = [FilledOrEmpty(f"Prefix{i}",
                            Field(f"Prefix{i}"),
                            ""),
              " ",
              no(i),
              " ",
              Field(f"Closure{i}")]
    unfilled = ["is ", no(i), " closed under"]
    return DecoratedField(field=f"Under{i}",
                          label=FilledOrEmpty(f"Closure{i}",
                                              filled,
                                              unfilled),
                          classes="Under",
                          infix="",
                          suffix="",
                          isMandatory=True)


def line(i):
    return [closedUnder(i), " ", when(i)]


_closed = NumberedFields(fieldPrefix="Under",
                         greater=11,
                         label=label,
                         localFun=(lambda i: {"child": LI(line(str(i))),
                                              "questions": {f"Under{i}"},
                                              "filledFields": [f"Under{i}"]}),
                         unordered=True,
                         )


def counterExample(i=""):
    return Answer(DecoratedField(field=f"CounterExample{i}",
                                 label="Counter example",
                                 suffix=hr))


closeds = [short_header, _closed, hr, footer]


def closed(i=""):
    return Filled(
        f"Under{i}",
        [short_header,
         label,
         line(str(i)),
         hr,
         counterExample(i),
         footer])
