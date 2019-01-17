from ...generators import *

def pianoScale(hand="right", nbOctave = 1,back=False,increase=True):
    hand = Image(f"_{hand}_hand.png")
    if hand=="both":
        hand = [Image("_left_hand.png"),
                Image("_right_hand.png")]
    
    
    if back:
        if increase:
            suffix = "increasing"
            arrow = ["increasing"]
        else:
            suffix = "decreasing"
            arrow = ["decreasing"]
    else:
        if increase:
            suffix = "total"
            arrow = ["increasing","decreasing"]
        else:
            suffix = "reverse"
            arrow = ["decreasing","increasing"]
            
    nbOctave = f"""{nbOctave} octave{"s" if nbOctave>1 else ""}"""
    [Answer([{f"{hand}{nbOctave}{suffix}"},hr]),
     {"Note"}, " ", {"Scale"}, hr,
     hand,
     arrow,
     nbOctave]
