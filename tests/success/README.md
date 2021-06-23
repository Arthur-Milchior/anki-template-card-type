This directory contains test. Those test have already been
successfull, and hopefully should remain so.

Functions used for the test are in ../functions. While it would make
sens to have them in those files, importing the function would also
trigger the test, which should be avoided.

# Config:
ensure that add-ons's config is read

# generators.py

Test equality between generators. Also test whether they should be kept, and whether they are truthy/empty.

# generatorsToHtml.py
Test that some generator (from ../data/generators), once compiled and applied to an empty text, generate some precise HTML (from ../data/htmlFromGenerator)

# html.py
Test that html is correctly compiled.

# models

Compile a full model
