
import pandas as pd
import json

# ========================================================
# LOAD MATCHING RESULTS
# ========================================================

results = pd.read_csv(
    "data/processed/matching_results.csv"
)


# ========================================================
# SORT CANDIDATES
# ========================================================
#
# For every CPSE record:
#   1. Highest confidence = best candidate
#   2. Second highest = runner-up
#
# We use both confidence and technical score so that
# technically stronger candidates are preferred when
# confidence is very close.
# ========================================================

results = results.sort_values(
    by=[
        "record_id",
        "confidence",
        "technical_score",
        "description_score"
    ],
    ascending=[
        True,
        False,
        False,
        False
    ]
)


# ========================================================
# SELECT BEST CANDIDATE FOR EACH RECORD
# ========================================================

best_matches = []

for record_id, group in results.groupby(
    "record_id"
):

    group = group.reset_index(drop=True)

    # ----------------------------------------------------
    # Best candidate
    # ----------------------------------------------------

    best = group.iloc[0]

    # ----------------------------------------------------
    # Second-best candidate
    # ----------------------------------------------------

    if len(group) > 1:

        second = group.iloc[1]

        second_confidence = float(
            second["confidence"]
        )

    else:

        second_confidence = 0

    # ----------------------------------------------------
    # Confidence gap
    # ----------------------------------------------------

    confidence_gap = (
        float(best["confidence"])
        - second_confidence
    )

    # ----------------------------------------------------
    # Final decision
    # ----------------------------------------------------
    #
    # High confidence + clear winner
    #       -> MATCH
    #
    # Good confidence but ambiguous
    #       -> REVIEW
    #
    # Low confidence
    #       -> NO_MATCH
    # ----------------------------------------------------

    best_confidence = float(
        best["confidence"]
    )

    conflict_count = int(
        best["conflict_count"]
    )
    critical_coverage = float(
        best["critical_coverage"]
    )

    critical_conflicts = int(
        best["critical_conflicts"]
    )
    # ----------------------------------------------------
# Decisive technical evidence
# ----------------------------------------------------

    decisive_attributes = {
        "BEARING": ["bearing_number"],
    }

    category = str(best["category"]).strip().upper()

    decisive_match = False

    if category in decisive_attributes:

        evidence = json.loads(
            best["attribute_evidence"]
        )

        for attribute in decisive_attributes[category]:

            for item in evidence:

                if (
                    item["attribute"] == attribute
                    and item["status"] == "MATCH"
                    and item["critical"] is True
                ):
                    decisive_match = True
                    break

            if decisive_match:
                break
        # ----------------------------------------------------
    # Final decision
    # ----------------------------------------------------

    # Rule 1:
    # Multiple critical technical conflicts
    # -> NO_MATCH

    if critical_conflicts >= 2:

        final_decision = "NO_MATCH"


    # Rule 2:
    # One critical conflict means the candidate
    # requires human validation.

    elif critical_conflicts == 1:

        if (
            best_confidence >= 85
            and
            confidence_gap >= 5
        ):

            final_decision = "REVIEW"

        else:

            final_decision = "NO_MATCH"


    # Rule 3:
    # Decisive technical identifier matches exactly
    # -> MATCH

    elif (
        decisive_match
        and
        critical_conflicts == 0
        and
        best_confidence >= 95
    ):

        final_decision = "MATCH"


    # Rule 4:
    # Very high confidence + strong critical evidence
    # + clear enough winner
    # -> MATCH

    elif (
        best_confidence >= 95
        and
        critical_coverage >= 75
        and
        confidence_gap >= 3
    ):

        final_decision = "MATCH"


    # Rule 5:
    # High confidence + reasonable critical evidence
    # + clear winner
    # -> MATCH

    elif (
        best_confidence >= 85
        and
        critical_coverage >= 50
        and
        confidence_gap >= 5
    ):

        final_decision = "MATCH"


    # Rule 6:
    # Plausible candidate but not strong enough
    # for automatic migration
    # -> REVIEW

    elif (
        best_confidence >= 60
        and
        critical_coverage >= 25
        and
        confidence_gap >= 3
    ):

        final_decision = "REVIEW"


    # Rule 7:
    # Insufficient confidence/evidence
    # -> NO_MATCH

    else:

        final_decision = "NO_MATCH"
        # ----------------------------------------------------
        # Store final result
        # ----------------------------------------------------

    best_matches.append({

        "record_id":
            best["record_id"],

        "cpse":
            best["cpse"],

        "original_description":
            best["original_description"],

        "normalized_description":
            best["normalized_description"],

        "category":
            best["category"],


        "predicted_canonical_id":
            best["canonical_id"],

        "predicted_canonical_description":
            best["canonical_description"],

        "description_score":
            best["description_score"],

        "technical_score":
            best["technical_score"],

        "technical_coverage":
            best["technical_coverage"],

        "conflict_count":
            best["conflict_count"],

        "weighted_conflict_score":
            best["weighted_conflict_score"],

        "attribute_evidence":
            best["attribute_evidence"],

        "confidence":
            best_confidence,

        "second_best_confidence":
            second_confidence,

        "confidence_gap":
            round(confidence_gap, 2),
        "critical_coverage": best["critical_coverage"],
        "critical_compared": best["critical_compared"],
        "critical_matches": best["critical_matches"],
        "critical_conflicts": best["critical_conflicts"],
        

        "final_decision":
            final_decision
    })


# ========================================================
# CREATE FINAL DATAFRAME
# ========================================================

final_df = pd.DataFrame(
    best_matches
)


# ========================================================
# SAVE
# ========================================================

output_path = (
    "data/processed/final_matches.csv"
)

final_df.to_csv(
    output_path,
    index=False
)


# ========================================================
# SUMMARY
# ========================================================

print(
    "CPSE records:",
    len(final_df)
)

print(
    "\nFinal decision distribution:"
)

print(
    final_df[
        "final_decision"
    ].value_counts()
)


print(
    "\nAverage confidence:",
    round(
        final_df["confidence"].mean(),
        2
    )
)


print(
    "\nAverage confidence gap:",
    round(
        final_df["confidence_gap"].mean(),
        2
    )
)


# ========================================================
# TOP FINAL MATCHES
# ========================================================

print(
    "\nTop 15 final matches:"
)

print(
    final_df[
        [
            "record_id",
            "cpse",
            "original_description",
            "predicted_canonical_id",
            "predicted_canonical_description",
            "confidence",
            "second_best_confidence",
            "confidence_gap",
            "final_decision"
        ]
    ]
    .sort_values(
        "confidence",
        ascending=False
    )
    .head(15)
    .to_string(index=False)
)


# ========================================================
# AMBIGUOUS CASES
# ========================================================

print(
    "\nMost ambiguous cases:"
)

print(
    final_df[
        [
            "record_id",
            "cpse",
            "original_description",
            "predicted_canonical_id",
            "confidence",
            "second_best_confidence",
            "confidence_gap",
            "final_decision"
        ]
    ]
    .sort_values(
        "confidence_gap",
        ascending=True
    )
    .head(15)
    .to_string(index=False)
)


print(
    "\nSaved to:",
    output_path
)

