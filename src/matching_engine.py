import pandas as pd
import numpy as np
import json


# ========================================================
# LOAD DATA
# ========================================================

records = pd.read_csv(
    "data/processed/processed_material_records.csv"
)

canonical = pd.read_csv(
    "data/benchmark/canonical_materials.csv"
)

candidates = pd.read_csv(
    "data/processed/candidate_pairs.csv"
)

# Recreate the same record IDs used by candidate_generation.py
records = records.reset_index(drop=True)
records["record_id"] = records.index


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
# CATEGORY-SPECIFIC CRITICAL ATTRIBUTES
# ========================================================
#
# These attributes define the identity of a material
# much more strongly than generic description similarity.
# ========================================================

CRITICAL_ATTRIBUTES = {

    "FASTENER": [
        "diameter_mm",
        "length_mm",
        "grade",
    ],

    "BEARING": [
        "bearing_number",
    ],

    "VALVE": [
        "size_in",
        "grade",
        "pressure_class",
        "valve_type",
    ],

    "PIPE": [
        "size_in",
        "grade",
        "schedule",
    ],

    "FLANGE": [
        "size_in",
        "grade",
        "pressure_class",
        "flange_type",
    ],

    "GASKET": [
        "size_in",
        "pressure_class",
        "gasket_type",
    ],

    "ELECTRICAL_CABLE": [
        "cores",
        "cross_section_mm2",
        "voltage_v",
    ],

    "MOTOR": [
        "power_kw",
        "voltage_v",
    ],

    "PUMP": [
        "flow_rate_m3h",
        "head_m",
        "power_kw",
    ],

    "INDUSTRIAL_TOOL": [
        "tool_type",
        "tool_size_mm",
        "power_kw",
    ],
}


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
# NUMERIC ATTRIBUTES
# ========================================================

