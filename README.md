
# AI-Driven Material Standardization and Harmonization Across CPSEs

**Smart India Hackathon 2026 — Problem Statement 26099**

An AI-driven material intelligence platform for identifying duplicate and equivalent materials across CPSE material masters and mapping them to a common national material standard.

## Problem Statement

Central Public Sector Enterprises (CPSEs) across sectors such as Oil & Gas, Power, Steel, Mining, and Heavy Engineering maintain their material masters independently.

The same or functionally equivalent material may therefore have different:

- Material codes
- Descriptions and naming conventions
- Abbreviations
- Technical specifications
- Units of measurement
- Classifications

This creates duplicate material masters, inconsistent descriptions, difficulty in identifying equivalent materials, limited cross-CPSE procurement visibility, and increased effort for material rationalization and legacy migration.

## Proposed Solution

The system provides an end-to-end material harmonization pipeline:


CPSE Material Records
        ↓
Data Ingestion
        ↓
Normalization
        ↓
Technical Attribute Extraction
        ↓
Candidate Generation
        ↓
Attribute-Aware Matching
        ↓
MATCH / REVIEW / NO_MATCH
        ↓
Human Validation
        ↓
National Material Master
        ↓
Legacy Migration & Analytics


The key approach is to combine **description similarity with technical attribute comparison and conflict detection**, rather than relying only on text similarity.

## Implementation

### 1. Data Foundation

The prototype uses a controlled synthetic dataset representing heterogeneous CPSE material records.

* 300 CPSE material records
* 100 canonical material standards
* 10 material categories
* Multiple CPSE-specific data formats
* Positive matching cases
* Easy negative cases
* Hard negative cases
* Ground-truth labels

Example CPSE formats:


CPSE-A → material_code, description, uom
CPSE-B → item_id, item_name, unit
CPSE-C → mat_no, short_text, base_uom


These different formats are converted into a common internal representation.

### 2. Normalization

Material descriptions are standardized by handling:

* Case variations
* Punctuation
* Separators
* Abbreviations
* Material-grade notation
* Dimension formatting
* Unit notation

For example:


M10 X 50 SS304 HEX BOLT
M10X50 SS304 HEX BOLT
M10-50 SS304 HEX BOLT


are normalized into a consistent representation.

### 3. Technical Attribute Extraction

The system extracts technical specifications from material descriptions, including:


Diameter
Length
Size
Grade
Pressure Class
Schedule
Voltage
Power
Flow Rate
Head
Cable Cores
Cross Section
Bearing Number
Valve Type
Flange Type
Gasket Type
Tool Type
Tool Size


These structured attributes provide additional evidence for material comparison.

### 4. Candidate Generation

Candidate generation performs coarse blocking by material category.


FASTENER → FASTENER
VALVE    → VALVE
PUMP     → PUMP


Description similarity is used as a feature, while technical specifications are evaluated later by the matching engine. This preserves difficult hard-negative cases for detailed evaluation.

### 5. Attribute-Aware Matching

The matching engine combines:


Description Similarity
        +
Technical Attribute Comparison
        +
Critical Attribute Matching
        +
Technical Conflict Detection
        ↓
Confidence Score


For example, two materials may have highly similar descriptions but different pressure classes:


GATE VALVE 150 CLASS
GATE VALVE 300 CLASS


The system detects the technical conflict instead of treating them as equivalent based only on textual similarity.

### 6. Matching Decisions

The system produces three decisions:

**MATCH**
Strong evidence indicates that the materials are equivalent.

**REVIEW**
A potential match exists but requires human validation.

**NO_MATCH**
The evidence indicates that the materials should not be harmonized.

### 7. Harmonization

Matched CPSE materials are mapped to a Common National Material Code while retaining their original CPSE identifiers.


CPSE Material
      ↓
CPSE Material Code
      ↓
Canonical Material
      ↓
Common National Material Code


### 8. Review & Approval

Materials requiring validation are placed into a review queue containing matching evidence, confidence, technical attributes, conflicts, reviewer decisions, comments, and timestamps.

This provides a human-in-the-loop governance mechanism before harmonization and migration.

### 9. Legacy Migration

Harmonization results are converted into migration mappings with statuses such as:


MIGRATION_READY
REVIEW_REQUIRED
BLOCKED


This provides a controlled approach to legacy material-code rationalization.

### 10. Analytics

The platform provides analytics for:

* CPSE-wise material distribution
* Category-wise distribution
* Migration readiness
* Common materials across CPSEs
* Potential material consolidation
* Procurement-related insights

### 11. Auditability

The system maintains traceability of:

