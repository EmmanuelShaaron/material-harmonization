import pandas as pd
import numpy as np
from rapidfuzz.fuzz import token_set_ratio
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)

# ========================================================
# PATHS
# ========================================================

CANONICAL_FILE = "data/benchmark/canonical_materials.csv"
BENCHMARK_FILE = "data/benchmark/match_pairs.csv"

OUTPUT_FILE = "data/processed/benchmark_evaluation.csv"


# ========================================================
# LOAD DATA
# ========================================================

canonical = pd.read_csv(CANONICAL_FILE)
benchmark = pd.read_csv(BENCHMARK_FILE)

print("=" * 70)
print("NATIONAL MATERIAL HARMONIZATION")
print("BENCHMARK EVALUATION")
print("=" * 70)

print("\nCanonical materials:", len(canonical))
print("Benchmark pairs:", len(benchmark))


# ========================================================
# TECHNICAL ATTRIBUTES
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
# ATTRIBUTE WEIGHTS
# ========================================================

ATTRIBUTE_WEIGHTS = {
    "diameter_mm": 5,
    "length_mm": 4,
    "size_in": 5,
    "grade": 5,
    "pressure_class": 5,
    "schedule": 5,
    "voltage_v": 5,
    "power_kw": 5,
    "flow_rate_m3h": 5,
    "head_m": 5,
    "cores": 5,
    "cross_section_mm2": 5,
    "bearing_number": 8,
    "valve_type": 6,
    "flange_type": 6,
    "gasket_type": 6,
    "tool_type": 6,
    "tool_size_mm": 5,
}


# ========================================================
# HELPERS
# ========================================================

def is_valid(value):

    if pd.isna(value):
        return False

    if str(value).strip() == "":
        return False

    return True


def compare_attributes(material_a, material_b):

    total_weight = 0
    matching_weight = 0

    conflicts = 0
    compared = 0
    matching = 0

    weighted_conflict_score = 0

    numeric_attributes = [
        "diameter_mm",
        "length_mm",
        "size_in",
        "pressure_class",
        "schedule",
        "voltage_v",
        "power_kw",
        "flow_rate_m3h",
        "head_m",
        "cores",
        "cross_section_mm2",
        "bearing_number",
        "tool_size_mm",
    ]

    for attribute in TECHNICAL_ATTRIBUTES:

        value_a = material_a.get(attribute)
        value_b = material_b.get(attribute)

        # Missing information cannot be compared
        if not is_valid(value_a) or not is_valid(value_b):
            continue

        compared += 1

        weight = ATTRIBUTE_WEIGHTS.get(
            attribute,
            1
        )

        total_weight += weight

        # ------------------------------------------------
        # Numeric comparison
        # ------------------------------------------------

        if attribute in numeric_attributes:

            try:

                number_a = float(value_a)
                number_b = float(value_b)

                if np.isclose(
                    number_a,
                    number_b,
                    rtol=0.01,
                    atol=0.01
                ):

                    matching += 1
                    matching_weight += weight

                else:

                    conflicts += 1
                    weighted_conflict_score += weight

            except (ValueError, TypeError):

                if str(value_a).upper() == str(value_b).upper():

                    matching += 1
                    matching_weight += weight

                else:

                    conflicts += 1
                    weighted_conflict_score += weight

        # ------------------------------------------------
        # Text comparison
        # ------------------------------------------------

        else:

            text_a = str(value_a).strip().upper()
            text_b = str(value_b).strip().upper()

            if text_a == text_b:

                matching += 1
                matching_weight += weight

            else:

                conflicts += 1
                weighted_conflict_score += weight

    if total_weight == 0:

        technical_score = 0

    else:

        technical_score = (
            matching_weight /
            total_weight
        ) * 100

    return (
        technical_score,
        conflicts,
        compared,
        matching,
        weighted_conflict_score
    )


# ========================================================
# SCORE ONE MATERIAL PAIR
# ========================================================

