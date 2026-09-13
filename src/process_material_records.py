import pandas as pd

from normalization import normalize_text, get_description
from attribute_extraction import extract_attributes


# ========================================================
# LOAD RAW MATERIAL RECORDS
# ========================================================

input_path = (
    "data/benchmark/material_records.csv"
)

records = pd.read_csv(
    input_path
)


# ========================================================
# TECHNICAL ATTRIBUTE LIST
# ========================================================

TECHNICAL_ATTRIBUTES = [
    "diameter_mm",
    "length_mm",
    "size_in",
    "grade",
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


# ========================================================
# PROCESS RECORDS
# ========================================================

processed_records = []


for _, row in records.iterrows():

    # ----------------------------------------------------
    # Get description from the CPSE-specific schema
    # ----------------------------------------------------

    original_description = get_description(row)

    # ----------------------------------------------------
    # Normalize description
    # ----------------------------------------------------

    normalized_description = normalize_text(
        original_description
    )

    # ----------------------------------------------------
    # Extract technical attributes
    # ----------------------------------------------------

    extracted_attributes = extract_attributes(
        original_description
    )

    # ----------------------------------------------------
    # Start with original row
    # ----------------------------------------------------

    processed_row = row.to_dict()

    # ----------------------------------------------------
    # Add standardized descriptions
    # ----------------------------------------------------

    processed_row[
        "original_description"
    ] = original_description

    processed_row[
        "normalized_description"
    ] = normalized_description

    # ----------------------------------------------------
    # IMPORTANT:
    # Remove old technical attributes.
    #
    # Otherwise pandas can preserve the old NaN values
    # from the raw CPSE schema.
    # ----------------------------------------------------

    for attribute in TECHNICAL_ATTRIBUTES:

        processed_row.pop(
            attribute,
            None
        )

    # ----------------------------------------------------
    # Add freshly extracted attributes
    # ----------------------------------------------------

    processed_row.update(
        extracted_attributes
    )

    processed_records.append(
        processed_row
    )


# ========================================================
# CREATE DATAFRAME
# ========================================================

processed_df = pd.DataFrame(
    processed_records
)


# ========================================================
# SAVE PROCESSED DATA
# ========================================================

output_path = (
    "data/processed/processed_material_records.csv"
)

processed_df.to_csv(
    output_path,
    index=False
)


# ========================================================
# SUMMARY
# ========================================================

print(
    "Input records:",
    len(records)
)

print(
    "Processed records:",
    len(processed_df)
)

print(
    "\nCPSE distribution:"
)

print(
    processed_df["cpse"].value_counts()
)


# ========================================================
# VERIFY CABLE EXTRACTION
# ========================================================

print(
    "\nCable attribute verification:"
)

cable_records = processed_df[
    processed_df["category"]
    ==
    "ELECTRICAL_CABLE"
]

print(
    cable_records[
        [
            "original_description",
            "cores",
            "cross_section_mm2",
            "voltage_v",
            "canonical_id"
        ]
    ]
    .head(15)
    .to_string(index=False)
)


print(
    "\nSaved to:",
    output_path
)