* Original CPSE material
* Recommended national material
* Confidence score
* Matching evidence
* Technical conflicts
* Final decision
* Review status
* Reviewer information
* Review timestamp

## Material Categories

The current prototype covers:


BEARING
ELECTRICAL_CABLE
FASTENER
FLANGE
GASKET
INDUSTRIAL_TOOL
MOTOR
PIPE
PUMP
VALVE


## Benchmark Evaluation

The prototype was evaluated using a controlled ground-truth benchmark containing 300 CPSE material records.

| Metric                   | Result |
| ------------------------ | -----: |
| CPSE material records    |    300 |
| Canonical materials      |    100 |
| Correct top-1 mappings   |    300 |
| Top-1 benchmark accuracy |   100% |

### Decision Distribution

| Decision | Records |
| -------- | ------: |
| MATCH    |     269 |
| REVIEW   |      16 |
| NO_MATCH |      15 |

The benchmark produced **300/300 correct top-1 mappings**.

The REVIEW state is intentionally retained so that uncertain cases can be validated by a human instead of being automatically accepted.

> The reported accuracy is based on the controlled synthetic benchmark used for this prototype and is not a claim of production accuracy on real CPSE data.

## Application Modules

The Streamlit application provides:

* **Dashboard** —                 Overall system and harmonization overview
* **Material Matching** —         Material-level matching evidence and decisions
* **Review & Approval** —         Human validation workflow
* **National Material Master** —  Standardized material records and mappings
* **Legacy Migration** —          Migration mappings and readiness
* **Analytics** —                 Material, category, CPSE, and consolidation insights
* **Audit Trail** —               Traceability of harmonization activities

## Technology Stack

| Technology | Purpose                 |
| ---------- | ----------------------- |
| Python     | Core implementation     |
| Pandas     | Data processing         |
| NumPy      | Numerical operations    |
| RapidFuzz  | Text similarity         |
| Streamlit  | Interactive application |
| Plotly     | Data visualization      |

The prototype runs on standard CPU hardware and does not require a GPU or a large language model.

## Project Structure

```text
material-harmonization/
│
├── app.py
├── README.md
├── requirements.txt
│
├── .streamlit/
│   └── config.toml
│
├── data/
│   ├── benchmark/
│   │   ├── canonical_materials.csv
│   │   ├── material_records.csv
│   │   └── match_pairs.csv
│   │
│   └── processed/
│       ├── candidate_pairs.csv
│       ├── evaluation_results.csv
│       ├── final_matches.csv
│       ├── harmonized_material_mapping.csv
│       ├── migration_mapping.csv
│       ├── national_material_master.csv
│       ├── processed_material_records.csv
│       ├── review_queue.csv
│       └── ...
│
└── src/
    ├── normalization.py
    ├── attribute_extraction.py
    ├── candidate_generation.py
    ├── matching_engine.py
    ├── select_best_matches.py
    ├── evaluate_matching.py
    ├── create_harmonized_mapping.py
    ├── create_migration_mapping.py
    ├── create_review_queue.py
    ├── create_review_decisions.py
    ├── create_audit_log.py
    └── ...
```

## Running the Project

### Clone the repository


git clone https://github.com/EmmanuelShaaron/material-harmonization.git
cd material-harmonization


### Create a virtual environment


python -m venv .venv


### Activate the environment on Windows


.venv\Scripts\Activate.ps1


### Install dependencies


pip install -r requirements.txt


### Run the application


streamlit run app.py


## Current Scope

The current implementation demonstrates the complete workflow:


Ingest
→ Normalize
→ Extract Technical Attributes
→ Generate Candidates
→ Match
→ Validate
→ Harmonize
→ Migrate
→ Analyze


The prototype focuses on demonstrating the technical feasibility of material standardization, matching, governance, harmonization, migration, and analytics using a controlled synthetic dataset.

## Future Production Adaptation

A production implementation would require integration with real CPSE material master data and enterprise systems.

Potential extensions include:

* Real CPSE master-data integration
* Enterprise schema adapters
* Domain-specific material taxonomies
* ERP/SAP integration
* Role-based access control
* Production-scale processing
* Advanced ML/NLP models
* Continuous improvement using reviewer feedback
* Enterprise security and governance

## Disclaimer

This project is a prototype developed for **Smart India Hackathon 2026 — Problem Statement 26099**.

The demonstration dataset is synthetic and does not contain confidential CPSE data.

The benchmark results represent performance on the controlled dataset created for this prototype.

Production deployment would require validation against real CPSE material masters, domain-specific business rules, enterprise security requirements, governance policies, and ERP/SAP integration requirements.

