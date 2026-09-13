import pandas as pd
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"

review_file = DATA_DIR / "review_queue.csv"
output_file = DATA_DIR / "review_decisions.csv"


# ============================================================
# LOAD REVIEW QUEUE
# ============================================================

review_df = pd.read_csv(review_file)

print(f"Review records loaded: {len(review_df)}")


# ============================================================
# CREATE DECISION COLUMNS
# ============================================================

review_df["decision"] = ""
review_df["reviewer"] = ""
review_df["review_comment"] = ""
review_df["decision_timestamp"] = ""


# ============================================================
# SAVE
# ============================================================

review_df.to_csv(output_file, index=False)

print()
print("=" * 60)
print("REVIEW DECISION STORE")
print("=" * 60)

print(f"Records available for review: {len(review_df)}")

print()
print(f"Saved to: {output_file}")