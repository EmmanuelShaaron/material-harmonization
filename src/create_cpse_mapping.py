import pandas as pd
from pathlib import Path


# ========================================================
# INPUTS
# ========================================================

RECORDS_FILE = "data/processed/processed_material_records.csv"
MATCHES_FILE = "data/processed/final_matches.csv"
NATIONAL_MASTER_FILE = "data/processed/national_material_master.csv"

OUTPUT_FILE = "data/processed/cpse_material_mapping.csv"


# ========================================================
# LOAD DATA
# ========================================================

records = pd.read_csv(RECORDS_FILE)
matches = pd.read_csv(MATCHES_FILE)
national_master = pd.read_csv(NATIONAL_MASTER_FILE)

print("CPSE records:", len(records))
print("Final matches:", len(matches))
print("National materials:", len(national_master))


# ========================================================
# RECREATE RECORD IDs
# ========================================================

records = records.reset_index(drop=True)
records["record_id"] = records.index


# ========================================================
# NORMALIZE CPSE-SPECIFIC SCHEMAS
# ========================================================

# Each CPSE deliberately uses different field names.
# Convert them into one common representation.

records["standard_material_code"] = records["material_code"]

records.loc[
    records["cpse"] == "CPSE-B",
    "standard_material_code"
] = records.loc[
    records["cpse"] == "CPSE-B",
    "item_id"
]

records.loc[
    records["cpse"] == "CPSE-C",
    "standard_material_code"
] = records.loc[
    records["cpse"] == "CPSE-C",
    "mat_no"
]


# --------------------------------------------------------
# Description
# --------------------------------------------------------

records["standard_description"] = records["description"]

records.loc[
    records["cpse"] == "CPSE-B",
    "standard_description"
] = records.loc[
    records["cpse"] == "CPSE-B",
    "item_name"
]

records.loc[
    records["cpse"] == "CPSE-C",
    "standard_description"
] = records.loc[
    records["cpse"] == "CPSE-C",
    "short_text"
]


# --------------------------------------------------------
# UOM
# --------------------------------------------------------

records["standard_uom"] = records["uom"]

records.loc[
    records["cpse"] == "CPSE-B",
    "standard_uom"
] = records.loc[
    records["cpse"] == "CPSE-B",
    "unit"
]

records.loc[
    records["cpse"] == "CPSE-C",
    "standard_uom"
] = records.loc[
    records["cpse"] == "CPSE-C",
    "base_uom"
]


# ========================================================
# KEEP RECORD INFORMATION
# ========================================================

record_info = records[
    [
        "record_id",
        "cpse",
        "standard_material_code",
        "standard_description",
        "standard_uom"
    ]
].copy()


record_info = record_info.rename(
    columns={
        "standard_material_code": "cpse_material_code",
        "standard_description": "cpse_description",
        "standard_uom": "cpse_uom"
    }
)


# ========================================================
# KEEP MATCH INFORMATION
# ========================================================

match_info = matches[
    [
        "record_id",
        "predicted_canonical_id",
        "confidence",
        "confidence_gap",
        "conflict_count",
        "attribute_evidence",
        "final_decision"
    ]
].copy()
# ========================================================
# MERGE MATCH RESULTS + CPSE INFORMATION
# ========================================================

mapping = match_info.merge(
    record_info,
    on="record_id",
    how="left"
)


# ========================================================
# NATIONAL MASTER INFORMATION
# ========================================================

national_info = national_master[
    [
        "canonical_id",
        "national_material_code",
        "category",
        "canonical_description"
    ]
].copy()


# ========================================================
# MAP CANONICAL MATERIAL → NATIONAL CODE
# ========================================================

mapping = mapping.merge(
    national_info,
    left_on="predicted_canonical_id",
    right_on="canonical_id",
    how="left"
)


# ========================================================
# FINAL MAPPING TABLE
# ========================================================

final_mapping = mapping[
    [
        "record_id",
        "cpse",
        "cpse_material_code",
        "cpse_description",
        "cpse_uom",
        "national_material_code",
        "predicted_canonical_id",
        "canonical_description",
        "category",
        "confidence",
        "confidence_gap",
        "conflict_count",
        "attribute_evidence",

        "final_decision"
    ]
].copy()


# ========================================================
# MAPPING STATUS
# ========================================================

def get_mapping_status(decision):

    if decision == "MATCH":
        return "AUTO_MAPPED"

    elif decision == "REVIEW":
        return "PENDING_REVIEW"

    else:
        return "UNMAPPED"


final_mapping["mapping_status"] = (
    final_mapping["final_decision"]
    .apply(get_mapping_status)
)


# ========================================================
# SAVE
# ========================================================

Path("data/processed").mkdir(
    parents=True,
    exist_ok=True
)

final_mapping.to_csv(
    OUTPUT_FILE,
    index=False
)


# ========================================================
# SUMMARY
# ========================================================

print()
print("=" * 60)
print("CPSE → NATIONAL MATERIAL MAPPING")
print("=" * 60)

print("Total records:", len(final_mapping))

print()
print("Mapping status:")
print(
    final_mapping["mapping_status"]
    .value_counts()
)

print()
print("Mappings by CPSE:")
print(
    final_mapping
    .groupby(["cpse", "mapping_status"])
    .size()
)

print()
print("Sample mappings:")

print(
    final_mapping[
        [
            "cpse",
            "cpse_material_code",
            "cpse_description",
            "national_material_code",
            "confidence",
            "mapping_status"
        ]
    ]
    .head(15)
    .to_string(index=False)
)

print()
print("Saved to:", OUTPUT_FILE)