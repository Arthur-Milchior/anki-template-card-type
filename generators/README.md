# Generator 
A generator is a template for template. It is a «language» used to
create anki's card type efficiently. This language is based on Python.

## States
An object of class Generator may have many states. 
* Normalized: this means that the object is composed only of core
  elements. Those elements will be described below. 
* toKeep: if this object appear, alone, in a list, should the list be
  kept ? For example, an HTML list may be encoded as a list with
  "<ul>", the elements and "</ul>". If there are no elements, the <ul>
  should not be kept.
* unRedundated: whethere the generator contains redundant (or
  contradictory) informations. For example
  {{#foo}}{{#foo}}bar{{/foo}}plop{{/foo}} is redundant and
  {{#foo}}{{^foo}}bar{{/foo}}plop{{/foo}} is contradictory. The
  unredundated version would be {{#foo}}barplop{{/foo}} and
  {{#foo}}plop{{/foo}} respectively. Only normalized element may be
  unredundated, it is not possible to test redundancy in non-core elements.
* empty: whether this generator may actually show any content in some
  case. Empty, an empty list, etc... are empty. Those generator should
  be discarded when they are used to create other generators.

## Process
The intended process to transform the input generator into anki's
template is as follows:
* normalize the generator. This translate syntactic sugar into the
  core elements. This is done by self.getNormalForm().
* remove redundancies and contradictions. This allow to obtain a
  smaller generator, and win time in latter process. This is done
  using self.getUnRedundate()
* take the model into account. That is, remove everything which is
  related to fields which does not exists in this particular
  model. This is similar to removing redundancies. Those are two
  separate steps because redundancies a generator may be used in
  multiple model. Thus, the part of the job which is not specific to a
  model may be done a single time. This is done using
  self.restrictToModel(model,fields = None).
* Actually outputting the template, taking into account whether it is
  question or answer side, what is asked, and what should be
  hidden. This can be done using self.template(asked,hide,question)
  
## Generators
### Core

Generators's core is based on a few basic construct. They are the only
generator on which the above mentionned process can be applied. They
are composed of:

* Empty : which is a generator representing the absence of any information. None can be used instead of Empty.
* Literal(foo) : this represents the string foo. A string can be used instead of this generator.
Field(foo) : this represents a field of a note type. Field(foo) is almost equivalent to the literal "{{foo}}", unless foo is not a field of the note's type or unless this generator appear in {{^foo}}...{{/foo}}.
* ListElement(foo) : A list of generators, printed one after the other. Empty generators are rempoved from this list. Can be represented as a python list of generators.
* Requirement(foo, ...) : this represents the fact that foo (a generator) should be seen only if some conditions are satisfied. Some fields may be required to be/not to be in the note type's list of field. Some fields may be required to have/not to have content. And the order to delete some generators below may also be given. There is no syntactic sugar for this.
* Branch(name,...) : The printed content of this generator depends on whether it's the question side or answer side, and on whether name belong to the set of asked elements. It can also be deleted if a Requirement above it requests it.
* HTML(tag, child, params={}): either "<tag param_1=value_1
  ... param_n=value_n>child</tag>", with param_i=value_i being given
  according to the dictionnary params. Or if child is None: then "<tag param_1=value_1
  ... param_n=value_n/>". This is not exactly similar to Literal, because it generate a
  beautiful soup tag. 

### None core generators

Those are syntactic sugar, which may be used for creating templates
more easily. There are currently three kinds of syntactic sugar.

#### HTML
it is not clear to me whether HTML will ever be usefull, as the HTML
cases can be directly created as literal. In doubt, I created it.

Some praticular classes and values are created for the sake of
simplicity, br, hr, Image(url), SPAN(child), DIV(child), P(child) and
finally Table(content, trParams, tdParams), with contents being an
array (list of list) with the content of the table.
  
Html's default's toKeep's holds if either there is no child, or the
child should not be keep. The same rules applies in order to know
whether it's empty.
#### Conditionals
Conditionals are generator to test some cases which may occur
often. Those conditionals should be easier to use than Requirement
and Branch.

* AtLeastOne(child,fields): print the child if at least one of the
  fields have some content. Note that the child is printed as many
  time as there are fields, so this may lead to a long text.
* FilledOrEmpty(field,filledCase, emptyCase): show filledCase if field
  has some content, emptyCase otherwise. 
* PresentOrAbsent(field, presentCase, absentCase): show presentCase if
  field is present in the note type, absentCase otherwise. Thus, only
  one of them is actually printed in a template.
* Fielled(field,child), Empty(field,child), Present(field,child),
  Absent(field,child): show child only if field satisfy the condition
* QuestionOrAnswer(field,questionSide, answerSide)

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
