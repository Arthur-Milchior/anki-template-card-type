# Generator
## States
An object of class Generator is parametrized by three indications.
* toKeep: if this object appear, alone, in a list, should the list be
  kept ? For example, an HTML list may state that it should not be
  kept if it has no content.
* empty: whether this generator may actually show any content in some
  case. Empty, an empty list, etc... are empty. Those generator should
  be discarded when they are used to create other generators. In
  particular, bool(gen), for gen a generator, returns the value ```not
  gen.isEmpty()```.
* state: Each generator corresponds to some step of the compilation
  process. Each step is described below. Each step must be computed in
  a precise order. Thus trying to do a step of the processing if the
  previous step is not already done will fail. It is considered that
  an empty generator has already done every state of the
  processing. Each state is a constants.Step instance. They are all
  defined in the end of constants.py file.


Furthermore, a generator

* Normalized: this means that the object is composed only of core
  elements. Those elements are listed below and described in README.md.
* unRedundated: whethere the generator contains redundant (or
  contradictory) informations. For example
  {{#foo}}{{#foo}}bar{{/foo}}plop{{/foo}} is redundant and
  {{#foo}}{{^foo}}bar{{/foo}}plop{{/foo}} is contradictory. The
  unredundated version would be {{#foo}}barplop{{/foo}} and
  {{#foo}}plop{{/foo}} respectively. Only normal element may be
  unredundated, it is not possible to test redundancy in non-core elements.

## Process
The intended process to transform the input generator into anki's
template follow a number of processing step. Each step corresponds to
a value of constants.py. Note that only getNormalForm(self) must be
defined on each generator. Every other method mentionned below must be
defined only on core generators.

* BASIC: An arbitrary generator is in basic step by default.
* NORMAL: A normal generator is a generator composed only of core
  generators. Transformation from BASIC to NORMAL is done using ```getNormalForm(self)```.
* WITHOUT_REDUNDANCY: {{#foo}}{{#foo}}bar{{/foo}}plop{{/foo}} is redundant and
  {{#foo}}{{^foo}}bar{{/foo}}plop{{/foo}} is contradictory. The
  unredundated version would be {{#foo}}barplop{{/foo}} and
  {{#foo}}plop{{/foo}} respectively. ```getWithoutRedundance(self)```
  returns a copy of gen where those redundancy and contradictions are
  removed. This step use the methods ```ensureFieldFilled(self,field)``` and```ensureFieldEmpty(self,field)``` which returns a copy of self where
  field is assumed to be filled or empty respectively.
* QUESTION_ANSWER: This step restrict a generator in order to obtain
  only the question side or the answer side. This is obtained using
  the method ```questionOrAnswer(self, isQuestion)```, where isQuestion is
  True iff we want to obtain the question side. This method use the
  method ```assumeQuestion(self)``` and ```assumeAnswer(self)```.
* MODEL_APPLIED: this step takes the model into account. That is, it
  remove everything which is related to fields which does not exists
  in this particular model. This is similar to removing
  redundancies. Those are two separate steps because redundancies a
  generator may be used in multiple model. Thus, the part of the job
  which is not specific to a model may be done a single time. This is
  done using ```restrictToModel(self,fields)```.
* TEMPLATE_APPLIED: this step adapts the generator in order to assume
  that some question are asked, some other informations are hidden,
  according to the attributes of the tag from which this generator is
  called. It also ensure that each required fields is filled. This is
  done using the method ```template(self,asked, hide, mandatory,
  modelName)```
* TAG: There is no generator in this step. This is a step mostly used
  for debugging. It means that the template has been used to generate
  some html content. This contant can be returned using the model ```applyTag(self,soup,model)```, where soup is a BeautifulSoup object used to
  create new tag. The parameter ```model``` is the name of the model
  currently used. This is used to know in which model questions were
  already asked.
* EMPTY: This is the last step. Most generators never reach it. In
  this step, it has been found that the generator has actually no
  content, and thus can be discarded.

### Other methods
#### getQuestions

This return a set of questions which may be asked in this
generator. This is currently not used.

#### getQuestionToAsk(nb)
We return a question of this generator which has not yet been
asked in this model.

## Current cores
Here is the current list of Core generators. They are described in README.md
* HTML
* HTMLAtom
* ListElement
* Absent
* Present
* Empty
* Filled
* Question
* Answer
* Asked
* NotAsked
* Empty
* Literal
* Field
## New generator
In this section, we explain how to create new generators.

You can create one by inheriting a generator, in which case you have
nothing special to do. (Note that Gen is not a generator). Otherwise,
you must decide whether you want to implement a core generator or not.

### Not core generator
In order to create a generator which is not a core generator, you:
* probably want to implement ```__init__```.
* must implement _getNormalForm() which return a core generator in
  normal form.

### New core
In order to create a new Core generator, you must:
* create a class inheriting from Gen (or from one of its
descendant).
* the class must be preceeded by the class by the decorator
  ``@thisClassIsClonable```,
* the class must implement ```__hash__```.
* the class must implement ```clone(self, elements)```, which, returns
a copy, similar to self, where the children are elements.
* the class must implement ```_getChildren``` returning the set of
children (not necessirily gen).
* If some step/method foo of the computation mentionned in section
  Process does not simply consist into applying the same method
  recursively to all children, and cloning itself with those new
  children, then the method ```_foo``` must be reimplemented. It does
  not have to return a generator. A generator will be computed from it
  using self._ensureGen() if the returned value is not a geneartor.

Furthermore, for debugging purposes, the classes must implement the
following method:
* the class must implement ```_repr```. Print the representation of
  this Gen, without indenting it. Call child.repr to call
  children. You can use genRepr(child, label = None) to print the
  parameter, prefixed by «label =», if you want to print some
  parameters.
* the method ```_outerEq``` is similar to __eq__ but does not consider
  the children. For example, it should return true for two lists of
  the same length, two html tags with the same tag and attributes.
* __eq__ should be the conjunction of ```_outerEq``` and
  ```_innerEq```. Hence, the method ```_innerEq``` should test the
  equality of everything, except the surface. It may be assume that it
  is called only if ```_outerEq``` returns True.
* the method _firstDifference(self,other) must return a pair of
  generators. Those are in the same position in the tree self/other,
  but which are distinct on surface. I.e. outerEq return false on
  them. It is assumed that self and other are distinct. Return None
  ifself and other are equal.

### Transforming a value of some type into a generator
The code ```"foo"``` is interpreted as ```Literal("foo")```. Similarly, , the code ```("foo",gen)``` is
interpreted as ```Filled(foo,gen)```. More generally, some types may
be interpreted as a generator. You can use  ```generators.addTypeToGenerator(typ, fun)```
to ensure that function ```fun``` is applied to element of type ```typ```
in order to transform them into generators.
