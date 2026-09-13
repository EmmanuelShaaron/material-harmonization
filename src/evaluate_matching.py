import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score
# ========================================================
# LOAD DATA
# ========================================================

processed = pd.read_csv(
    "data/processed/processed_material_records.csv"
)

final_matches = pd.read_csv(
    "data/processed/final_matches.csv"
)


# ========================================================
# PREPARE GROUND TRUTH
# ========================================================

processed = processed.reset_index(drop=True)

processed["record_id"] = processed.index

ground_truth = processed[
    [
        "record_id",
        "cpse",
        "original_description",
        "canonical_id",
        "category"
    ]
].rename(
    columns={
        "canonical_id": "true_canonical_id"
    }
)


# ========================================================
# AVOID DUPLICATE COLUMNS
# ========================================================

# final_matches already contains:
# record_id, cpse, original_description

# Therefore only take the ground-truth fields
# that are not already present.

ground_truth = ground_truth[
    [
        "record_id",
        "true_canonical_id",
        "category"
    ]
]


# ========================================================
# MERGE PREDICTIONS WITH GROUND TRUTH
# ========================================================

evaluation = final_matches.merge(
    ground_truth,
    on="record_id",
    how="left",
    suffixes=("", "_truth")
)

# Use ground-truth category
if "category_truth" in evaluation.columns:
    evaluation["category"] = evaluation["category_truth"]
    evaluation.drop(columns=["category_truth"], inplace=True)


# ========================================================
# CORRECTNESS
# ========================================================

evaluation["correct"] = (
    evaluation["predicted_canonical_id"]
    == evaluation["true_canonical_id"]
)


# ========================================================
# TOP-1 ACCURACY
# ========================================================

accuracy = evaluation["correct"].mean()

print("=" * 60)
print("MATCHING ENGINE EVALUATION")
print("=" * 60)

print("\nTotal records:", len(evaluation))

print(
    "Correct predictions:",
    int(evaluation["correct"].sum())
)

print(
    "Incorrect predictions:",
    int((~evaluation["correct"]).sum())
)

print(
    "Top-1 Accuracy:",
    round(accuracy * 100, 2),
    "%"
)


# ========================================================
# DECISION DISTRIBUTION
# ========================================================

print("\nDecision distribution:")

print(
    evaluation["final_decision"]
    .value_counts()
)


# ========================================================
# CORRECTNESS BY DECISION
# ========================================================

print("\nCorrectness by final decision:")

decision_summary = (
    evaluation
    .groupby("final_decision")["correct"]
    .agg(
        total="count",
        correct="sum"
    )
)

decision_summary["accuracy_%"] = (
    decision_summary["correct"]
    / decision_summary["total"]
    * 100
)

print(
    decision_summary.round(2)
)


# ========================================================
# CATEGORY PERFORMANCE
# ========================================================

print("\nCategory performance:")

category_summary = (
    evaluation
    .groupby("category")["correct"]
    .agg(
        total="count",
        correct="sum"
    )
)

category_summary["accuracy_%"] = (
    category_summary["correct"]
    / category_summary["total"]
    * 100
)

print(
    category_summary
    .sort_values("accuracy_%")
    .round(2)
)


# ========================================================
# CPSE PERFORMANCE
# ========================================================

print("\nCPSE performance:")

cpse_summary = (
    evaluation
    .groupby("cpse")["correct"]
    .agg(
        total="count",
        correct="sum"
    )
)

cpse_summary["accuracy_%"] = (
    cpse_summary["correct"]
    / cpse_summary["total"]
    * 100
)

print(
    cpse_summary.round(2)
)


# ========================================================
# INCORRECT PREDICTIONS
# ========================================================

false_matches = evaluation[
    ~evaluation["correct"]
].copy()

print(
    "\nIncorrect predictions:",
    len(false_matches)
)


if len(false_matches) > 0:

    print("\nTop incorrect predictions:")

    columns = [
        "record_id",
        "cpse",
        "original_description",
        "true_canonical_id",
        "predicted_canonical_id",
        "predicted_canonical_description",
        "confidence",
        "confidence_gap",
        "final_decision"
    ]

    print(
        false_matches[
            columns
        ]
        .sort_values(
            "confidence",
            ascending=False
        )
        .head(20)
        .to_string(index=False)
    )


# ========================================================
# CORRECT PREDICTIONS REJECTED BY DECISION LAYER
# ========================================================

rejected_correct = evaluation[
    (evaluation["correct"])
    &
    (evaluation["final_decision"] != "MATCH")
].copy()

print(
    "\nCorrect predictions rejected by decision layer:",
    len(rejected_correct)
)


if len(rejected_correct) > 0:

    print("\nExamples:")

    columns = [
        "record_id",
        "cpse",
        "original_description",
        "true_canonical_id",
        "predicted_canonical_id",
        "confidence",
        "second_best_confidence",
        "confidence_gap",
        "conflict_count",
        "final_decision"
    ]

    print(
        rejected_correct[
            columns
        ]
        .sort_values(
            "confidence",
            ascending=False
        )
        .head(20)
        .to_string(index=False)
    )


# ========================================================
# SAVE
# ========================================================

output_path = (
    "data/processed/evaluation_results.csv"
)

evaluation.to_csv(
    output_path,
    index=False
)

print(
    "\nSaved to:",
    output_path
)