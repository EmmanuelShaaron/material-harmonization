import pandas as pd
import random
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

random.seed(42)

INPUT_FILE = Path("data/benchmark/canonical_materials.csv")
OUTPUT_FILE = Path("data/benchmark/match_pairs.csv")


# ============================================================
# LOAD DATA
# ============================================================

df = pd.read_csv(INPUT_FILE)

print("=" * 60)
print("CREATING GROUND TRUTH MATCH PAIRS")
print("=" * 60)

print(f"Canonical materials loaded: {len(df)}")


# ============================================================
# STORE PAIRS
# ============================================================

pairs = []


# ============================================================
# 1. POSITIVE PAIRS
# ============================================================
# Same canonical material = MATCH
#
# We create multiple positive examples for every material.
# ============================================================

for canonical_id in df["canonical_id"]:

    # Same material compared with itself
    pairs.append({
        "material_a": canonical_id,
        "material_b": canonical_id,
        "label": 1,
        "pair_type": "POSITIVE"
    })


# ============================================================
# 2. EASY NEGATIVES
# ============================================================
# Different categories = clearly different materials.
# ============================================================

for _ in range(150):

    row_a, row_b = df.sample(
        2,
        random_state=random.randint(1, 100000)
    ).itertuples(index=False)

    if row_a.category != row_b.category:

        pairs.append({
            "material_a": row_a.canonical_id,
            "material_b": row_b.canonical_id,
            "label": 0,
            "pair_type": "EASY_NEGATIVE"
        })


# ============================================================
# 3. HARD NEGATIVES
# ============================================================
# Same category + similar technical properties.
#
# These are VERY important.
#
# Example:
# M10 X 50 SS304
# M12 X 50 SS304
#
# Text looks extremely similar, but diameter differs.
# ============================================================

def technical_similarity(row_a, row_b):

    score = 0

    # Same category
    if row_a["category"] == row_b["category"]:
        score += 3

    # Same material
    if pd.notna(row_a["material"]) and pd.notna(row_b["material"]):
        if row_a["material"] == row_b["material"]:
            score += 2

    # Same grade
    if pd.notna(row_a["grade"]) and pd.notna(row_b["grade"]):
        if row_a["grade"] == row_b["grade"]:
            score += 2

    # Same size
    if pd.notna(row_a["size_in"]) and pd.notna(row_b["size_in"]):
        if row_a["size_in"] == row_b["size_in"]:
            score += 2

    # Same diameter
    if pd.notna(row_a["diameter_mm"]) and pd.notna(row_b["diameter_mm"]):
        if row_a["diameter_mm"] == row_b["diameter_mm"]:
            score += 2

    # Same pressure
    if pd.notna(row_a["pressure_class"]) and pd.notna(row_b["pressure_class"]):
        if row_a["pressure_class"] == row_b["pressure_class"]:
            score += 2

    # Same schedule
    if pd.notna(row_a["schedule"]) and pd.notna(row_b["schedule"]):
        if row_a["schedule"] == row_b["schedule"]:
            score += 2

    return score


# Generate candidate pairs
candidate_pairs = []

for i in range(len(df)):

    for j in range(i + 1, len(df)):

        row_a = df.iloc[i]
        row_b = df.iloc[j]

        score = technical_similarity(row_a, row_b)

        # Similar enough to be a challenging negative
        if score >= 5:

            candidate_pairs.append({
                "material_a": row_a["canonical_id"],
                "material_b": row_b["canonical_id"],
                "label": 0,
                "pair_type": "HARD_NEGATIVE"
            })


# Remove duplicates
hard_negative_df = pd.DataFrame(candidate_pairs)

if not hard_negative_df.empty:

    hard_negative_df = hard_negative_df.drop_duplicates(
        subset=["material_a", "material_b"]
    )

    # Limit to a manageable number
    hard_negative_df = hard_negative_df.sample(
        n=min(150, len(hard_negative_df)),
        random_state=42
    )

    pairs.extend(
        hard_negative_df.to_dict("records")
    )


# ============================================================
# CREATE DATAFRAME
# ============================================================

pairs_df = pd.DataFrame(pairs)


# ============================================================
# REMOVE DUPLICATE PAIRS
# ============================================================

pairs_df["pair_key"] = pairs_df.apply(
    lambda row: "_".join(
        sorted([
            row["material_a"],
            row["material_b"]
        ])
    ),
    axis=1
)

pairs_df = pairs_df.drop_duplicates(
    subset=["pair_key"]
)

pairs_df = pairs_df.drop(
    columns=["pair_key"]
)


# ============================================================
# SHUFFLE
# ============================================================

pairs_df = pairs_df.sample(
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

pairs_df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# REPORT
# ============================================================

print("\n" + "=" * 60)
print("GROUND TRUTH CREATION COMPLETE")
print("=" * 60)

print(f"Total pairs: {len(pairs_df)}")

print("\nPair distribution:")
print(
    pairs_df["pair_type"].value_counts()
)

print("\nLabel distribution:")
print(
    pairs_df["label"].value_counts()
)

print("\nSample pairs:")

print(
    pairs_df.head(20).to_string(index=False)
)

print("\n" + "=" * 60)
print(f"Saved to: {OUTPUT_FILE}")
print("=" * 60)