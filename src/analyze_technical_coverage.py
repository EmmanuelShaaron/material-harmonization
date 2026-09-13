import pandas as pd


# ========================================================
# LOAD MATCHING RESULTS
# ========================================================

df = pd.read_csv(
    "data/processed/matching_results.csv"
)


# ========================================================
# CATEGORY-SPECIFIC CRITICAL ATTRIBUTES
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
# ANALYZE CRITICAL COVERAGE
# ========================================================

coverage_results = []

for _, row in df.iterrows():

    category = str(row["category"]).upper()

    critical = CRITICAL_ATTRIBUTES.get(
        category,
        []
    )

    evidence = []

    try:
        import json
        evidence = json.loads(
            row["attribute_evidence"]
        )
    except Exception:
        pass

    evidence_map = {
        item["attribute"]: item
        for item in evidence
    }

    compared = 0
    matched = 0
    conflicts = 0

    for attribute in critical:

        item = evidence_map.get(attribute)

        if not item:
            continue

        if item["status"] != "NOT_AVAILABLE":

            compared += 1

            if item["status"] == "MATCH":
                matched += 1

            elif item["status"] == "CONFLICT":
                conflicts += 1

    total_critical = len(critical)

    if total_critical > 0:

        coverage = (
            compared /
            total_critical
        ) * 100

    else:

        coverage = 0

    coverage_results.append({
        "record_id": row["record_id"],
        "category": category,
        "confidence": row["confidence"],
        "decision": row["decision"],
        "critical_total": total_critical,
        "critical_compared": compared,
        "critical_matched": matched,
        "critical_conflicts": conflicts,
        "critical_coverage": round(
            coverage,
            2
        )
    })


coverage_df = pd.DataFrame(
    coverage_results
)


# ========================================================
# SUMMARY
# ========================================================

print("=" * 60)
print("CRITICAL ATTRIBUTE COVERAGE ANALYSIS")
print("=" * 60)

print()

print(
    "Average critical coverage:",
    round(
        coverage_df[
            "critical_coverage"
        ].mean(),
        2
    ),
    "%"
)

print()

print("Coverage distribution:")

print(
    coverage_df[
        "critical_coverage"
    ]
    .value_counts()
    .sort_index()
)

print()

print("Low critical coverage cases (<50%):")

low = coverage_df[
    coverage_df[
        "critical_coverage"
    ] < 50
]

print(
    low[
        [
            "record_id",
            "category",
            "confidence",
            "decision",
            "critical_total",
            "critical_compared",
            "critical_matched",
            "critical_conflicts",
            "critical_coverage"
        ]
    ]
    .sort_values(
        "confidence",
        ascending=False
    )
    .head(30)
    .to_string(
        index=False
    )
)

print()

print("High-confidence + low-evidence cases:")

high_low = coverage_df[
    (
        coverage_df["confidence"] >= 85
    )
    &
    (
        coverage_df["critical_coverage"] < 50
    )
]

print(
    high_low[
        [
            "record_id",
            "category",
            "confidence",
            "decision",
            "critical_total",
            "critical_compared",
            "critical_matched",
            "critical_coverage"
        ]
    ]
    .sort_values(
        "confidence",
        ascending=False
    )
    .head(30)
    .to_string(
        index=False
    )
)