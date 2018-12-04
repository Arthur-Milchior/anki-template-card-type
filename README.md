# Efficient Templates
## Rationale


## Usage

## Warning

## Configuration
Currently, there is a single configuration, called:
"instructions". This is a list of instructions.

Each instruction is either a string, which is interpreted as standard
python code, in the environment of the add-on. 

Or a pair ("name","expression"), in which case a name is added to the
environment, whose value is "expression" evaluated in the current
add'on environment. An expression may use names defined above, and any
generator.
## Advice

Using add-on [Newline in strings in add-ons
configurations](https://ankiweb.net/shared/info/112201952) you can
have new lines in you configuration file. This will considerably help
you writing your code.

Note that strings, in python, can be defined using single quote
('). Using single quote instead of double quote means that you don't
have to escape your quote in the json.

## TODO 
Add more generators /syntactic sugar. 

Allow more complex question generation. In particular, generation
created on multiple fields.

{{FrontSide}}: 

## Links, licence and credits

Key         |Value
------------|-------------------------------------------------------------------
Copyright   | Arthur Milchior <arthur@milchior.fr>
Based on    | Anki code by Damien Elmes <anki@ichi2.net>
License     | GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
Source in   | https://github.com/Arthur-Milchior/anki-
Addon number| [NNNNNNNNNNNN](https://ankiweb.net/shared/info/NNNNNNNNNNNN)
