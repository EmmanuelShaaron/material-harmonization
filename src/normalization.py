import re
import pandas as pd
from pathlib import Path


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(text):
    """
    Normalize a material description while preserving
    important technical information.
    """

    if pd.isna(text):
        return ""

    text = str(text).upper().strip()

    # --------------------------------------------------------
    # Standardize common separators
    # --------------------------------------------------------

    text = text.replace("–", "-")
    text = text.replace("—", "-")
    text = text.replace("/", " ")
    text = text.replace(",", " ")

    # --------------------------------------------------------
    # Normalize common material abbreviations
    # --------------------------------------------------------

    replacements = {
        r"\bSS\s*304\b": "SS304",
        r"\bSS\s*316\b": "SS316",
        r"\bSTAINLESS\s+STEEL\b": "STAINLESS STEEL",
        r"\bCARBON\s+STEEL\b": "CARBON STEEL",
        r"\bGALVANIZED\s+STEEL\b": "GALVANIZED STEEL",
        r"\bGALV\b": "GALVANIZED",
    }

    for pattern, replacement in replacements.items():
        text = re.sub(pattern, replacement, text)

    # --------------------------------------------------------
    # Normalize dimensions
    #
    # M10 X 50
    # M10X50
    # M10-50
    #
    # → M10X50
    # --------------------------------------------------------

    text = re.sub(
        r"\bM\s*(\d+)\s*[-X]\s*(\d+)\b",
        r"M\1X\2",
        text
    )

    # --------------------------------------------------------
    # Normalize inch notation
    #
    # 2 IN
    # 2IN
    # 2"
    #
    # → 2IN
    # --------------------------------------------------------

    text = re.sub(
        r'(\d+(?:\.\d+)?)\s*(?:INCH|IN|\")\b',
        r"\1IN",
        text
    )

    # --------------------------------------------------------
    # Normalize SQMM / SQ MM
    # --------------------------------------------------------

    text = re.sub(
        r"\bSQ\s*MM\b",
        "SQMM",
        text
    )

    # --------------------------------------------------------
    # Normalize common abbreviations
    # --------------------------------------------------------

    abbreviation_map = {
        r"\bBRG\b": "BEARING",
        r"\bVLV\b": "VALVE",
        r"\bFLG\b": "FLANGE",
        r"\bGKT\b": "GASKET",
        r"\bPMP\b": "PUMP",
        r"\bMTR\b": "MOTOR",
        r"\bCS\b": "CARBON STEEL",
        r"\bGI\b": "GALVANIZED STEEL",
    }

    for pattern, replacement in abbreviation_map.items():
        text = re.sub(pattern, replacement, text)

    # --------------------------------------------------------
    # Remove punctuation except X and decimal points
    # --------------------------------------------------------

    text = re.sub(r"[^A-Z0-9.\sX#-]", " ", text)

    # --------------------------------------------------------
    # Normalize whitespace
    # --------------------------------------------------------

    text = re.sub(r"\s+", " ", text).strip()

    return text


# ============================================================
# EXTRACT DESCRIPTION FROM CPSE RECORD
# ============================================================

def get_description(row):

    if pd.notna(row.get("description")):
        return row["description"]

    if pd.notna(row.get("item_name")):
        return row["item_name"]

    if pd.notna(row.get("short_text")):
        return row["short_text"]

    return ""


# ============================================================
# TEST THE NORMALIZER
# ============================================================

if __name__ == "__main__":

    examples = [
        "M10 X 50 SS304 HEX BOLT",
        "M10X50 SS 304 HEX BOLT",
        "M10-50 SS304 HEX. BOLT",
        "2 IN SS304 GATE VALVE 150 CLASS",
        "2\" SS304 GATE VALVE 150 CLASS",
        "DEEP GROOVE BALL BRG 6205",
        "CENTRIFUGAL PMP 20 M3/H 30M HEAD 5.5KW",
        "4C X 25 SQ MM PVC CABLE 1.1KV",
    ]

    print("=" * 60)
    print("TEXT NORMALIZATION TEST")
    print("=" * 60)

    for example in examples:

        normalized = normalize_text(example)

        print(f"\nOriginal : {example}")
        print(f"Normalized: {normalized}")

    print("\n" + "=" * 60)