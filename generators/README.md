This document consider the use of generators in your code. To learn
more about the creation of new generators, go read
[https://github.com/Arthur-Milchior/anki-template-card-type/blob/master/generators/INTERNALS.md].

# Generators
A generator is a template for template. It is a «language» used to
create anki's card type efficiently. This language is based on Python.

## Leaves
The leaves are generators which does not recursively contains other
generators. 

The  HTML generator is omitted. While it may have no child, it will
still be considered in a section for itself alone.

### Empty
This generator represents the absence of any information. 

None can be used instead of Empty.

### Literal
The generator ```Literal(foo)```represents the string foo. It is
always compiled as this string. 

A standard Python string can be used instead of this generator. Please
don't add either mustaches (i.e. {{foo}}) nor tags (i.e. <foo>) in
literals, use directly the generators for them.

### Field
The generator ```Field(foo)```represents the field {{foo}}. It is
compiled as this field if it is present in the model, otherwise as the
empty string. 

The Python expression ```{"foo"}``` (i.e. a set containing the string
"foo") can be used instead of this generator. This is supposed to
recall the Mustache form {{. However {{"foo"}} would be invalid
Python, since {"foo"} is a set, and not Hashable.

### Function
The generator ```Function(foo)``` contains a function foo. The
compilation of this generator consists into evaluating the function,
transforming the result into a generator, and compiling this
generator. The function is evaluated only once, its result is saved
for further evaluation.

This as many purposes. It allow to delay the evaluation of a generator
which could not be computed immediatly. If the computation is costly,
it ensures that it is done only if the value is required. And
furthermore, that it is done only once (this is called memoization).

### ToAsk
The generator ```ToAsk(set)``` ensure that it is known that the
content of the set consists of questions one may want to ask in
templates. It's required for the method getQuestions, which returns
this set, and for the method questQuestionToAsk(model), which, given a
model, returns a question which has not yet been added in this model.

### Failure
The generator ```Failure(lastStep)``` returns an error if it is still
present in a generator at a step after the lastStep. lastStep being in
element from constants.py

This allows to ensure that an error is raised in case which should not
exists at some step, but have not been properly eliminated at previous
step.

 

## HTML
The generator ```HTML(tag, atom = False, attrs={}, child=None)``` is
interpreted as ```<tag attr_1=value_1
... attr_n=value_n>child</tag>```, with  ```attr_i=value_i``` being
given according to the dictionnary attrs. 

A number of generators are created for standard HTML, and ready to use:
* ```Image(url)```
* ```Table(content, trAttrs= {}, tdAttrs = {}, attrs= {})```, where
  content is a two dimensional array, trAttrs are the attributes for
  tr lines, tdAttrs are attribute for td cells, and attrs are
  attributes for the whole table.
* ```SPAN(child, attrs = {})``` is similar to ```HTML("span", child,
    attrs)```. And similarly for LI, DIV, P, TR, SUB, SUP and TD, and
    the HTML5 HEADER and FOOTER. That is, they are constructors with
    the name of the tag fixed.
* ```OL(elements, liAttrs = {}, attrs = {})``` is an ordered list,
  where each element of elements is a child, enclosed in a ```LI```
  tag with attributes ```liAttrs```. Similarly for ```UL(elements, attrs = {})```.
* ```CLASS(cl, child, attrs = {})``` is used to enclose the child in a
  span whose class is ```cl```.
* Furthermore, ```br``` and ```hr``` are variables representing the
  related tag.

In the case where there is no child, such as the tags IMG, BR, etc...,
use HTMLAtom instead. Note that most standard atomic tag are already
listed above.

## List
The generator ```ListElement([gen_1,...,gen_n])``` represents a list of
generators ```gen_1``` to ```gen_n```. This means that, the result of
the compilation of this generator consists in appending the result of
the concatenation of each of its generators. 

The Python expresion ```[gen_1,...,gen_n]``` can be used insted of the generator.

If a generator is empty, it is removed from the list. If the list is
empty, the generator itself is considered to be empty. Furthermore, if
for each generator, ```gen.getToKeep()``` returns False, then the list
is considered to be empty.


## Conditionals
In this section, we see generators used to print different
informations depending on some conditions. Those condition may be
whether its question or answer side. Whether a field is present or not
in the model. Whether a field is filled or empty. Whether a name is
asked or not.

The basic conditional only assert that: "if condition COND is filled,
print that". It also have a dicotomy version, of the kind "if
condition COND is filled, print this, else, print that".

Finally, we'll introduce more complex conditionals.

### Question or Answer
The generators ```Question(gen)``` and ```Answer(gen)``` compile as
gen on templates on the question (respectively, answer) side. On the
other side, the compile as the empty string.

The generator ```QuestionOrAnswer(gen1,gen2)``` compiles as gen1 on
the question side and gen2 on the answer side.

### Present or Absent
The generators ```Present(field,gen)``` and ```Absent(field, gen)```
compile as gen when the field ```field``` is present in the model,
(respectively, absent from the model). Otherwise, it compiles as the
empty string.

The generator ```PresentOrAbsent(field, gen1,gen2)``` compiles as gen1
if the field ```field``` is present in the model, otherwise as gen2.

### Filled or Empty
The generators ```Filled(field,gen)``` and ```Empty(field, gen)```
show the result of compiling gen if the field ```field``` is filled,
(respectively, empty). That is, they compile as ```{{#field}}result of
compiling gen{{/field}}``` and as ```{{^field}}result of compiling
gen{{/field}}``` respectively. Note that, in anki
both 
```
{{#field}}{{#field}} ... {{/field}}{{/field}}
``` 
and 
```
{{#field}}{{^field}} ... {{/field}}{{/field}}
``` 
are invalid template. You don't have to take care about those
redundancy/contradiction with generators. They take care of always
writting correct template (assuming you never write conditionals {{#
or {{^ yourself.


The generator ```FilledOrEmpty(field, gen1,gen2)``` shows the result
of the compilation of gen1 if the field ```field``` is filled and
otherwise the result of the compilation of gen2. That is, it compiles
as ```{{#field}}result of compiling gen1{{/field}}{{^field}}result of
compiling gen2{{/field}}```.

If the field ```field``` is absent from the model, then it is
considered to be empty.

### Asked or not
The generator ```Asked("name",gen)``` (resp, ```NotAsked("name",gen)```)
compiles as ```gen``` if "name" is marked as "asked" in the template
(respectively, is not marked as asked). 

The generator ```AskedOrNot("name", gen1,gen2)``` is compiled
similarly to ```gen1``` if ```"name"``` is marked as asked in the
template, otherwise as ```gen2```. This is the only kind of
conditionals which allow to make change between two cards using the
same generators.

Furthermore, if ```"name"``` is asked to be ```"hidden"``` in the
template, then the three generators compiles as the empty string.

#### Cascade
You may want to ask many questions simultaneously. In fact, you may
want to give a name to a set of questions. Thus you don't have to
explicitly write every questions in the template.

This can be made using the generator ```Cascade```. 
```
Cascade(field, child, cascade)
```
is a generator similar to child, where - if ```field``` is asked, then
each element of ```cascade``` is also supposed to be asked.

The generator AskedOrNot have an argument```cascade```. Its effect is
similar to the effect described in this generator.

### MultipleRequirement
This is a generator used to add multiple requirements simultaneously.
The generator ```MultipleRequirement(child = gen, requirement1 =
...)``` gen if each requirements are filled. Otherwise as empty
string. The requirements may be isQuestion (true or false). And sets
of fields/name which must satisfy some properties. Those names are
given in arguments requireFilled, requireEmpty, requireInModel,
requireAbsentOfModel, requireAsked, requireNotAsked.

### HideInSomeQuestions
Sometime, there are part of the generator which should always be
shown, except when some particular questions is asked. Not because
it's the answer to the question, but may be it would give too much
clues.

The generator
```Python
HideInSomeQuestions(fields,child)
```
Print child, except on the question side when some field in the
container fields is asked.

## Syntax
In this section, we present more complex generators. They represents
things the author of this add-on often want to do.

### Parenthesis
The generator ```Parenthesis(gen)``` compiles as ```gen```, with
parenthesis around them. Similarly, ```Parenthesis(gen, left = l,
right = r)``` is an abbreviation for the list [l, gen, r], where
both l and r's toKeep values is False.

### Formatted field(s)
We present here a few ways to format and present questions. We first
present a formatting of single question. Then the formatting of list
of questions.

#### Single fields
##### Just the field "foo"
The generator ```QuestionnedField(foo)``` is a basic unit
representing a question. The field is shown on every card, except on
the question side where this field is asked, in this case, the content
of the field is replaced by ```???```. 

If this is asked, the answer side is encapsulated in the two css
classes ```answer``` and ```answer_foo```.

##### Question
This generator is used to obtain a result of the form:
```
{{#foo}}label: {{foo}}<br/>{{/foo}}
```
Here, ```foo``` is the field considered, ```label``` is some context
for foo. 

The pair of label and field is given as a labeled field. Those are
described after this section.

Here, ```<br/>``` is some suffix to separates the content to
everything after. A prefix can also be added. Both prefix and suffix
are shown iff the field ```foo``` is not empty.

If ```foo``` is asked, the question side show 
```
{{#foo}}<span class="question queston_foo">label</span>: ???<br/>{{/foo}}
```
The label is emphased using classes question and question_foo, so that
it is clear that this is the question currently asked. On the answer
side, ```{{foo}}``` is emphasized, as in the «Just the field "foo"» case.

The name of the generator is ```Question```. Its arguments
are:
* ```fieldName```: ```foo``` in this example. This can be either a
  string, or a Field generator. This is the only mandatory argument.
* ```label```: in this example, the label is ```label```. Its default
  value is the fieldName's value.
* ```prefix```, ```infix``` and ```suffix```. In this example, they
  are the empty string, ```": "``` and ```br``` respectively. Those
  are also the default values. Any generator can be used instead.

#### LabeledField
We now explain what is a LabeledField. This is not a generator, but a
class allowing to generate the pair (label,field) easily from
different kind of input. Those are also used in ```TableFields```
below. The different kinds of input are:
* LabeledField(field): in this case, the field is either a string or a
  Field. The label is the nmae of the field.
* LabeledField(labeledField): in this case, the object is a copy of
  the input
* LabeledField(field,label): in this case, the field is either a
  Field object or a string, and is used for the field. The label is a
  string, used for label.

#### FromAndTo
This generator is used for simple questions which, which has a few
properties:
* it begins by the content of a field
* it ends by its answer, the content of another field
* between them, there is the link between both informations, which can
  be emphasized.
* The generator is used only for this property. Hence it is already
assumed that this "answer" is asked.

For example
«Carré in ENGLISH is Square»
or more generally
```
{{French}} in ENGLISH is {{English}}
```
is obtained by 
```
FromAndTo("French"," in ","English"," is ","English")
```
Note that neither "in" nor "is" is emphasized.



#### ListFields
In this section, we explain how to display a consistent set of
informations. Either as a list or as a table.

##### TableFields
This generator will display a table of the form:
```
<table>
{{#field_1}}<tr><td>label_1</td><td>{{field_1}}</td>{{/field_1}}
...
{{#field_n}}<tr><td>label_n</td><td>{{field_n}}</td>{{/field_n}}
</table>
```
All of ```table```, ```tr``` and ```td``` can take attributes, they
are given in keyword arguments (similarly to  HTML generator).
They are called ```attrs```, ```trAttrs``` and ```tdAttrs```
respectively. Furthermore, ```tdLabelAttrs``` and ```tdFieldAttrs```
are used to give attributes to the td's tags of the label and of the
field respectively.

The only mandatory argument is the first one, called ```fields```. This
argument contains a list of table line. Each of those table line is
given either:
* as a string. In this case, the field name is used as label.
* as a dictionnary. This dictionnary may contain:
  * "field" (this is the only mandatory value), which is the name of
    the field shown in this line
  * "label" the label to put in the first column in this line
  * "hideInSomeQuestion": apply HideInSomeQuestion to this line, with
    the value contained in this entry.
* as a list ```relatedList```. In which case, it is assumed that for
  each field ```f``` of ```relatedList```, the list ```fields```
  contains an entry ```{"field":f,
  hideInSomeQuestion:relatedList-f}```.
  
Each line is similar to a Question generator, with ```<tr><td>``` as
prefix, ```</td><td>``` as infix and ```</td></tr>``` as suffix.
  
This generator as an optional argument ```name```. When ```name``` is
asked, it is similarly to asking simultaneously every single fields.
##### NumberedFields
Sometime, you have a list of successive fields with name suffixed by
numbers, such as ```foo```, ```foo2```, ..., ```foon```. For example
if you want to list different names of a same concept or different
lines of a lyrics. In this case, there is no reason to repeat the
label. This generator generates codes of the kind:
```
label:
<ol>
{{#foo}}<li>{{foo}}{{/foo}}
{{#foo2}}<li>{{foo2}}{{/foo2}}
...
{{#foon}}<li>{{foon}}{{/foon}}
</ol>
```

If fooi is asked (with i a number), then the label is emphasized on
the question side as in Question generator. And {{fooi}} is emphasized
on the answer side with css classes answer and answer_foo. (note the
absence of ```i``` after the label.)

Both ```ol``` and ```li``` attributes can be set, similarly to the
HTML generator, using the parametrs ```attrs``` and ```liAttrs```.

There are two mandatory arguments:
* ```fieldPrefix```, in this example ```foo```. The prefix a the fields.
* ```greater```, the number of field to consider. Note that if you
  enter a number which is greater than the actual number of fields, it
  create no problem. Indeed, ```{{#foo}}bar{{/foo}}``` does not appear
  in the template if ```foo``` is not a field of the model.
The optional arguments are:
* ```label```, as in the example
* ```name```, similarly to the case of tableField
* ```unordered```, if set to True, then <ul> is used instead of <ol>.

##### PotentiallyNumberedFields
This generator is similar to the precedent one when ```foo2``` is
filled. Otherwise, it is similar to ```Question("foo")```, that is, it
only ask a single question and does not use the list.

Note that you should avoid using this in the case where some
fields ```fooi``` may be used while ```foo2``` is empty. I.e. we
assume that you fill the foo in their numeric order. 

The keywords are similar to the one of NumberedFields and of Question.

##### ListFields
The two last examples are created from a more general kind of
generators, called ListFields.

ListFields takes the following parameters:
* fields: a list of field or of labeled fields, depending on what is required.
* globalSep: a function taking the list of fields seen and creating a
  generator which separate each successive pair of fields. By default,
  it returns None. 
* globalFun: a function applied to the list of generator returned by
  localfun. It should return a generator. By default it is the
  identity function.
* name: this parameter is optional. If it is given, then, when this
  name is asked, the union of the set returned by localFun's calls are
  assumed to be asked.
* localFun: a function, applied to each element of fields which return
  either a generator or a dictionnary. If it is a generator, then this
  generator is added to the list directly. Otherwire, the dictionnary
  is as follows:
  * child: the generator to display
  * questions: a set such that if ```name``` is asked, then those
    elements are also supposed to be asked.
  * filledFields: request that at least one of the field from this
    list is filled to display the line
  * hideInSomeQuestion: apply HideInSomeQuestion with those fields to
  this line.
