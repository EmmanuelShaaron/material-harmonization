import re
import pandas as pd


# ============================================================
# TECHNICAL ATTRIBUTE EXTRACTION
# ============================================================

def extract_attributes(text):

    if pd.isna(text):
        text = ""

    text = str(text).upper()

    attributes = {
        "diameter_mm": None,
        "length_mm": None,
        "size_in": None,
        "grade": None,
        "pressure_class": None,
        "schedule": None,
        "voltage_v": None,
        "power_kw": None,
        "flow_rate_m3h": None,
        "head_m": None,
        "cores": None,
        "cross_section_mm2": None,
        "bearing_number": None,
        "valve_type": None,
        "flange_type": None,
        "gasket_type": None,
        "tool_type": None,
        "tool_size_mm": None,
    }


    # ========================================================
    # FASTENER DIMENSIONS
    # Example: M10X50
    # ========================================================

    match = re.search(
        r"\bM\s*(\d+(?:\.\d+)?)\s*X\s*(\d+(?:\.\d+)?)\b",
        text
    )

    if match:

        attributes["diameter_mm"] = float(match.group(1))
        attributes["length_mm"] = float(match.group(2))


    # ========================================================
    # MATERIAL GRADES
    # ========================================================

    grade_patterns = [
        r"\bSS\s*304\b",
        r"\bSS\s*316\b",
        r"\bCS\b",
        r"\bCARBON STEEL\b",
        r"\bGI\b",
        r"\bGALVANIZED STEEL\b",
    ]

    for pattern in grade_patterns:

        match = re.search(pattern, text)

        if match:

            value = match.group(0)

            value = re.sub(
                r"\s+",
                "",
                value
            )

            if value == "CARBONSTEEL":
                value = "CS"

            if value == "GALVANIZEDSTEEL":
                value = "GI"

            attributes["grade"] = value

            break


    # ========================================================
    # INCH SIZE
    #
    # 2 IN
    # 2IN
    # 2"
    # ========================================================

    match = re.search(
        r"\b(\d+(?:\.\d+)?)\s*(?:INCH|IN)\b",
        text
    )

    if match:

        attributes["size_in"] = float(
            match.group(1)
        )

    else:

        match = re.search(
            r'\b(\d+(?:\.\d+)?)"',
            text
        )

        if match:

            attributes["size_in"] = float(
                match.group(1)
            )


    # ========================================================
    # PRESSURE CLASS
    #
    # 150 CLASS
    # 300 CLASS
    # 150#
    # ========================================================
    match = re.search(
        r"\b(\d+)\s*(?:CLASS\b|#)",
        text
    )
    if match:

        attributes["pressure_class"] = int(
            match.group(1)
        )


    # ========================================================
    # PIPE SCHEDULE
    #
    # SCH40
    # SCH 40
    # ========================================================

    match = re.search(
        r"\bSCH\s*(\d+)\b",
        text
    )

    if match:

        attributes["schedule"] = int(
            match.group(1)
        )


    # ========================================================
    # VOLTAGE
    #
    # 415V
    # 1100V
    # 1.1KV
    # ========================================================

    match = re.search(
        r"\b(\d+(?:\.\d+)?)\s*KV\b",
        text
    )

    if match:

        attributes["voltage_v"] = float(
            match.group(1)
        ) * 1000

    else:

        match = re.search(
            r"\b(\d+(?:\.\d+)?)\s*V\b",
            text
        )

        if match:

            attributes["voltage_v"] = float(
                match.group(1)
            )


    # ========================================================
    # POWER
    #
    # 5.5KW
    # 750W
    # ========================================================

    match = re.search(
        r"\b(\d+(?:\.\d+)?)\s*KW\b",
        text
    )

    if match:

        attributes["power_kw"] = float(
            match.group(1)
        )

    else:

        match = re.search(
            r"\b(\d+(?:\.\d+)?)\s*W\b",
            text
        )

        if match:

            attributes["power_kw"] = float(
                match.group(1)
            ) / 1000


    # ========================================================
    # PUMP FLOW RATE
    #
    # 20 M3/H
    # 100 M3/H
    # ========================================================

    match = re.search(
        r"\b(\d+(?:\.\d+)?)\s*M3\s*/?\s*H\b",
        text
    )

    if match:

        attributes["flow_rate_m3h"] = float(
            match.group(1)
        )


    # ========================================================
    # PUMP HEAD
    #
    # 30M HEAD
    # 50 M HEAD
    # ========================================================

    match = re.search(
        r"\b(\d+(?:\.\d+)?)\s*M\s*HEAD\b",
        text
    )

    if match:

        attributes["head_m"] = float(
            match.group(1)
        )


# ========================================================
# ELECTRICAL CABLE
# ========================================================

