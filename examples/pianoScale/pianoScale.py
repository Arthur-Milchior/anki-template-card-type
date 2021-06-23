from ...generators import *


def pianoScale(hand="right", nbOctave=1, back=False, increase=True):
    if hand == "Both":
        handImage = [Image("_Left_hand.png"),
                     Image("_Right_hand.png")]
    else:
        handImage = Image(f"_{hand}_hand.png")

    if back:
        if increase:
            suffix = "total"
            arrow = ["increasing", "decreasing"]
        else:
            suffix = "reverse"
            arrow = ["decreasing", "increasing"]
    else:
        if increase:
            suffix = "increasing"
            arrow = ["increasing"]
        else:
            suffix = "decreasing"
            arrow = ["decreasing"]

    arrowImage = [Image(f"_{side}_arrow.png") for side in arrow]

    nbOctaveText = f"""{nbOctave} octave{"s" if nbOctave>1 else ""}"""
    fieldName = f"{hand}{nbOctave}{suffix}"
    content = [Answer([Field(fieldName, isMandatory=True), hr]),
               {"Tonic"}, " ", {"Scale"}, hr,
               handImage,
               arrowImage,
               nbOctaveText]
    return Filled(fieldName, content)
