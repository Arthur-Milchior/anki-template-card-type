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
This  generator represents the absence of any information. 

None can be used instead of Empty.

### Literal
The generator ```Literal(foo)```represents the string foo. It is
always compiled as this string. 

A standard Python string can be used instead of this generator.

### Field
The generator ```Field(foo)```represents the field {{foo}}. It is
compiled as this field if it is present in the model, otherwise as the
empty string. 

The Python expression ```{{"foo"}}``` (i.e. a set containing a set
containing the string "foo") can be used instead of this generator.

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

## HTML
The generator ```HTML(tag, atom = False, attrs={}, child=None)``` is
interpreted as ```<tag attr_1=value_1
... attr_n=value_n>child</tag>```, with  ```attr_i=value_i``` being
given according to the dictionnary attrs. 

In the case where there is no child, such as the tags IMG, BR, etc...,
atom should be set to True, to state that the tag should be kept even
when its content is empty.

A number of standard HTML tags are already created, and ready to use:
* br and hr
* Image(url)
* Table(content, trAttrs= {}, tdAttrs = {}, attrs= {}), where content is a two
  dimensional array, trAttrs are the attributes for tr lines, tdAttrs
  are attribute for td cells, and attrs are attributes for the whole
  table.
* SPAN(child, attrs = {}) is similar to HTML("span", child,
  attrs). And similarly for LI, DIV, P, TR and TD. That is, they are
  constructors with the name of the tag fixed.
* OL(elements, liAttrs = {}, attrs = {}) is an ordered list, where
  each element of elements is a child, enclosed in a LI tag with
  attributes liAttrs. Similarly
  for UL(elements, attrs = {}).
  
## List
The generator ```ListElement([gen_1,...,gen_n])``` represents a list of
generators ```gen_1``` to ```gen_n```. This means that, the result of
the compilation of this generator consists in appending the result of
the concatenation of each of its generators. 

The Python expresion ```[gen_1,...,gen_n]``` can be used insted of the generator.

If a generator is empty, it is removed from the list. If the list is
empty, the generator itself is considered to be empty. Furthermore, if
for each generator, gen.getToKeep() returns False, then the list is
considered to be empty.


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

AskedOrNot("name", gen1,gen2) is compiled similarly to gen1 if "name"
is marked as asked in the template, otherwise as gen2. This is the
only kind of conditionals which allow to make change between two cards
using the same generators.

Furthermore, if "name" is asked to be "hidden" in the template, then
the three generators compiles as the empty string.

### MultipleRequirement
This is a generator used to add multiple requirements simultaneously.


## Syntax
This is a set generators used to allow to had syntax.

The generator ```Parenthesis(gen)``` compiles as ```gen```, with
parenthesis around them. Similarly, ```Parenthesis(gen, left = l,
right = r)``` is an abbreviation for the list [l, gen, r].


########################################


#### Questions
Hopefully, this should correspond to most standard way of asking
questions. Not all kind of questions are already taken into
account. The author hope to add more syntactic sugar later, once this
version already works. Because honestly, it's not a minimal product
anymore.

##### Question(fieldName)
The type to use in order to nicely display the field foo. It's main
purpose is to generate question, but that's not actually mandatory.

For example ```Question(fieldName, suffix="<br/>")``` would display
«{{#fieldName}}fieldName: {{fieldName}}<br/>{{/fieldName}}», and thus
fieldName will be displayed if they are present, and nothing will be
displayed otherwise. If "fieldName" is not a field of the model,
nothing would be displayed.


If "fieldName" is asked, then «__fieldName__ : ???<br/>» will be displayed
instead on the question side. With "fieldName" emphasized. And «fieldName:
__{{fieldName}}__» on the answer side. (Emphasize is still TODO)

This has many optional parameters:
* symbol: generator, emphasized during question, to display instead of
  the name of the field.
* prefix: generator not emphasized to display before the name of the
  field/symbol
* suffix: generator not emphasized, to display after the content of the
  field.
* question mark: generator to display instead of ???, when field is
  asked, on question side. Still keeping prefix, symbol, separator, suffix.
* separator: generator, not emphasized, to display between field's
  name/symbol, and the field content/ ???

The following parameters replace prefix, symbol, separator, suffix,
etc.. in some cases.
* absent: generator to display if the field is not in the model. 
* empty:  generator to display if the field is empty.
* question: generator to display on question side if this field is asked.
* answer: generator to display on answer side if this field is asked.

#### ListFields(fields)
Fields is a list. Each element is interpreted as a question. Either an
element is already a question, in which case it is used as it. Or it
is a pair, interpreted as (label, field name). Or it is a string, in which
it is interpreted as a field name.

The arguments are:
* globalPrefix/globalSuffix: if at least one question is present, this
  will be shown before/after them.
* globalSeparator: shown between each pair of fields which are
  present. (Avoid, as it will generate a texte whose size is the
  product of the separator, and the square of the number of
  question. Use local prefix/suffix instead)

#### NumberedFields(field, number)
This is a special case of ListFields, where each field name is of the
form field1, field2, ... fieldNumber. (Numbering does NOT start at 0
because hopefully, this add-on can be used by non computer-scientist).
