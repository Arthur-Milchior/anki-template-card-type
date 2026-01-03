# Closure
## Rationale
In order to explain this note type, I'll introduce a very basic
mathematical example. This example require only you to have heard of
fractions (the number of the form 3/4), additions, multiplications and
square root. You don't even need to recall what all of those are.

As a mathematician, it's often useful to recall which mathematical
operations preserve some property. For example, the sum of two
fractions is a fraction. The product of two fractions is also a
fraction. However, the square root of a fraction is not a fraction in
general. Its a fraction if both numbers of the fractions are pure
square. I.e. are of the form 3*3. The exponential of a fraction is
sometime a fraction sometime not, there is no clear rules for this.

Thus, I need to have question of the following form:
* Fractions are ??? closed under addition when ???
* Fractions are ??? closed under square root when ???
* Fractions are ??? closed under exponential when ???
And the answers are:
* Fractions are under addition
* Fractions are closed under square root when both of its numbers are pure square.
* Fractions are not closed under exponential


I also want the following question:
> Fractions are:
> ??? closed under ??? when ???
> closed under square root when both of its numbers are pure square.
> not closed under exponential
whose answer is
> Fractions are:
> closed under addition
> closed under square root when both of its numbers are pure square.
> not closed under exponential

The first kind of questions ensure that I recall which are the
conditions under which fractions are closed under a particular
operations. The second kind of questions ensure that I recall every
operations which I have entered in anki.

## The code 
### Fields
For this note type I need 4 kinds of fields:
* ```Name```: here it's «Fractions»
* ```Not1```, ```Case1```, ```Condition1```: here the values are
  ("","addition",""), ("","square root", "both of its numbers are pure
  square") and ("not","exponential",""). Of course, there are also
  fields called ```Not2```, ```Case2```, ```Condition2``` and so on.
  
### Python
As usual, I begin by importing the library of this addon with:
```
from .general import header, footer
```

#### Label
Then I create the questions, piece by piece. The label is created by:
```
label=[{"Name"}," are"]
```

#### Closed under
We consider here the part ```closed under {{case1}}```. Its simply a
decorated field:
```
DecoratedField(field=f"Case1",
                      label="closed under ",
                      classes="Case",
                      infix="",
                      suffix="")
```

Since we may want to have the same thing for each case, we create a
function which generate this kind of field. This function takes, as
argument, the number of the field we consider. The function is:
```
def cu(i):
    return DecoratedField(field=f"Case{i}",
                          label="closed under ",
                          classes="Case",
                          infix="",
                          suffix="")
```

Note that, using a DecoratedField, it ensures that «Closed under» is
emphasized when the question ```Case1``` is asked. By emphasized, I
means that it will have both the CSS classes ```Questions``` 
and ```Case1```.

#### Condition
We now consider the conditions for the closure to hold. If a question
is asked, it should display «when ???». If no question is asked, it
should either display nothing, if the field ```Condition``` is
empty. Or display ```when {{Condition}}``` if the field is filled. 

To test whether the condition is filled or not, I do:
```
df=DecoratedField(field=f"Condition{i}",
                  label="when ",
                  classes="Condition",
                  infix="",
                  suffix="")
```
The ```i``` represents the number of the current question. Because, as
you may recall from the field names, we create multiple similar
questions.

Then, to display the question side, I use:
```
question=[Label("when",
                fields=[f"Conditions",f"Condition{i}",f"Case{i}"],
                classes=["Condition"]),
          " ???"]
```
In order to consider whether a question related to the ```i```-th case
    is asked, we do:
```
alo=AtLeastOneField(fields=[f"Conditions",f"Condition{i}",f"Case{i}"],
                    asked=True,
                    child=question,
                    otherwise=df)
```
Finally, to ensure to display the ??? only on the question side, we do:
```
return QuestionOrAnswer(alo,
                        df)
```

The whole code of the function generating this «when» part is:
```
def when(i):
    df=DecoratedField(field=f"Condition{i}",
                      label="when ",
                      classes="Condition",
                      infix="",
                      suffix="")
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
```
#### «Not» part
The «not» part is quite similar to the «when» part. The main
difference being that the value of the field is not important. If the
field ```Not1``` is filled we assume it means that the set is not
closed under the first operation. Otherwise, if this field is empty,
the set is closed under this operation. Thus, the code to generate
this part of the question is:
```
def no(i):
    filled=Filled(f"Not{i}",
                  "not ")
    alo=AtLeastOneField(fields=[f"Condition{i}",f"Case{i}",f"Cases","Conditions"],
                        asked=True,
                        child="???",
                        otherwise=filled)
    return QuestionOrAnswer(alo,
                            filled)
```
#### The question line:
We now consider the whole part: "(not) closed under (operation) when
(condition)". This is the part of the line used in both kinds of
questions.

```
def line(i):
    return [no(i),cu(i),when(i)]
```
As we can see, this part of the line is just a list using the three
pieces we created before.

#### A card with a single case
We now consider the first of the two kinds of questions we have seen
in the introduction. This question consider a single operation.

```
def closed(i):
    return [label,line(str(i))]
```

#### A card with every cases:
We now consider the second kind of questions, with a case by
line. This question display every informations from the card appart
from the missing case. 

```
closeds = NumberedFields(fieldPrefix = "Case",
                         greater=11,
                         label=label,
                         numbered_field=numbered_field,
                         localFun=(lambda i:{"child":LI(line(str(i))),
                                             "questions":{f"Case{i}"},
                                             "filledFields":[f"Case{i}"]}),
                         unordered=True,
)
```
Here, we use the generator NumberedFields, which does exactly what we
want here: it shows a label, and then an HTML list, where every lines
are the same, except that a numerical parametr change. 

Here:
* greater: this is the number of lines to show. In this case, if we
  only have three fields filled, only three lines will be shown. Thus
  you can put a number bigger than actually required.
* label: the text shown before the beginning of the list. It is
  emphasized using CSS if one of the question ```Case1```, ```Case2```
  etc... is asked.
* unordered: when set to True, it means that we don't want a number to
  prefix the list, but only a bullet point.
* localFun: a function which, given the number of the line (as a
  string), return three things: The line itself:```LI(line(i))```,
  which generate a ```LI``` html tag whose content is the result of
  the method line. The second returned value is a container which
  state that this line must not be displayed if the field Casei is
  empty. The last state that if a template asks ```Cases", then, it
  should be considered that it also ask ```Casei```. 
* fieldPrefix: this field is mostly useless because we use a localFun
  which is not the default one. Still, it ensures that every line can
  be simultaneously asked by asking ```Cases``` (i.e. ```Case``` and
  then the letter s.)
  

### Templates
The card asking in which fractions are closed under square root
(i.e. the second operation) is 
```
<span template="eval" generator="closed(2)" asked="Condition2"/>
```

The code of the card asking which is the second operation, showing
every other operations, is
```
<span template="eval" generator="closeds" asked="Case"/>
```

Finally, the card which ask everything simultaneously is:
```
<span template="eval" generator="closeds" asked="Cases"/>
```

## Note about a simplification I made in this example
The fields ```Not1```, ```Case1```, ```Condition1``` are in fact
called ```Not```, ```Case```, ```Condition```. I decided that
numberedField would send the numbers "", "2", "3", etc... It's more
beautiful, for me, if the 1 is not indicated. 
