This directory contains a list of data used to test the add-on.


# generators.py
Generators contains generators. They are not processed.

# jsons.py
contains a json string, and directly process it to create testObjects.
The processing should be similar to the one of /config.py, but processing is done by loads and not by add-on template

# model.py

Contains a model. With fields Question, Back, Definition, Definition2,... to Definition6 and a few templates.

# htmlFromGenerator

Some html. Obtained by applying gen.toTag() from an empty html tag.


# templatesToCompile.py
html contains some html strings. As it should be outputted by beautifulSoup's prettify. Either an input string to compile, or the expected result from the compilation
