import pandas as pd
from pathlib import Path
from datetime import datetime


# ========================================================
# INPUT / OUTPUT
# ========================================================

INPUT_FILE = "data/processed/migration_mapping.csv"

OUTPUT_FILE = "data/processed/audit_log.csv"


# ========================================================
# LOAD DATA
# ========================================================

migration = pd.read_csv(INPUT_FILE)

print("Records loaded:", len(migration))


# ========================================================
# CREATE AUDIT EVENTS
# ========================================================

audit_records = []

timestamp = datetime.now().strftime(
    "%Y-%m-%d %H:%M:%S"
)


for _, row in migration.iterrows():

    if row["migration_status"] == "MIGRATION_READY":

        action = "AI_RECOMMENDED_MIGRATION"
        result = "PENDING_EXECUTION"

    elif row["migration_status"] == "REVIEW_REQUIRED":

        action = "AI_RECOMMENDED_REVIEW"
        result = "HUMAN_VALIDATION_REQUIRED"

    else:

        action = "AI_BLOCKED_MIGRATION"
        result = "MIGRATION_BLOCKED"


    audit_records.append(
        {
            "timestamp": timestamp,
            "record_id": row["record_id"],
            "cpse": row["cpse"],
            "legacy_material_code": row["cpse_material_code"],
            "national_material_code": row["national_material_code"],
            "action": action,
            "result": result,
            "confidence": row["confidence"],
            "conflict_count": row["conflict_count"],
            "system": "Material Harmonization Engine"
        }
    )


# ========================================================
# CREATE DATAFRAME
# ========================================================

audit_log = pd.DataFrame(audit_records)


# ========================================================
# SAVE
# ========================================================

Path("data/processed").mkdir(
    parents=True,
    exist_ok=True
)

audit_log.to_csv(
    OUTPUT_FILE,
    index=False
)


# ========================================================
# SUMMARY
# ========================================================

print()
print("=" * 60)
print("AUDIT TRAIL")
print("=" * 60)

print("Audit events:", len(audit_log))

print()
print("Actions:")

print(
    audit_log["action"]
    .value_counts()
)

print()
print("Results:")

print(
    audit_log["result"]
    .value_counts()
)

print()
print("Sample audit records:")

print(
    audit_log
    .head(10)
    .to_string(index=False)
)

print()
print("Saved to:", OUTPUT_FILE)