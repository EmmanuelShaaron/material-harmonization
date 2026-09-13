\# AI-Driven Material Standardization and Harmonization Across CPSEs



\## Smart India Hackathon — Problem Statement 26099



An AI-driven material intelligence platform designed to identify duplicate and equivalent materials across CPSE material masters and map them to a common national material standard.



\## Problem



Different CPSEs may maintain similar materials using different material codes, descriptions, specifications, units of measurement, and naming conventions.



This creates:



\- Duplicate material masters

\- Inconsistent descriptions

\- Difficult procurement analysis

\- Poor cross-organization visibility

\- Manual material rationalization effort



\## Proposed Solution



The platform processes CPSE material records through a multi-stage harmonization pipeline:



1\. \*\*Data Ingestion\*\* — Standardizes material records from different CPSE formats.

2\. \*\*Normalization\*\* — Cleans descriptions, abbreviations, units, and naming variations.

3\. \*\*Technical Attribute Extraction\*\* — Extracts specifications such as size, grade, pressure class, voltage, power, flow, and other domain attributes.

4\. \*\*Candidate Generation\*\* — Generates potential matches within the same material category.

5\. \*\*AI Matching Engine\*\* — Combines description similarity with technical attribute comparison and conflict detection.

6\. \*\*Harmonization \& Governance\*\* — Assigns confidence-based decisions: MATCH, REVIEW, or NO\_MATCH.

7\. \*\*National Material Master\*\* — Maps equivalent materials to a Common National Material Code.

8\. \*\*Migration \& Analytics\*\* — Supports legacy-code migration, review workflows, auditability, and procurement insights.



\## Key Features



\- Cross-CPSE material matching

\- Technical attribute-aware matching

\- Hard-conflict detection

\- Confidence-based decision making

\- Human-in-the-loop review

\- Common National Material Code generation

\- Legacy material migration mapping

\- Review queue and approval workflow

\- Audit trail

\- Analytics and procurement intelligence



\## Technology Stack



\- Python

\- Pandas

\- NumPy

\- RapidFuzz

\- Streamlit

\- Plotly



The prototype is designed to run on standard CPU hardware without requiring a GPU or large language model.



\## Prototype Dataset



The current demonstration uses a controlled synthetic benchmark representing CPSE material records across multiple industrial categories.



The benchmark contains:



\- 300 CPSE material records

\- 100 canonical material standards

\- Multiple CPSE data formats

\- Positive and hard-negative matching cases

\- Ground-truth labels for evaluation



The synthetic dataset is used for prototype validation and does not represent confidential CPSE data.



\## Evaluation



The current benchmark achieved:



\- \*\*300/300 correct top-1 material mappings\*\*

\- \*\*100% benchmark top-1 accuracy\*\*



The system also separates automatic matches from cases requiring human review or blocking, rather than relying only on a similarity score.



\## Project Structure



```text

material-harmonization/

│

├── app.py

├── requirements.txt

├── README.md

├── .streamlit/

│   └── config.toml

│

├── data/

│   ├── benchmark/

│   └── processed/

│

└── src/

&#x20;   ├── normalization.py

&#x20;   ├── attribute\_extraction.py

&#x20;   ├── candidate\_generation.py

&#x20;   ├── matching\_engine.py

&#x20;   ├── select\_best\_matches.py

&#x20;   ├── evaluate\_matching.py

&#x20;   └── ...