def score_pair(material_a, material_b):

    # ----------------------------------------------------
    # Description similarity
    # ----------------------------------------------------

    description_a = str(
        material_a["canonical_description"]
    )

    description_b = str(
        material_b["canonical_description"]
    )

    description_score = token_set_ratio(
        description_a,
        description_b
    )

    # ----------------------------------------------------
    # Technical comparison
    # ----------------------------------------------------

    (
        technical_score,
        conflict_count,
        compared_attributes,
        matching_attributes,
        weighted_conflict_score
    ) = compare_attributes(
        material_a,
        material_b
    )

    # ----------------------------------------------------
    # Confidence
    # ----------------------------------------------------

    if compared_attributes == 0:

        confidence = (
            description_score * 0.45
        )

    else:

        confidence = (
            description_score * 0.45
            +
            technical_score * 0.55
        )

    # ----------------------------------------------------
    # Conflict penalty
    # ----------------------------------------------------

    if weighted_conflict_score >= 10:

        confidence -= 30

    elif weighted_conflict_score >= 5:

        confidence -= 18

    elif weighted_conflict_score > 0:

        confidence -= 8

    confidence = max(
        0,
        min(100, confidence)
    )

    return {
        "description_score": round(
            description_score,
            2
        ),

        "technical_score": round(
            technical_score,
            2
        ),

        "compared_attributes": compared_attributes,

        "matching_attributes": matching_attributes,

        "conflict_count": conflict_count,

        "weighted_conflict_score": weighted_conflict_score,

        "confidence": round(
            confidence,
            2
        )
    }


# ========================================================
# EVALUATE ALL BENCHMARK PAIRS
# ========================================================

results = []

for _, pair in benchmark.iterrows():

    material_a_id = pair["material_a"]
    material_b_id = pair["material_b"]

    material_a = canonical[
        canonical["canonical_id"] == material_a_id
    ]

    material_b = canonical[
        canonical["canonical_id"] == material_b_id
    ]

    if material_a.empty or material_b.empty:
        continue

    material_a = material_a.iloc[0]
    material_b = material_b.iloc[0]

    scores = score_pair(
        material_a,
        material_b
    )

    result = {
        "material_a": material_a_id,
        "material_b": material_b_id,
        "label": int(pair["label"]),
        "pair_type": pair["pair_type"]
    }

    result.update(scores)

    results.append(result)


evaluation = pd.DataFrame(results)


# ========================================================
# DECISION THRESHOLD
# ========================================================

# For benchmark evaluation:
#
# confidence >= 70 AND no technical conflicts
#     -> predicted MATCH
#
# otherwise
#     -> predicted NON-MATCH
#
# This evaluates the scoring engine independently
# from the top-1 candidate selector.

evaluation["predicted_match"] = (
    (evaluation["confidence"] >= 70)
    &
    (evaluation["conflict_count"] == 0)
).astype(int)


# ========================================================
# OVERALL METRICS
# ========================================================

y_true = evaluation["label"]
y_pred = evaluation["predicted_match"]

accuracy = (
    y_true == y_pred
).mean() * 100

precision = precision_score(
    y_true,
    y_pred,
    zero_division=0
) * 100

recall = recall_score(
    y_true,
    y_pred,
    zero_division=0
) * 100

f1 = f1_score(
    y_true,
    y_pred,
    zero_division=0
) * 100


print("\n" + "-" * 70)
print("OVERALL PERFORMANCE")
print("-" * 70)

print(f"Accuracy  : {accuracy:.2f}%")
print(f"Precision : {precision:.2f}%")
print(f"Recall    : {recall:.2f}%")
print(f"F1 Score  : {f1:.2f}%")


# ========================================================
# CONFUSION MATRIX
# ========================================================

cm = confusion_matrix(
    y_true,
    y_pred
)

print("\n" + "-" * 70)
print("CONFUSION MATRIX")
print("-" * 70)

print(
    "                 Predicted"
)

print(
    "                 NON-MATCH  MATCH"
)

print(
    f"Actual NON-MATCH  {cm[0][0]:>8} {cm[0][1]:>6}"
)

print(
    f"Actual MATCH      {cm[1][0]:>8} {cm[1][1]:>6}"
)


# ========================================================
# PAIR-TYPE PERFORMANCE
# ========================================================

print("\n" + "-" * 70)
print("PAIR-TYPE PERFORMANCE")
print("-" * 70)

pair_summary = []

for pair_type, group in evaluation.groupby(
    "pair_type"
):

    pair_accuracy = (
        group["label"]
        ==
        group["predicted_match"]
    ).mean() * 100

    pair_summary.append({
        "Pair Type": pair_type,
        "Records": len(group),
        "Accuracy": round(
            pair_accuracy,
            2
        )
    })

    print(
        f"{pair_type:<20}"
        f"{len(group):>6} pairs    "
        f"{pair_accuracy:>7.2f}%"
    )


