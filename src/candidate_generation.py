
import pandas as pd
from rapidfuzz.fuzz import token_set_ratio


# ===================
#=====================================
# LOAD DATA
# ========================================================

records = pd.read_csv(
    "data/processed/processed_material_records.csv"
)

canonical = pd.read_csv(
    "data/benchmark/canonical_materials.csv"
)


# ========================================================
# PREPARE DATA
# ========================================================

# Give every CPSE record a stable ID
records = records.reset_index(drop=True)
records["record_id"] = records.index


# ========================================================
# CANDIDATE GENERATION
# ========================================================
#
# IMPORTANT:
# Candidate generation ONLY performs coarse blocking.
#
# It must NOT reject candidates because of:
# - diameter
# - length
# - size
# - grade
# - pressure class
# - schedule
# - etc.
#
# Those conflicts are handled later by the
# matching engine.
# ========================================================

candidates = []

for _, record in records.iterrows():

    # ----------------------------------------------------
    # CATEGORY BLOCKING
    # ----------------------------------------------------
    #
    # Only compare materials belonging to the same
    # broad category.
    #
    # Example:
    # FASTENER -> FASTENER candidates
    # VALVE    -> VALVE candidates
    #
    # This removes obviously unrelated materials while
    # preserving hard negatives.
    # ----------------------------------------------------

    same_category = canonical[
        canonical["category"] == record["category"]
    ]

    for _, material in same_category.iterrows():

        # ------------------------------------------------
        # DESCRIPTION SIMILARITY
        # ------------------------------------------------
        #
        # This is stored as a feature only.
        # It does NOT filter candidates.
        # ------------------------------------------------

        similarity = token_set_ratio(
            str(record["normalized_description"]),
            str(material["canonical_description"])
        )

        candidates.append({
            "record_id": record["record_id"],
            "cpse": record["cpse"],
            "original_description": record["original_description"],
            "normalized_description": record["normalized_description"],

            "canonical_id": material["canonical_id"],
            "canonical_description": material["canonical_description"],

            "category": record["category"],
            "description_similarity": similarity
        })


# ========================================================
# CREATE DATAFRAME
# ========================================================

candidate_df = pd.DataFrame(candidates)


# ========================================================
# SAVE
# ========================================================

output_path = "data/processed/candidate_pairs.csv"

candidate_df.to_csv(
    output_path,
    index=False
)


# ========================================================
# SUMMARY
# ========================================================

print("CPSE records:", len(records))
print("Canonical materials:", len(canonical))
print("Candidate pairs generated:", len(candidate_df))

print(
    "Average candidates per record:",
    round(len(candidate_df) / len(records), 2)
)

print("\nCandidates by category:")

print(
    candidate_df["category"]
    .value_counts()
    .sort_index()
)

print("\nSample candidates:")

print(
    candidate_df[
        [
            "record_id",
            "cpse",
            "original_description",
            "canonical_id",
            "canonical_description",
            "description_similarity"
        ]
    ].head(10).to_string(index=False)
)

print("\nSaved to:", output_path)

