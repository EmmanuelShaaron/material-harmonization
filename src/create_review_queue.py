import pandas as pd
from pathlib import Path


# ========================================================
# INPUT / OUTPUT
# ========================================================

INPUT_FILE = "data/processed/migration_mapping.csv"

OUTPUT_FILE = "data/processed/review_queue.csv"


# ========================================================
# LOAD MIGRATION DATA
# ========================================================

migration = pd.read_csv(INPUT_FILE)

print("Migration records loaded:", len(migration))


# ========================================================
# SELECT RECORDS REQUIRING HUMAN REVIEW
# ========================================================

review_queue = migration[
    migration["review_required"] == True
].copy()


# ========================================================
# CREATE REVIEW FIELDS
# ========================================================

review_queue["review_status"] = "PENDING"

review_queue["reviewer"] = ""

review_queue["review_comment"] = ""

review_queue["review_timestamp"] = ""


# ========================================================
# REVIEW PRIORITY
# ========================================================

def calculate_priority(row):

    if row["migration_status"] == "REVIEW_REQUIRED":
        return "HIGH"

    elif row["migration_status"] == "BLOCKED":
        return "CRITICAL"

    else:
        return "LOW"


review_queue["priority"] = review_queue.apply(
    calculate_priority,
    axis=1
)


# ========================================================
# REORDER COLUMNS
# ========================================================

review_queue = review_queue[
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
        "priority",
        "review_status",
        "reviewer",
        "review_comment",
        "review_timestamp"
    ]
]


# ========================================================
# SAVE
# ========================================================

Path("data/processed").mkdir(
    parents=True,
    exist_ok=True
)

review_queue.to_csv(
    OUTPUT_FILE,
    index=False
)


# ========================================================
# SUMMARY
# ========================================================

print()
print("=" * 60)
print("HUMAN REVIEW QUEUE")
print("=" * 60)

print("Records requiring review:", len(review_queue))

print()
print("Priority:")
print(
    review_queue["priority"]
    .value_counts()
)

print()
print("Review status:")
print(
    review_queue["review_status"]
    .value_counts()
)

print()
print("Review queue:")

print(
    review_queue[
        [
            "record_id",
            "cpse",
            "cpse_material_code",
            "cpse_description",
            "national_material_code",
            "confidence",
            "priority"
        ]
    ]
    .to_string(index=False)
)

print()
print("Saved to:", OUTPUT_FILE)