# ========================================================
# POSITIVE MATCH PERFORMANCE
# ========================================================

positive = evaluation[
    evaluation["pair_type"] == "POSITIVE"
]

positive_correct = (
    positive["predicted_match"] == 1
).sum()

positive_recall = (
    positive_correct /
    len(positive) *
    100
)

print("\n" + "-" * 70)
print("POSITIVE PAIR DETECTION")
print("-" * 70)

print(
    f"Positive pairs        : {len(positive)}"
)

print(
    f"Correctly identified   : {positive_correct}"
)

print(
    f"Positive recall       : {positive_recall:.2f}%"
)


# ========================================================
# EASY NEGATIVE PERFORMANCE
# ========================================================

easy_negative = evaluation[
    evaluation["pair_type"] == "EASY_NEGATIVE"
]

easy_correct = (
    easy_negative["predicted_match"] == 0
).sum()

easy_detection = (
    easy_correct /
    len(easy_negative) *
    100
)

print("\n" + "-" * 70)
print("EASY NEGATIVE DETECTION")
print("-" * 70)

print(
    f"Easy negative pairs    : {len(easy_negative)}"
)

print(
    f"Correctly rejected    : {easy_correct}"
)

print(
    f"Detection rate        : {easy_detection:.2f}%"
)


# ========================================================
# HARD NEGATIVE PERFORMANCE
# ========================================================

hard_negative = evaluation[
    evaluation["pair_type"] == "HARD_NEGATIVE"
]

hard_correct = (
    hard_negative["predicted_match"] == 0
).sum()

hard_detection = (
    hard_correct /
    len(hard_negative) *
    100
)

print("\n" + "-" * 70)
print("HARD NEGATIVE DETECTION")
print("-" * 70)

print(
    f"Hard negative pairs    : {len(hard_negative)}"
)

print(
    f"Correctly rejected    : {hard_correct}"
)

print(
    f"Detection rate        : {hard_detection:.2f}%"
)


# ========================================================
# TECHNICAL CONFLICT ANALYSIS
# ========================================================

conflict_pairs = evaluation[
    evaluation["conflict_count"] > 0
]

correct_conflict_rejections = conflict_pairs[
    conflict_pairs["predicted_match"] == 0
]

print("\n" + "-" * 70)
print("TECHNICAL CONFLICT ANALYSIS")
print("-" * 70)

print(
    "Pairs with technical conflicts:",
    len(conflict_pairs)
)

print(
    "Correctly rejected due to conflicts:",
    len(correct_conflict_rejections)
)


# ========================================================
# FALSE MATCHES
# ========================================================

false_matches = evaluation[
    (evaluation["label"] == 0)
    &
    (evaluation["predicted_match"] == 1)
]

print("\n" + "-" * 70)
print("FALSE MATCHES")
print("-" * 70)

print(
    "Incorrectly accepted negative pairs:",
    len(false_matches)
)

if len(false_matches) > 0:

    print(
        false_matches[
            [
                "material_a",
                "material_b",
                "pair_type",
                "description_score",
                "technical_score",
                "conflict_count",
                "confidence"
            ]
        ]
        .sort_values(
            "confidence",
            ascending=False
        )
        .head(20)
        .to_string(index=False)
    )


# ========================================================
# MISSED POSITIVE MATCHES
# ========================================================

missed_positive = evaluation[
    (evaluation["label"] == 1)
    &
    (evaluation["predicted_match"] == 0)
]

print("\n" + "-" * 70)
print("MISSED POSITIVE MATCHES")
print("-" * 70)

print(
    "Positive pairs rejected:",
    len(missed_positive)
)

if len(missed_positive) > 0:

    print(
        missed_positive[
            [
                "material_a",
                "material_b",
                "description_score",
                "technical_score",
                "conflict_count",
                "confidence"
            ]
        ]
        .sort_values(
            "confidence",
            ascending=False
        )
        .head(20)
        .to_string(index=False)
    )


# ========================================================
# SAVE RESULTS
# ========================================================

evaluation.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\n" + "=" * 70)

print(
    "Saved benchmark evaluation to:",
    OUTPUT_FILE
)

print("=" * 70)