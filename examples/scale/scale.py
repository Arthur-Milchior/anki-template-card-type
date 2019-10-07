from ...generators import *

def scale(octaveNumber=1, nbOctave = 1, back=False, increase=True):
    # arrows: which arrow to show and in which order
    # Suffix -- End of field name

    # Values changing depending on which sides it goes
    start_number = octaveNumber - 1
    end_number = octaveNumber + nbOctave - 1
    start_string = str(start_number)
    end_string = str(end_number)
    start_field = {start_string}
    end_field = {end_string}
    start_text = SUB(str(start))
    end_text = SUP(str(end))
    start = FilledOrEmpty(
        str(start_number),
        start_field,
        start_number
    )
    end = FilledOrEmpty(
        str(end_number),
        end_field,
        end_number
    )

    increasingImage = Image(f"_increasing_arrow.png")
    decreasingImage = Image(f"_decreasing_arrow.png")
    if back:
        if increase:
            suffix = "/\\"
            arrow = [start, increasingImage, end, decreasingImage, start]
        else:
            suffix = "\\/"
            arrow = [end, decreasingImage, start, increasingImage, end]
    else:
        if increase:
            suffix = "/"
            arrow = [start, increasingImage, end]
        else:
            suffix = "\\"
            arrow = [end, decreasingImage, start]

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
