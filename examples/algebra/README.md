# Algebra

Most of this example is pretty standard definition. There is a single
thing I'll comment here. A thing which is not really important, but it
was a good exercice for me to try to do it. This thing is: Trying to
figure out the name of the algebraic structure, given the functions it
has.

For example:
* A structure which has got a 0, an addition and a substraction symbol
  is a group.
* If it as no substraction symbol, its a monoid.
* If furthermore, it has a multiplication, its a Rng.
* If it also has a 1, its a ring.
And so on.

In [algebra.py](algebra.py) you can take a look at the variable
algebra_name and try to understand how the name of the structure is guessed.
