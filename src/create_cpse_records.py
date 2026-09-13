import pandas as pd
import random
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

random.seed(42)

INPUT_FILE = Path("data/benchmark/canonical_materials.csv")
OUTPUT_FILE = Path("data/benchmark/material_records.csv")


# ============================================================
# LOAD CANONICAL MATERIALS
# ============================================================

df = pd.read_csv(INPUT_FILE)

print("=" * 60)
print("GENERATING CPSE MATERIAL RECORDS")
print("=" * 60)

print(f"Canonical materials loaded: {len(df)}")


# ============================================================
# TEXT VARIATION FUNCTIONS
# ============================================================

def variation_a(description):
    """
    CPSE-A:
    Mostly readable descriptions with common abbreviations.
    """

    text = description.upper()

    replacements = {
        "STAINLESS STEEL": "SS",
        "CARBON STEEL": "CS",
        "GALVANIZED STEEL": "GI",
        "BEARING": "BRG",
        "VALVE": "VLV",
        "FLANGE": "FLG",
        "GASKET": "GKT",
        "PIPE": "PIP",
        "CENTRIFUGAL": "CENT",
        "MOTOR": "MTR",
        "PUMP": "PMP",
        "ELECTRIC": "ELEC",
        "CABLE": "CABL",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text


def variation_b(description):
    """
    CPSE-B:
    Different word ordering and punctuation.
    """

    text = description.upper()

    replacements = {
        "STAINLESS STEEL": "SS",
        "CARBON STEEL": "CS",
        "GALVANIZED STEEL": "GALV",
        "BEARING": "BEARING",
        "VALVE": "VAL",
        "FLANGE": "FLG",
        "GASKET": "GASK",
        "PIPE": "PIPE",
        "CENTRIFUGAL": "CENTRIF",
        "MOTOR": "MOTOR",
        "PUMP": "PUMP",
        "ELECTRIC": "ELEC",
        "CABLE": "CABLE",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    # Change common formatting
    text = text.replace(" X ", "X")
    text = text.replace(" IN ", "\"")
    text = text.replace(" CLASS", "#")

    return text


def variation_c(description):
    """
    CPSE-C:
    More compressed / ERP-style material descriptions.
    """

    text = description.upper()

    replacements = {
        "STAINLESS STEEL": "SS",
        "CARBON STEEL": "CS",
        "GALVANIZED STEEL": "GI",
        "DEEP GROOVE BALL": "DGB",
        "TAPERED ROLLER": "TR",
        "SPHERICAL ROLLER": "SR",
        "BEARING": "BRG",
        "GATE VALVE": "GTV",
        "BALL VALVE": "BLV",
        "BUTTERFLY VALVE": "BFV",
        "GLOBE VALVE": "GLV",
        "WELD NECK FLANGE": "WN FLG",
        "SLIP ON FLANGE": "SO FLG",
        "SPIRAL WOUND": "SW",
        "FULL FACE": "FF",
        "CENTRIFUGAL PUMP": "C/PMP",
        "INDUCTION MOTOR": "IND MTR",
        "ELECTRIC DRILL": "E-DRILL",
        "ANGLE GRINDER": "A/GRINDER",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    # Remove some spaces around X
    text = text.replace(" X ", "X")

    return text


# ============================================================
# CREATE RECORDS
# ============================================================

records = []

cpse_configs = [
    ("CPSE-A", variation_a),
    ("CPSE-B", variation_b),
    ("CPSE-C", variation_c),
]


for _, row in df.iterrows():

    for cpse_name, variation_function in cpse_configs:

        description = variation_function(
            row["canonical_description"]
        )

        # ----------------------------------------------------
        # Generate CPSE-specific material code
        # ----------------------------------------------------

        cpse_code = (
            f"{cpse_name.replace('-', '')}-"
            f"{random.randint(100000, 999999)}"
        )

        # ----------------------------------------------------
        # Different schemas
        # ----------------------------------------------------

        if cpse_name == "CPSE-A":

            record = {
                "cpse": cpse_name,
                "material_code": cpse_code,
                "description": description,
                "uom": row["uom"],
                "canonical_id": row["canonical_id"],
            }

        elif cpse_name == "CPSE-B":

            record = {
                "cpse": cpse_name,
                "item_id": cpse_code,
                "item_name": description,
                "unit": row["uom"],
                "canonical_id": row["canonical_id"],
            }

        else:

            record = {
                "cpse": cpse_name,
                "mat_no": cpse_code,
                "short_text": description,
                "base_uom": row["uom"],
                "canonical_id": row["canonical_id"],
            }

        records.append(record)


# ============================================================
# COMBINE
# ============================================================

records_df = pd.DataFrame(records)


# ============================================================
# ADD TECHNICAL ATTRIBUTES
# ============================================================

# We keep the canonical technical attributes internally
# so that later we can evaluate matching performance.

technical_columns = [
    "category",
    "material",
    "grade",
    "standard",
    "diameter_mm",
    "length_mm",
    "size_in",
    "pressure_class",
    "schedule",
    "voltage_v",
    "power_kw",
    "flow_rate_m3h",
    "head_m",
    "cores",
    "cross_section_mm2",
    "bearing_number",
    "valve_type",
    "flange_type",
    "gasket_type",
    "tool_type",
    "tool_size_mm",
]

records_df = records_df.merge(
    df[["canonical_id"] + technical_columns],
    on="canonical_id",
    how="left"
)


# ============================================================
# SHUFFLE
# ============================================================

records_df = records_df.sample(
    frac=1,
    random_state=42
).reset_index(drop=True)


# ============================================================
# SAVE
# ============================================================

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

records_df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# REPORT
# ============================================================

print("\n" + "=" * 60)
print("CPSE RECORD GENERATION COMPLETE")
print("=" * 60)

print(f"Total CPSE records: {len(records_df)}")

print("\nRecords by CPSE:")
print(records_df["cpse"].value_counts())

print("\nColumns:")
print(list(records_df.columns))

print("\nSample records:")

display_columns = [
    "cpse",
    "canonical_id",
]

# Show whichever description column exists
for column in ["description", "item_name", "short_text"]:
    if column in records_df.columns:
        display_columns.append(column)

display_columns.append("uom" if "uom" in records_df.columns else "unit")

print(
    records_df[
        display_columns
    ].head(15).to_string(index=False)
)

print("\n" + "=" * 60)
print(f"Saved to: {OUTPUT_FILE}")
print("=" * 60)