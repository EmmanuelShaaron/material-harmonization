
import pandas as pd


# ========================================================
# LOAD DATA
# ========================================================

results = pd.read_csv(
    "data/processed/final_matches.csv"
)

records = pd.read_csv(
    "data/processed/processed_material_records.csv"
)

canonical = pd.read_csv(
    "data/benchmark/canonical_materials.csv"
)


# ========================================================
# PREPARE CPSE MATERIAL IDENTIFIER
# ========================================================

# Different CPSEs use different column names.
# Create one common material-code column.

def get_cpse_code(row):

    if pd.notna(row.get("material_code")):
        return row["material_code"]

    if pd.notna(row.get("item_id")):
        return row["item_id"]

    if pd.notna(row.get("mat_no")):
        return row["mat_no"]

    return ""


records["cpse_material_code"] = records.apply(
    get_cpse_code,
    axis=1
)



# ========================================================
# MERGE MATCH RESULTS WITH CPSE DATA
# ========================================================

# final_matches.csv already contains the record_id.
# The processed records file may not contain record_id,
# so create the same stable ID from its row order.

records = records.reset_index(drop=True)
records["record_id"] = records.index


mapping = results.merge(
    records[
        [
            "record_id",
            "cpse_material_code"
        ]
    ],
    on="record_id",
    how="left"
)


# ========================================================
# GENERATE COMMON NATIONAL MATERIAL CODE
# ========================================================

def create_national_code(row):

    canonical_id = str(
        row["predicted_canonical_id"]
    )

    category = str(
        row["category"]
    ).upper()

    # CM0021 -> 0021
    number = canonical_id.replace("CM", "")

    return f"NMMC-{category}-{number}"


mapping["national_material_code"] = mapping.apply(
    create_national_code,
    axis=1
)


# ========================================================
# SELECT FINAL HARMONIZATION FIELDS
# ========================================================

harmonized = mapping[
    [
        "record_id",
        "cpse",
        "cpse_material_code",
        "original_description",
        "predicted_canonical_id",
        "national_material_code",
        "confidence",
        "final_decision"
    ]
].copy()


# ========================================================
# SAVE
# ========================================================

output_path = (
    "data/processed/"
    "harmonized_material_mapping.csv"
)

harmonized.to_csv(
    output_path,
    index=False
)


# ========================================================
# SUMMARY
# ========================================================

print("Harmonized records:", len(harmonized))

print("\nMappings by CPSE:")

print(
    harmonized["cpse"]
    .value_counts()
)

print("\nDecision distribution:")

print(
    harmonized["final_decision"]
    .value_counts()
)

print("\nSample harmonized mappings:")

print(
    harmonized.head(10).to_string(
        index=False
    )
)

print("\nSaved to:", output_path)

