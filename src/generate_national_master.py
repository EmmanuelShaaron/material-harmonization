import pandas as pd
from pathlib import Path


# ========================================================
# CONFIGURATION
# ========================================================

INPUT_FILE = "data/benchmark/canonical_materials.csv"
OUTPUT_FILE = "data/processed/national_material_master.csv"


# ========================================================
# CATEGORY PREFIXES
# ========================================================

CATEGORY_PREFIX = {
    "FASTENER": "FAST",
    "BEARING": "BEAR",
    "VALVE": "VALV",
    "PIPE": "PIPE",
    "FLANGE": "FLG",
    "GASKET": "GASK",
    "ELECTRICAL_CABLE": "CABL",
    "MOTOR": "MOTR",
    "PUMP": "PUMP",
    "INDUSTRIAL_TOOL": "TOOL",
}


# ========================================================
# LOAD CANONICAL MATERIALS
# ========================================================

canonical_df = pd.read_csv(INPUT_FILE)

print("Canonical materials loaded:", len(canonical_df))


# ========================================================
# GENERATE NATIONAL MATERIAL CODES
# ========================================================

category_counters = {}

national_codes = []

for _, row in canonical_df.iterrows():

    category = row["category"]

    prefix = CATEGORY_PREFIX.get(category, "MAT")

    category_counters[category] = (
        category_counters.get(category, 0) + 1
    )

    sequence = category_counters[category]

    national_code = f"NMC-{prefix}-{sequence:04d}"

    national_codes.append(national_code)


# ========================================================
# CREATE NATIONAL MASTER
# ========================================================

national_master = canonical_df.copy()

national_master.insert(
    1,
    "national_material_code",
    national_codes
)

national_master["status"] = "ACTIVE"

national_master["approval_status"] = "APPROVED"

national_master["source"] = "NATIONAL_HARMONIZATION_ENGINE"


# ========================================================
# SAVE
# ========================================================

Path("data/processed").mkdir(
    parents=True,
    exist_ok=True
)

national_master.to_csv(
    OUTPUT_FILE,
    index=False
)


# ========================================================
# SUMMARY
# ========================================================

print()
print("=" * 60)
print("NATIONAL MATERIAL MASTER")
print("=" * 60)

print("Total national materials:", len(national_master))

print()
print("Materials by category:")
print(
    national_master["category"]
    .value_counts()
    .sort_index()
)

print()
print("Sample national codes:")

print(
    national_master[
        [
            "national_material_code",
            "canonical_id",
            "category",
            "canonical_description"
        ]
    ].head(15).to_string(index=False)
)

print()
print("Saved to:", OUTPUT_FILE)