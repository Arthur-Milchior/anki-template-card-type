# Relation
This example is kinda similar to (closed)[../closed/README.md], but
more complicated. Once again, this note type is used mostly for
mathematics notes, but should be understandable by anyone. The other
similarity is that it's a note type containing a lot of related
informations, and I want in some cards either to display all, or to
display only a part of it.


## Example
I'll introduce a bunch of examples.  Those examples are totally
fictitious. But I believe them to be easy enough examples.

I need multiple examples because this note type allows to do multiple
kinds of questions simultaneously.

### List of implications

Let's consider the following geometric figures with four sides:
* square
* rectangle
* parallelogram
* trapeze

Let's say I want to recall which figures is a particular case of which
other figure. So, let's say I've got a geometry figure ```F```, I want
to have questions of the kind:

* F is a square ??? F is a rectangle
* F is a parallelogram ??? F is a rectangle

In the first case, the answer is «implies», in the second case, it is
«is implied by».

I also want to have a question of the form:
> F is square implies F is a ??? implies F
> is a parallelogram implies F is a trapeze.

In this case, the missing part is "rectangle".

We use six fields for this example:
* Smallest: "a square"
* Smaller0: "a rectangle"
* Greater0: "a parallelogram"
* Greatest: "a trapeze"
* Increasing: "implies"
* Decreasing: "implied by"
* Prefix smallest: "F is",
* Prefix smaller: "F is",
* Prefix greater: "F is",
* Prefix greatest: "F is",
(Actually, we don't need to fill the two last fields, that the value
by default)

We'll explain the reason of the number 0 in the next example. We'll
call Increasing and Decreasing the relations fields. The four other
fields will be called the "sides". The other sides are "Intermediate",
"Equivalent", "Equivalent2" and "Equivalent3".

We consider that square is the "smallest" side, because there are less
squares than rectangles. It's not really importante, but this ensure
that we are consistent with the "increasing" field, which give the
text of the relation between the smaller side and the greater side.

### Multiple part