NUMERIC_ATTRIBUTES = [
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


# ========================================================
# HELPER
# ========================================================

def is_valid(value):

    if pd.isna(value):
        return False

    if str(value).strip() == "":
        return False

    return True


# ========================================================
# ATTRIBUTE COMPARISON
# ========================================================

def compare_attributes(record, material, category):

    total_weight = 0
    matching_weight = 0

    conflicts = 0
    compared = 0
    matches = 0

    weighted_conflict_score = 0

    critical_compared = 0
    critical_matches = 0
    critical_conflicts = 0

    critical_attributes = CRITICAL_ATTRIBUTES.get(
        category,
        []
        )
    critical_total = len(critical_attributes)
    # ------------------------------------------------
    # ATTRIBUTE-LEVEL EXPLAINABILITY
    # ------------------------------------------------

    attribute_evidence = []

    for attribute in TECHNICAL_ATTRIBUTES:

        record_value = record.get(attribute)
        material_value = material.get(attribute)

        is_critical = attribute in critical_attributes

        # ------------------------------------------------
        # Missing information
        # ------------------------------------------------

        if not is_valid(record_value) or not is_valid(material_value):

            attribute_evidence.append({
                "attribute": attribute,
                "record_value": (
                    None
                    if not is_valid(record_value)
                    else str(record_value)
                ),
                "canonical_value": (
                    None
                    if not is_valid(material_value)
                    else str(material_value)
                ),
                "status": "NOT_AVAILABLE",
                "critical": is_critical
            })

            continue

        compared += 1

        weight = ATTRIBUTE_WEIGHTS.get(
            attribute,
            1
        )

        total_weight += weight

        if is_critical:
            critical_compared += 1

        # ------------------------------------------------
        # Compare numeric attributes
        # ------------------------------------------------

        if attribute in NUMERIC_ATTRIBUTES:

            try:

                record_num = float(record_value)
                material_num = float(material_value)

                same = np.isclose(
                    record_num,
                    material_num,
                    rtol=0.01,
                    atol=0.01
                )

            except (ValueError, TypeError):

                same = (
                    str(record_value).strip().upper()
                    ==
                    str(material_value).strip().upper()
                )

        # ------------------------------------------------
        # Compare text attributes
        # ------------------------------------------------

        else:

            same = (
                str(record_value).strip().upper()
                ==
                str(material_value).strip().upper()
            )

        # ------------------------------------------------
        # MATCH
        # ------------------------------------------------

        if same:

            matches += 1
            matching_weight += weight

            if is_critical:
                critical_matches += 1

            attribute_evidence.append({
                "attribute": attribute,
                "record_value": str(record_value),
                "canonical_value": str(material_value),
                "status": "MATCH",
                "critical": is_critical
            })

        # ------------------------------------------------
        # CONFLICT
        # ------------------------------------------------

        else:

            conflicts += 1
            weighted_conflict_score += weight

            if is_critical:
                critical_conflicts += 1

            attribute_evidence.append({
                "attribute": attribute,
                "record_value": str(record_value),
                "canonical_value": str(material_value),
                "status": "CONFLICT",
                "critical": is_critical
            })

    # ----------------------------------------------------
    # Technical score
    # ----------------------------------------------------

    if total_weight == 0:

        technical_score = 0

    else:

        technical_score = (
            matching_weight /
            total_weight
        ) * 100

    # ----------------------------------------------------
    # Critical attribute score
    # ----------------------------------------------------

    if critical_compared == 0:

        critical_score = 0

    else:

        critical_score = (
            critical_matches /
            critical_compared
        ) * 100


    # ----------------------------------------------------
    # Critical evidence coverage
    # ----------------------------------------------------
    #
    # Measures how much of the category-specific
    # critical information is actually available.
    #
    # Example:
    # VALVE has 4 critical attributes.
    # If only 1 is available:
    # 1 / 4 = 25% coverage.
    #
    # Missing information is NOT treated as a conflict.
    # ----------------------------------------------------

    if critical_total == 0:

        critical_coverage = 0

    else:

        critical_coverage = (
            critical_compared /
            critical_total
        ) * 100

    return (
        technical_score,
        conflicts,
        compared,
        matches,
        weighted_conflict_score,
        critical_compared,
        critical_matches,
        critical_conflicts,
        critical_score,
        critical_coverage,
        attribute_evidence
    )

# ========================================================
# DESCRIPTION SCORE
# ========================================================

def get_description_score(candidate):

    value = candidate["description_similarity"]

    if pd.isna(value):
        return 0

    return float(value)


# ========================================================
# MATCHING
# ========================================================

results = []


for _, candidate in candidates.iterrows():

    record_id = int(candidate["record_id"])
    canonical_id = candidate["canonical_id"]

    # ----------------------------------------------------
    # Retrieve record
    # ----------------------------------------------------

    record = records[
        records["record_id"] == record_id
    ]

    material = canonical[
        canonical["canonical_id"] == canonical_id
    ]

    if record.empty or material.empty:
        continue

    record = record.iloc[0]
    material = material.iloc[0]

    category = str(
        candidate["category"]
    ).strip().upper()

    # ----------------------------------------------------
    # Description similarity
    # ----------------------------------------------------

    description_score = get_description_score(
        candidate
    )

    # ----------------------------------------------------
    # Technical comparison
    # ----------------------------------------------------

    (
        technical_score,
        conflict_count,
        compared_attributes,
        matching_attributes,
        weighted_conflict_score,
        critical_compared,
        critical_matches,
        critical_conflicts,
        critical_score,
        critical_coverage,

        attribute_evidence

    ) = compare_attributes(
        record,
        material,
        category
    )

    # ----------------------------------------------------
    # Technical coverage
    # ----------------------------------------------------

    if compared_attributes == 0:

        technical_coverage = 0

    else:

        technical_coverage = (
            compared_attributes /
            len(TECHNICAL_ATTRIBUTES)
        ) * 100

    # ----------------------------------------------------
    # CONFIDENCE
    # ----------------------------------------------------
    #
    # Description = 30%
    # Technical = 70%
    #
    # Technical information is more important because
    # materials must be functionally/technically equivalent.
    # ----------------------------------------------------

    if compared_attributes == 0:

        confidence = description_score * 0.30

    else:

        confidence = (
            description_score * 0.30
            +
            technical_score * 0.70
        )

    # ----------------------------------------------------
    # CRITICAL ATTRIBUTE BOOST
    # ----------------------------------------------------
    #
    # When the critical attributes agree, increase
    # confidence slightly.
    # ----------------------------------------------------

    if critical_compared > 0:

        confidence = (
            confidence * 0.70
            +
            critical_score * 0.30
        )

    # ----------------------------------------------------
    # CRITICAL ATTRIBUTE CONFLICT
    # ----------------------------------------------------
    #
    # A critical technical mismatch is much more serious
    # than a generic description mismatch.
    # ----------------------------------------------------

    if critical_conflicts >= 2:

        confidence -= 35

    elif critical_conflicts == 1:

        confidence -= 20

    # ----------------------------------------------------
    # Additional technical conflict penalty
    # ----------------------------------------------------

    if weighted_conflict_score >= 10:

        confidence -= 15

    elif weighted_conflict_score >= 5:

        confidence -= 8

    elif weighted_conflict_score > 0:

        confidence -= 3

    # ----------------------------------------------------
    # Clamp confidence
    # ----------------------------------------------------

    confidence = max(
        0,
        min(100, confidence)
    )

    # ----------------------------------------------------
    # DECISION
    # ----------------------------------------------------

    if critical_conflicts >= 2:

        decision = "NO_MATCH"

    elif critical_conflicts == 1 and confidence < 75:

        decision = "NO_MATCH"

    elif confidence >= 85:

        decision = "MATCH"

    elif confidence >= 60:

        decision = "REVIEW"

    else:

        decision = "NO_MATCH"

    # ----------------------------------------------------
    # STORE RESULT
    # ----------------------------------------------------

    results.append({

        "record_id":
            record_id,

        "cpse":
            candidate["cpse"],

        "original_description":
            candidate["original_description"],

        "normalized_description":
            candidate["normalized_description"],

        "canonical_id":
            canonical_id,

        "canonical_description":
            candidate["canonical_description"],

        "category":
            category,

        "description_score":
            round(
                description_score,
                2
            ),

        "technical_score":
            round(
                technical_score,
                2
            ),

        "technical_coverage":
            round(
                technical_coverage,
                2
            ),

        "compared_attributes":
            compared_attributes,

        "matching_attributes":
            matching_attributes,

        "critical_compared":
            critical_compared,

        "critical_matches":
            critical_matches,

        "critical_conflicts":
            critical_conflicts,

        "critical_score":
            round(
                critical_score,
                2
            ),
        "critical_coverage":
            round(
                critical_coverage,
                2
            ),

        "attribute_evidence":
            json.dumps(
                attribute_evidence
            ),
        "conflict_count":
            conflict_count,

        "weighted_conflict_score":
            weighted_conflict_score,

        "confidence":
            round(
                confidence,
                2
            ),

        "decision":
            decision
    })


# ========================================================
# SAVE RESULTS
# ========================================================

results_df = pd.DataFrame(results)

output_path = (
    "data/processed/matching_results.csv"
)

results_df.to_csv(
    output_path,
    index=False
)


# ========================================================
# SUMMARY
# ========================================================

print(
    "Candidate pairs:",
    len(candidates)
)

print(
    "\nDecision distribution:"
)

print(
    results_df[
        "decision"
    ].value_counts()
)

print(
    "\nAverage confidence:",
    round(
        results_df[
            "confidence"
        ].mean(),
        2
    )
)

print(
    "Maximum confidence:",
    round(
        results_df[
            "confidence"
        ].max(),
        2
    )
)

print(
    "\nConflict statistics:"
)

print(
    results_df[
        "conflict_count"
    ]
    .value_counts()
    .sort_index()
)

print(
    "\nCritical conflict statistics:"
)

print(
    results_df[
        "critical_conflicts"
    ]
    .value_counts()
    .sort_index()
)


# ========================================================
# SHOW TOP MATCHES
# ========================================================

print(
    "\nTop 15 results:"
)

print(
    results_df[
        [
            "record_id",
            "cpse",
            "original_description",
            "canonical_id",
            "canonical_description",
            "description_score",
            "technical_score",
            "critical_score",
            "critical_conflicts",
            "confidence",
            "decision"
        ]
    ]
    .sort_values(
        "confidence",
        ascending=False
    )
    .head(15)
    .to_string(
        index=False
    )
)


# ========================================================
# SHOW CRITICAL CONFLICTS
# ========================================================

critical_conflicts_df = results_df[
    results_df[
        "critical_conflicts"
    ] > 0
]

print(
    "\nExample critical technical conflicts:"
)

if len(critical_conflicts_df) > 0:

    print(
        critical_conflicts_df[
            [
                "original_description",
                "canonical_id",
                "canonical_description",
                "category",
                "technical_score",
                "critical_score",
                "critical_conflicts",
                "confidence",
                "decision"
            ]
        ]
        .head(15)
        .to_string(
            index=False
        )
    )

else:

    print(
        "No critical technical conflicts detected."
    )


print(
    "\nSaved to:",
    output_path
)