# Piano scales
This note type is used for one very precise thing: practicing piano
scales.


I have images which show each scales with piano fingering for:
* right hand, left hand, and both hands (let ```hand``` be the hand)
* A number ```noOctave``` of  octaves (currently 1 or 2)
* starting on any note ```note``` of the twelve notes
* increasing, decreasing, increasing-decreasing or
  decreasing-increasing (let ```direction``` the direction(s) of the
  scale)
* any scale ```scale``` found on wikipedia.

For each fixed scale ```s``` and starting note ```n``` there is an
anki note. It contains one field for each ```{h}{o}{d}``` for each
value of h o and d. We use the fact that each fields have such a
fixed form to create a function which, generate the template. Those
values are entered in two fields ```Note``` and ```Scales```.

More precisely, instead of ```d``` the function takes two parameters:
* Back, which states whether the scale is played in both directions
* Increase, which states if the scale start by increasing.

Depending on those two informations, we decide which arrows to show,
to indicate the direction to play in the question side. Depending on
the variable ```hand``` we decide which hand(s) to display.

Finally, this code allow us to have very simple templates in each
card's type. The template being:
```html
<span template="eval" object="pianoScale(hand,nbOctave,back,increase)
```
where the four variables are replaced by the expected value.

## Appendix
Those scales have been generated using (this
program)[https://github.com/Arthur-Milchior/generate-musical-image]. This
is not related to this add-on and I will not describe the process.

The notes themselves were also created by this program, and then imported.