Let us consider multiplication. We want to really know the fact that
"12*5=15*4" (don't ask me why we would want to learn that.)

We want questions of the form 
* 12*5 = 15*???
* 15*4 = ???*5 
* 12*5 ??? 15*4

You can also do this using this add-on. This time, you'll need the
following fields:
* Smaller0: 12
* Smaller1: 5
* Greater0: 15
* Greater1: 4
* Connect smaller0: *
* Connect greater0: *
* increasing: =
* decreasing: =

(actually, you don't need to fill the field decreasing if the field
increasing is filled with the value we want for decreasing. If
increasing is filled and not decreasing, then the value of increasing
is used for decreasing too. This allows to use this note type for
equivalence relation)

To be more precise in our definiton, we consider that Smaller0 and
Smaller1 belongs to the same sides. 

### Mixing both examples
You can have a part using more than two sides, where some sides have
multiple fields. Only the sides Smaller and Greater have multiple
fields. They both have four fields. In practice, I discovered I never
needed more than two sides with at least two fields. I may change the
note type if this change one day.

Mixing both examples is usefull, because, if you recall the question
> F is square implies F is ??? implies F
> is a parallelogram implies F is a trapeze.
and if you know a little bit of geometry, you may know that "diamond"
would also be a correct answer. Thus we actually need to set the
fields as follow:
* Greater1: a diamond
* Connect greater: and/or.
And the question now becomes:
> F is square implies F is ??? and/or a diamond implies F
> is a parallelogram implies F is a trapeze.

The other question may become:
* F is a sqare ??? F is a rectangle and/or a trapeze
* F is a parallelogram ??? F is a rectangle and/or a trapeze

### Hiding some questions
Sometime we don't want to ask the sides or the questions.

For example, let us consider the implication
>Socrate is a man implies Socrate is mortal
We are interested in the side of the implication, not into the actual
conclusion. After all, the question
>Socrate is a man implies ???
may have an infinite number of answers.

Thus, we have a field "Hide sides" which, when filled, ensure that
those questions are not asked.

Similarly, consider the equality
>a²-b²=(a+b)(a-b)
Clearly, the question
>a²-b² ??? (a+b)(a-b)
is useless. If we ask the question, it is pretty clear that the answer
is the equality, otherwise we would not even have asked this.
In this case, we fill a field "Hide middle", which ensure that the
only questions asked are 
* a²-b²=??? and
* ???=(a+b)(a-b)
## Code

### Generators (Python)
#### Increasing relation text
We first want to to generate the part of the code showing
"implies". More precisely, as explained above, we want to show
"{{Smaller to greater}}" if it exists, and "implies" otherwise.

This is done using the code:
```Python
foe=FilledOrEmpty("Smaller to greater",
                  {"Smaller to greater"},
                  "implies")
```
We want this to be considered to be a field which can be asked, even
if the answer of the question may be "implies" and not the actual
content of the field. Thus we use a decorated field. Thus we use a
QuestionnedField:
```Python
qf=QuestionnedField(field = "Smaller to greater",
                    child = foe)
```
We also need to add spaces around the text generated. We uses the
generator ```Parenthesis``` for that. It ensures that if no content is
generated by the QuestionnedField, then the useless spaces aren't
printed either.
```Python
increaseRelation = Parenthesis(left = " ",
                              right = " ",
                               child = qf)
```

#### Decreasing relation text
The decreasing relation text is similar to the increasing text, but it
should also consider the following case. If {{Smaller to greater}} is
filled but not {{Greater to smaller}} then we assume that the relation
is an equivalence relation (such as "=" or "if and only if") and thus
the decreasing relation is considered to be the same as the increasing
relation.

The code is:
```Python
foe=FilledOrEmpty("Smaller to greater",
                  {"Smaller to greater"},
                  "implied by")
foe = FilledOrEmpty("Greater to smaller",
                    {"Greater to smaller"},
                    foe)
qf=QuestionnedField(field = "Greater to smaller",
                    child = foe)
decreaseRelation = Parenthesis(left = " ",
                               right = " ",
                               child = qf)
```
#### The sides with multiple fields
We first want a code which shows "{{connect smaller0}} {{Smaller1}}"
if the field Smaller1 is filled, and show nothing otherwise. This is
done by:
```Python
Filled(f"Smaller1",
       [Parenthesis(left = " ", right = " ",
                    child = FilledOrEmpty(f"Connect Smaller0",
                                          {f"Connect Smaller0"},
                                          "and")),
        QuestionnedField(f"Smaller1")])
```

We may want to replace "and" by another default value ```default```,
the number by an arbitrary number ```nb``` and Smaller by another
side name ```side```. This lead to the function:

```Python
def connexion(nb,side,default = "and"):
    """{{Connect sidenb}} if field, else (default = "And"). 
    {{field side(nb+1)}}"""
    return Filled(f"{side}{nb+1}",
                  [Parenthesis(left = " ", right = " ",
                               child = FilledOrEmpty(f"Connect {side}{nb}",
                                                   {f"Connect {side}{nb}"},
                                                   default)),
                   QuestionnedField(f"{side}{nb+1}")])
```

The part showing:
```Python
{{Prefix smaller}}{{Smaller0}}{{Connect smaller0}}{{Smaller1}}...{{Suffix smaller}}
```
can finally be obtained by:
```Python
l=[{f"Prefix {side}"},
   QuestionnedField(f"{side}0"),
   connexion(0,side),
   connexion(1,side),
   connexion(2,side,default = FilledOrEmpty(f"Connect {side}0",
                                            {f"Connect {side}0"},
                                            "and")),
   {f"Suffix {side}"},]
```
Here, the default value is changed because we consider that if the
last connexion is not given, it should be considered that it's similar
to the first one.

We want to consider that if Smaller0 or Greater0 is not filled, there
is a problem. This is done using:
```Python
    foe=FilledOrEmpty(f"{side}0",
                      l,
                      CLASS("Error",f"Error, {side}0 is empty"))
```
Finally, if Smallers or Greaters is asked, we want to consider that
each field is asked, this is done using:
```Python
Cascade(field=f"{side}s",
        cascade=[f"{side}{i}" for i in range(4)],
        child= foe)
```

The whole function returing the entire side is thus:
```Python
def bigSide(side):
    """side0 connect0 side1 connect1 side2 connect2 side3"""
    l=[{f"Prefix {side}"},
       QuestionnedField(f"{side}0"),
       connexion(0,side),
       connexion(1,side),
       connexion(2,side,default = FilledOrEmpty(f"Connect {side}0",
                                                {f"Connect {side}0"},
                                                "and")),
       {f"Suffix {side}"},]
    foe=FilledOrEmpty(f"{side}0",
                      l,
                      CLASS("Error",f"Error, {side}0 is empty"))
    return Cascade(field=f"{side}s",
                   cascade=[f"{side}{i}" for i in range(4)],
                   child= foe)
                 
```
We now create the sides themselves:
```
greater = bigSide("Greater")
smaller = bigSide("Smaller")
```

#### The sides with a single field
We now want to do a similar function, but for sides with a single
field. We do it as follows:
```Python
def df(fieldName,suffix = None,prefix = None):
    return DecoratedField(label = "",infix = None,field = fieldName,suffix = suffix,prefix = prefix)
```
#### The list with every sides
Here we show the list showing every sides, and the relations between
them:
```Python
increasing_ = [df("Smallest",suffix = increaseRelation),
               smaller,
               increaseRelation,
               df("Intermediate",suffix = increaseRelation),
               greater,
               df("Greatest",prefix = increaseRelation),
               df("Equivalent",prefix = increaseRelation),
               df("Equivalent2",prefix = increaseRelation),
               df("Equivalent3",prefix = increaseRelation)]
```
Note that only a single relation is printed unconditionnaly, between
the two big sides. Every other relations are printed if they
corresponds to a field which is actually filled. The relation is shown
as prefix or suffix in a field FIELD so that it's between the big
relations and FIELD.

The list in decreasing order is similar, it is:
```Python
decreasing_ = [
    df("Equivalent3",suffix = decreaseRelation),
    df("Equivalent2",suffix = decreaseRelation),
    df("Equivalent",suffix = decreaseRelation),
    df("Greatest",suffix = decreaseRelation),
    greater,
    df("Intermediate",prefix = decreaseRelation),
    decreaseRelation
    smaller,
    df("Smallest",prefix = decreaseRelation),
]
```

#### Printing this list conditionnally.
We don't want to always print this list of fields. If "Definition" is
asked, we want to print "???" insteads. This is the case where a name
is given to the relation, and, given the name, we want to ask the
relation's name.
```Python
increasing_ = [header,AskedOrNot("Definition","???",increasing_),hr,footer]
```
Here, header and footer are variables used in every note type. We
won't consider them there.

Furthermore, if the field "Hide sides" is filled, then we don't want
to have questions of the form 
> F is square implies F is a ??? implies F
> is a parallelogram implies F is a trapeze.
Thus we'll ensure that, if a side is asked and the field "Hide sides"
is filled, nothing is printed. This is done using:
```Python
increasing = AtLeastOneField(asked = True,
                           fields = listOfSideFieldNames,
                           child = Empty("Hide sides",line),
                           otherwise = increasing_)
```
Here ```listOfSideFieldNames``` is a variable containing the name of
every fields. We won't copy it here, it's just a python list.


The decreasing line is created similarly.

#### Printing only two sides

We now consider questions of the form "F is a square ??? F is a
rectangle". That is, given two sides, we ask the relation between
them. 

We first consider the sides Smaller and Greater.
```Python
l=[header, smaller,relation,greater,hr,footer]
```
We now want to ensure that this is not shown is the field "Hide
middle" is filled. The reason being the same than for the "Hide sides"
seen above.
```Python
empty = Empty("Hide middle",l)
```
We also want to ask this question only if the fields Smaller0 and
Greater0 are filled. 
```Python
filled = Filled("Smaller0",Filled("Greater0",empty))
```

In order to avoid repeating this for each pair of questions, we put
all of this section in a function:
```Python
def relation(left,right):
    if left<right:
        relation = increaseRelation
        asked = "Smaller to greater"
    elif right<left:
        relation = decreaseRelation
        asked = "Greater to smaller"
    else :
        assert False
    relation = relation.getNormalForm().assumeAsked(asked)
    leftField = listOfSideFields[left]
    rightField = listOfSideFields[right]
    leftFieldName = listOfSideFieldNames[left]
    rightFieldName = listOfSideFieldNames[right]
    l = [header, leftField,relation,rightField,hr,footer]
    empty = Empty("Hide middle",l)
    filled = Filled(leftFieldName,Filled(rightFieldName,empty))
    return filled
```
Here, ```ListofSideFields``` is a list associating of the sides in
increasing order, and ```ListOfSideFieldNames``` is the name of the
first field of this side.

Note that ```relation(1,3)``` and ```relation(3,1)``` asks essentially
the same question. In the geometry examples, it would be:
* F is a rectangle ??? F is a parallelogram
* F is a parallelogram ??? F is a rectangle

It's still usefull to have both questions. Indeed, if you only add the
first question, you'll know the answer is always «implies», and you
would not have to think to check when the answer is «implies» or
«implied by»

### Templates
Once all of the python code is written, the templates are really easy:

To ask for the field "Greater0" you just have to write
```HTML
<span askedmandatory="Greater0" generator="decreasing"
template="eval"/>
```

To ask what is the relation between the Smaller side and the greater
side, you just have to ask
```HTML
<span generator="relation(1,3)" template="eval">
```
