# Name and faces
This is a simplified versions of a note type which changed my life. It
allows me to recall people's name and the reason why I should recall
them. Such a reason may be «Boss of the company», or «Spoke with him
at conference XXX».

Here is the example of the first card I obtain:
* ![A card asking for the first name of some guy who's face is shown](https://raw.githubusercontent.com/Arthur-Milchior/anki-template-card-type/master/examples/images/exampleQuestion.png "First name question")
And here are the templates of the five card types:
* ![Template of the card asking for first name](https://raw.githubusercontent.com/Arthur-Milchior/anki-template-card-type/master/examples/images/templateFirst.png "First name template")
* ![Template of the card asking for last name](https://raw.githubusercontent.com/Arthur-Milchior/anki-template-card-type/master/examples/images/templateLast.png "Last name template")
* ![Template of the card asking for full name](https://raw.githubusercontent.com/Arthur-Milchior/anki-template-card-type/master/examples/images/templateName.png "Full name template")
* ![Template of the card asking why do you know this person](https://raw.githubusercontent.com/Arthur-Milchior/anki-template-card-type/master/examples/images/templateKnown.png "Known for template")
* ![Template of the card asking for which is the person you know for this reason](https://raw.githubusercontent.com/Arthur-Milchior/anki-template-card-type/master/examples/images/templateKnownName.png "Full name give known template")


This has four fields:
* First name
* Last name
* Known for
* Picture

It has four cards:
* First name: Given the picture and Known for, ask the first name
* Last name: Given the picture and Known for, ask the last name
* Picture -> Known for: Given the picture, ask why you know this person
* Picture -> Full name: Given the picture, ask for the full name
* Know for -> Full name: Given the reason you know this person, ask
  the full name

The last card is usefull if the reason you know this person is «it's
the boss of the company». In case where the reason is «Met him at
XXX's birthday party» I'll just suspend this card.

I can't just use cloze-deletion for those cards, because some time I
want to ask twice the same information. Either first name, last name,
or both.

If I have to do it in standard anki, I'll have to do a lot of copy and
paste. Which I really want to avoid. Instead, I'll write the following
python code in `user_files/imports.py` (or in a file imported by
imports.py)

``` Python
from ...generators.imports import *
firstName = QuestionnedField("First name")
lastName = QuestionnedField("Last name")
fullName = Cascade("Full name",[firstName,lastName,br],["First name","Last name"])
knownFor = QuestionnedField("Known for",suffix=br)
face=[fullName,knownFor,Field("Picture")]
```
Then, the template of my cards, in the same order as above, are going
to be:
* `<span template="eval" generator="face" askedmandatory="First name"/>`
* `<span template="eval" generator="face" askedmandatory="Last name"/>`
* `<span template="eval" generator="face" askedmandatory="Known for" hide="Full name"/>`
* `<span template="eval" generator="face" asked="Full name" hide="Known for"/>`
* `<span template="eval" generator="face" asked="Full name" hide="Picture"/>`
## Explanation
We now explain this example
### Python part
First, `from ..generators.imports import *`
is used to import in this file everything required to create templates.

```Python
firstName = QuestionnedField("First name")
```
means that you create an object, which by default shows the first name, except if "First name" is asked in the template. Instead, it'll show ???.


In the fullName line, `[firstName,lastName,br]` is an object,
representing the concatenation of the first name (as a question), the
last name, and a newline symbol.

```Python
fullName = Cascade("Full name",[firstName,lastName,br],["First name","Last name"])
```
means that `fullName` is a variable represing the following
informations:
* when `Full name` is asked, you must ask both `First name`
  and `Last name` (that's the point of the first and third
  arguments)
* in all cases, you must show the content of
  ```Python
  [firstName,lastName,br]
  ```
```Python
knownFor = DecoratedField("Known for",suffix=br)
```
is similar to QuestionnedField in the sens that it states that "Known
for" is a field whose content may be asked. But it also ensure that
this field is prefixed by a label which explain what the field's
contains. By default, the label is the field name, thus "Known
for". Furthermore, it adds a prefix after the field, the HTML tag
br. Finally, all of this is printed only if the field "Known for" has
content. (This is why we put the "br" as a parameter of the
DecoratedField. It ensures that this newline is not printed when
"Known for" is empty.)

### HTML part
The entire templates are contained in an HTML tag. This ensure that no
information is ever printed on the card's itself. It still allows us
to keep all information related to this process in the card's
template.

We use `template="eval"` to state that this template
will have a generator field - which is an arbitrary python expression
which must be evaluated as a generator (see
[https://github.com/Arthur-Milchior/anki-template-card-type/tree/master/generators/DOCUMENTATION.md]
to learn more about generators).

We use `generator="face"` to state that we'll use the
variable `face` defined in the python file. The value of
thi variable will state how to compile the template.

We use `askedmandatory="First name"` as an abbreviation for
```python
asked="First name" mandatory="First name"
```
Here, `mandatory="First Name"` means that this template should be
printed only when the field "First name" has some content. In anki's
template, it means that the entire template will be contained between
the mustaches `{{#First name}}` and `{{/First name}}`.

The parameter `asked="First name"` states that "First name" should
be considered to be asked. `QuestionnedField("First name")` will
know that it means:
* in the question side, replace the field content by ???
* in the answer side, apply the CSS classes "Answer" and "First name"
  on the field. (In this example, we won't consider CSS)

Finally, `hide="Known for"` means: in this template, don't show
the content of the part named "Known for". Once again, it is
`
QuestionnedField("Known for",suffix=br)
`
which interprets it and understands that, in this template, its
content should not be printed.

## Back side/answer

The template on the answer side will always be `<span template='Front side'/>`. Note that this add-on add, in the edit menu «frontSide to each», which add this template to each back side of the templates of the selected's note. This ensure
