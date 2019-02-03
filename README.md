# Multi-column edit window
This is a BETA version. If people want to help debugging and
improving. It may change a lot and while I use this add-on a lot, I
can't promise it to be fit for everyone (yet?)

![An example of card generated using my add-on](https://raw.githubusercontent.com/Arthur-Milchior/anki-template-card-type/master/examples/images/exampleQuestion.png "First name question")

## Links
To see a few examples of note type created using this add-on, go read:
[examples/README.md]
You should probably download this add-on and try those examples to
understand how everything works.

Please, refer to
[generator's documentation](generators/DOCUMENTATION.md)
to learn how to use this add-on. I'll just give a few examples here.


## Rationale
One of anki big limitation, as far as I'm concerned, is that templates
can't have code in them. In my case, in a fixed note type, most of the
templates are similar. Which means that I have to do a lot of
copy-paste. And if I want to edit a part of the template, I have to
edit once in each template.

If you know a little bit of Python and of HTML, you can use this
add-on to ensure that your template is generated by some arbitrary
Python code. The Python expression is given as an attribute of an HTML
tag of the template. This ensure that the python code can remain in
the template while never being shown in the card's content. This also
means that you can recompile a template already compiled - which is
pretty useful for debugging.

In order to easily write templates, this add-on also gives you a
library/domain specicif language of basic component, called
generators. Those generators allow you to change the template,
depending on a lot of conditions. 

## Links, licence and credits

Key         |Value
------------|-------------------------------------------------------------------
Copyright   | Mostly https://github.com/hssm/anki-addons
Maintener   | Arthur Milchior <arthur@milchior.fr>
Based on    | Anki code by Damien Elmes <anki@ichi2.net>
License     | GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
Source in   | https://github.com/Arthur-Milchior/anki-Multi-column-edit-window
Addon number| [2064123047](https://ankiweb.net/shared/info/2064123047)
