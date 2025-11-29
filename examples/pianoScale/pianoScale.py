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
    tonic = Field("Tonic", useClasses=False)
    name = FilledOrEmpty("Scale notation", [tonic, Field("Scale notation", useClasses=False)], [tonic, " ", {"Scale name"}])
    content = [Answer([Field(fieldName, isMandatory=True), hr]),
               name, hr,
               handImage,
               arrowImage,
               nbOctaveText]
    if nbOctave == 1:
        content = Filled("Practice single octave", content)
    if hand != "Both":
        content = Filled("Practice hands separate", content)
    if not back :
        content = Filled("Practice single direction", content)
    return Filled(fieldName, content)
