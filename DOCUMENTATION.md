# Programmable Templates's main documentation
## Usage
This add-on must be used in three successive steps. You must create
the generators you'll use in your templates. Then you must edit your
template to state which generator to use in them, and what question of
this generator is asked. Finally, you must compile the note
type. Those three steps are more detailled below.

Potentially, as a last step, you should check the result, and correct
either the generators or the template if you see a problem. As any
person who tried to make complex template should now, it's hard to
have it all right at the first try.

You can find a few examples in 
[https://github.com/Arthur-Milchior/anki-template-card-type/blob/master/generators/README.md]

### Generators
A generator is an abstract piece of template. Each generator can be
compiled into an actual template that anki can use. The result of the
computation depends:
* on the set of fields present in the model, 
* on whether the generator is used in the question side or in the
  answer side. 
* on some names which are asked or hidden.

Here are a few examples of generators:
* The simplest generators represents a string literal.  For example
  the string ```"foo"```, is a generator. In the template, it is
  always compiled as the string ```foo``` in the template.
* A list of generator ```[gen1, gen2, gen3]``` is also a
  generator. When it is compiled, it becomes the concatenation of the
  result of the compilations of gen1, gen2 and gen3.
* A more complex generator would be ```QuestionOrAnswer(gen1,
  gen2)```, which compiles as gen1 on the question side of the card,
  and as gen2 on the answer side of the card. (Similarly, the
  generator ```Question(gen)```, compiles similarly to the generator
  gen on the question side, and compiles as an empty string on the
  answer side.)
* ```FilledOrEmpty('foo', gen1, gen2)``` is a more complex
  generator. It shows gen1 if the field foo is filled, and it shows
  gen2 if the field 'foo' is empty. Thus, it compiles as
  ```
  {{#foo}}gen1{{/foo}}{{^foo}}gen2{{/foo}}
  ```
  However, if this
  generator inside some ```{{#foo}}...{{/foo}}```, since it is already
  known that the field 'foo' is filled, this generator compiles as
  gen1 only. Reciprocally, if the field foo is not present in the
  model, then it can't be filled, thus this generator compiles as gen2
  only.
  
#### Where to write the generators

You may put your generators in two distinct places. Json's
add-on configuration file or the folder ```user_files```.

##### User files
The file ```user_files/imports.py``` is executed while loading the
add-on. Its entire content is imported while compiling
templates. Thus, you can use it for debugging purpose as
standard-python. And you can put any variables that you want in it,
and then uses those variables in your templates.

When you download this add-on, this folder will already have some
content. This content is the actual content used by this add-on
writer. This may serve as code example.

The main problem is that those files are reads exactly once, when anki
is launched. This means that you should use another method to edit
quickly your code and change it.

##### Addon's configuration
You can uses the add-ons manager to edit a configuration file in
JSON. Currently, there is a single field in the json configuration
field. It is called: "instructions". This is a list of instructions.

Each instruction is either a string, which is interpreted as standard
python code, in the environment of the add-on. 

Or a pair ("name","expression"), in which case a name is added to the
environment, whose value is "expression" evaluated in the current
add'on environment. An expression may use names defined above, and any
generator.

If you change the configuration file using the add-on manager, each
execution are executed again. In particular, it means that if you
changed the value of a variable, this new value will be used in the
compilation process.

###### Advice for JSON
Using add-on [Newline in strings in add-ons
configurations](https://ankiweb.net/shared/info/112201952) you can
have new lines in you configuration file. This will considerably help
you writing your code. However, writing code in user_files may be easier.

Note that strings, in python, can be defined using single quote
('). Using single quote instead of double quote means that you don't
have to escape your quote in the json.
#### Generator's documentation

The current list of generators can be found at
[https://github.com/Arthur-Milchior/anki-template-card-type/blob/master/generators/README.md]. This
document also explains how to create more generators. Don't hesitate
to send me your generators so that I can include them in this add-on.

### Template
The templates must satisfy a few basic rules:
* Compiled or not, the template must be valid HTML.
* The code written for this add-on must never be shown in anki's
  card. Thus it is written in parameters of HTML tag.
* Compiling a template already compiled does not change the
  template(Unless you changed some variables' value, of course).
* The compilation can be undone, in the sens that some code can remove
  the result of the compilation (i.e. the content of a tag), and keep
  only the code (i.e. the tag and its attributes).
  
An HTML tag is used by this add-on if it has a "template"
parameter. The action done on this tag depends on the value of this
paramer. The current possible values are listed below.

We now list the templates present by default. If you want to create a
new template, have a look at
[https://github.com/Arthur-Milchior/anki-template-card-type/tree/master/templates/INTERNALS.md].
Don't hesitate to send me your generators so that I can include them
in this add-on.

#### Generator
The most basic template's value is a generator. This generator is
compiled and the result of the compilation is put between the tags.
```
    <span template="eval" generator="foo" asked="bar"/>
```
This compile as 
```
<span template="eval" generator="foo" asked="bar">
  Result of the compilation of foo, where the name bar is asked.
</span>
```

For example, if ```foo``` is the generator ```DecoratedField("bar")```,
then this templates compiles, on the question side, as:
```
<span template="eval" generator="foo" asked="bar">
  {{#bar}}<span class="Question bar">bar</span>: ???{{/bar}}
</span>
```
and on the answer side as:
```
<span template="eval" generator="foo" asked="bar">
  {{#bar}}bar: <span class="Answer bar">{{bar}}</span>{{/bar}}
</span>
```
Finally, in the case where ```bar``` is not asked, then this template
is printed as:
```
<span template="eval" generator="foo">
  {{#bar}}bar: <span class="bar">{{bar}}</span>{{/bar}}
</span>
```


Note that the CSS classes ```Question``` and ```Answer``` are applied
to the question and the answer respectively. And the class ```bar```
is applied to emphasize the value ```bar```. Unless this value is
absent, in which case it is applied to its label.

#### Front side
Anki has a special field called {{FrontSide}}, which show the content
of the question side of the card. Its use is really limited, because
every single thing in the question side appears in the answer
side. Sometime, you want to makes a slight change in the question
side, for example emphasizing an element, replacing [...] by its
value. In those case, in anki, you have to copy-paste front side into
the back side and do the edition manually.

Instead, this add-on allow you to use ```<span template='Front
side'>```, to obtain the question side, where each generators are
recompiled using the knowledge that this is the answer side.


In the last example ```<span template='Front side'/>``` would compile as:
```
<span template='Front side'>
  <span template='eval' generator='foo' asked='bar'>
    {{#bar}}bar: <span class="Answer bar">{{bar}}</span>{{/bar}}
  </span>
</span>
```

#### Instruction
You may want to execute an arbitrary Python expression ```foo``` during the
compilation. This can be done using ```<span template='instructions'
instr="foo"/>```. Note that this must remains valid html, thus <, > and
' must be replaced in foo by ```&lt;```, ```&gt;``` and ```&quot;```.

#### String
You may want to have a string ```foo``` which is shown only when the
template is compiled, and absent when the template is
«uncompiled». This can be done using ```<span template='string'
string="foo"/>```.

Having some text present only during uncompilation is not currently
possible, and I don't intend to ever do it. Because uncompiling means
removing, and never adding.

#### Fixing content
You may want to ensure that the content of some part of the text is
not changed. This can be done using ```<span
template='fix'>foo<span>```. Not that if foo contains template, they
may be compiled (TODO: remove the last statement.)
Note that if this span is contained in another template, it may still
be removed. This span does not affect tags containing it.

### Compiling
In the browser, select at least one card. Then on Edit>Template. It
will compile the templates of the selected card(s)'s note(s)'s type.

## Warning
This is still relatively experimental. It works on the author's
computer. But it is possible that anything breaks on another
computer. So think about backuping your note type before using this
add-on.