# Detect combined cable notation.
#
# Supported:
# 4CX25 SQMM
# 4CX10 SQMM
# 3CX6 SQMM
# 3CX35 SQMM
# 1CX2.5 SQMM
# 4C X 25 SQMM
# 3C X 6 SQMM

    cable_match = re.search(
        r"(\d+)\s*C\s*X\s*(\d+(?:\.\d+)?)\s*SQ\s*MM",
        text
    )

    if cable_match:

        attributes["cores"] = int(
            cable_match.group(1)
        )

        attributes["cross_section_mm2"] = float(
            cable_match.group(2)
        )

    else:

        # Standalone core count
        core_match = re.search(
            r"(\d+)\s*C\b",
            text
        )

        if core_match:
            attributes["cores"] = int(
                core_match.group(1)
            )

        # Standalone cross section
        section_match = re.search(
            r"(\d+(?:\.\d+)?)\s*SQ\s*MM",
            text
        )

        if section_match:
            attributes["cross_section_mm2"] = float(
                section_match.group(1)
            )

    # ========================================================
    # BEARING NUMBER
    #
    # 6205
    # 30205
    # 22205
    # ========================================================

    match = re.search(
        r"\b(6\d{3}|3\d{4}|2\d{4})\b",
        text
    )

    if match:

        attributes["bearing_number"] = match.group(1)


    # ========================================================
    # VALVE TYPE
    # ========================================================

    valve_types = [
        "GATE",
        "BALL",
        "BUTTERFLY",
        "GLOBE",
    ]

    # Only detect valve type when the description is actually a valve
    if re.search(r"\bVALVE\b", text):
        for valve_type in valve_types:
            if re.search(
                rf"\b{valve_type}\b",
                text
            ):
                attributes["valve_type"] = valve_type
                break


    # ========================================================
    # FLANGE TYPE
    # ========================================================

    if "WELD NECK" in text or "WN FLG" in text:

        attributes["flange_type"] = "WELD NECK"

    elif "SLIP ON" in text or "SO FLG" in text:

        attributes["flange_type"] = "SLIP ON"


# ========================================================
# CABLE CROSS SECTION
#
# Supports:
# 25 SQMM
# 25 SQ MM
# 3CX25 SQMM
# 4CX16 SQMM
# ========================================================

    match = re.search(
        r"\b\d+\s*C\s*X\s*(\d+(?:\.\d+)?)\s*SQ\s*MM\b",
        text
    )

    if match:
        attributes["cross_section_mm2"] = float(match.group(1))

    else:
        match = re.search(
            r"\b(\d+(?:\.\d+)?)\s*SQ\s*MM\b",
            text
        )

        if match:
            attributes["cross_section_mm2"] = float(match.group(1))


    # ========================================================
    # INDUSTRIAL TOOL TYPE
    # ========================================================

    tool_types = [
        "ANGLE GRINDER",
        "A/GRINDER",
        "DRILL",
        "IMPACT WRENCH",
        "CUTTING MACHINE",
        "WELDING MACHINE",
        "TORQUE WRENCH",
        "BENCH GRINDER",
    ]

    for tool_type in tool_types:

        if tool_type in text:

            attributes["tool_type"] = tool_type

            break


    # ========================================================
    # TOOL SIZE
    # ========================================================

    if attributes["tool_type"]:

        match = re.search(
            r"\b(\d+(?:\.\d+)?)\s*MM\b",
            text
        )

        if match:

            attributes["tool_size_mm"] = float(
                match.group(1)
            )


    return attributes


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    examples = [

        "M10X50 SS304 HEX BOLT",

        '2" SS304 GATE VALVE 150 CLASS',

        "4 IN SS316 WELD NECK FLANGE 300 CLASS",

        "6 IN CS SEAMLESS PIPE SCH80",

        "CENTRIFUGAL PUMP 20 M3/H 30M HEAD 5.5KW",

        "3 PHASE INDUCTION MOTOR 15KW 415V 50HZ",

        "4C X 25 SQMM PVC CABLE 1.1KV",

        "DEEP GROOVE BALL BEARING 6205",

        "ANGLE GRINDER 125MM 1100W",
        "3CX6 SQMM PVC CABLE 1.1KV",
        "3CX35 SQMM PVC CABLE 1.1KV",
        "4CX16 SQMM PVC CABLE 1.1KV",
        "4CX25 SQMM PVC CABLE 1.1KV",
        "10 IN GRAPHITE SPIRAL WOUND GASKET 150 CLASS",
        "12 IN GRAPHITE SPIRAL WOUND GASKET 300 CLASS",
    ]


    print("=" * 60)
    print("TECHNICAL ATTRIBUTE EXTRACTION TEST")
    print("=" * 60)


    for example in examples:

        result = extract_attributes(example)

        print("\nDescription:")
        print(example)

        print("\nExtracted:")

        for key, value in result.items():

            if value is not None:

                print(
                    f"  {key}: {value}"
                )


    print("\n" + "=" * 60)