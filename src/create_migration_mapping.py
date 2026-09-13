import pandas as pd
from pathlib import Path


# ========================================================
# INPUT / OUTPUT
# ========================================================

INPUT_FILE = "data/processed/cpse_material_mapping.csv"

OUTPUT_FILE = "data/processed/migration_mapping.csv"


# ========================================================
# LOAD MAPPING
# ========================================================

mapping = pd.read_csv(INPUT_FILE)

print("Mapping records loaded:", len(mapping))


# ========================================================
# CREATE MIGRATION STATUS
# ========================================================

def get_migration_status(row):

    if row["mapping_status"] == "AUTO_MAPPED":
        return "MIGRATION_READY"

    elif row["mapping_status"] == "PENDING_REVIEW":
        return "REVIEW_REQUIRED"

    else:
        return "BLOCKED"


mapping["migration_status"] = mapping.apply(
    get_migration_status,
    axis=1
)


# ========================================================
# REVIEW FLAG
# ========================================================

mapping["review_required"] = (
    mapping["mapping_status"] != "AUTO_MAPPED"
)


# ========================================================
# MIGRATION ACTION
# ========================================================

def get_migration_action(row):

    if row["migration_status"] == "MIGRATION_READY":
        return "REPLACE_LEGACY_CODE"

    elif row["migration_status"] == "REVIEW_REQUIRED":
        return "VALIDATE_BEFORE_MIGRATION"

    else:
        return "NO_MIGRATION"


mapping["migration_action"] = mapping.apply(
    get_migration_action,
    axis=1
)


# ========================================================
# FINAL MIGRATION TABLE
# ========================================================

migration = mapping[
    [
        "record_id",
        "cpse",
        "cpse_material_code",
        "cpse_description",
        "cpse_uom",
        "national_material_code",
        "canonical_description",
        "category",
        "confidence",
        "confidence_gap",
        "conflict_count",
        "migration_status",
        "review_required",
        "migration_action"
    ]
].copy()


# ========================================================
# SAVE
# ========================================================

Path("data/processed").mkdir(
    parents=True,
    exist_ok=True
)

migration.to_csv(
    OUTPUT_FILE,
    index=False
)


# ========================================================
# SUMMARY
# ========================================================

print()
print("=" * 60)
print("LEGACY MATERIAL MIGRATION")
print("=" * 60)

print("Total legacy records:", len(migration))

print()
print("Migration status:")

print(
    migration["migration_status"]
    .value_counts()
)

print()
print("Migration actions:")

print(
    migration["migration_action"]
    .value_counts()
)

print()
print("Records requiring review:")

print(
    migration["review_required"]
    .value_counts()
)

print()
print("Migration by CPSE:")

print(
    migration
    .groupby(["cpse", "migration_status"])
    .size()
)

print()
print("Sample migration mappings:")

print(
    migration[
        [
            "cpse",
            "cpse_material_code",
            "cpse_description",
            "national_material_code",
            "migration_status"
        ]
    ]
    .head(15)
    .to_string(index=False)
)

print()
print("Saved to:", OUTPUT_FILE)