from ...generators import *

def scale(octaveNumber=1, nbOctave = 1, back=False, increase=True):
    # arrows: which arrow to show and in which order
    # Suffix -- End of field name

    # Values changing depending on which sides it goes
    low = SUB(str(octaveNumber - 1))
    high = SUP(str(octaveNumber + nbOctave - 1))
    increasingImage = Image(f"_increasing_arrow.png")
    decreasingImage = Image(f"_decreasing_arrow.png")
    if back:
        if increase:
            suffix = "/\\"
            arrow = [low, increasingImage, high, decreasingImage, low]
        else:
            suffix = "\\/"
            arrow = [high, decreasingImage, low, increasingImage, high]
    else:
        if increase:
            suffix = "/"
            arrow = [low, increasingImage, high]
        else:
            suffix = "\\"
            arrow = [high, decreasingImage, low]

    octaveNumbers = [str(i) for i in range(octaveNumber, octaveNumber+nbOctave)]
    octaveNumbersReverse = octaveNumbers[::-1]
    octaves = "".join(octaveNumbers)
    mandatoryFields = []
    for suffixPart in suffix:
        on = octaveNumbers if suffixPart == "/" else octaveNumbersReverse
        for octaveNumber in on:
            mandatoryFields.append(f"{octaveNumber} {suffixPart}")

    fieldName = f"{octaves} {suffix}"
    print(f"field name is {fieldName}")

    nbOctaveText = f"""{nbOctave} octave{"s" if nbOctave>1 else ""}"""

    scales = (fieldName, {fieldName}, [{mandatoryFieldName} for mandatoryFieldName in mandatoryFields])

    content = [Answer([scales, hr]),
               {"Instrument"}, {"Name"}, " ", {"Start"}, hr,
               arrow,
               #nbOctaveText
    ]
    return MultipleRequirement(child=content, requireFilled=mandatoryFields)
