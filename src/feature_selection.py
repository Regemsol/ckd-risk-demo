"""Select the five predictors most correlated with CKD class."""

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
CLEAN_PATH = ROOT / "data" / "ckd_clean.csv"
SELECTED_PATH = ROOT / "data" / "ckd_selected.csv"
FEATURES_PATH = ROOT / "data" / "selected_features.csv"


def select_features(input_path: Path = CLEAN_PATH) -> list[str]:
    frame = pd.read_csv(input_path)
    correlations = frame.drop(columns="class").corrwith(frame["class"]).abs().sort_values(ascending=False)
    selected = correlations.head(5).index.tolist()
    frame[selected + ["class"]].to_csv(SELECTED_PATH, index=False)
    correlations.loc[selected].rename("absolute_correlation").to_csv(FEATURES_PATH, header=True)
    print("Selected features:")
    print(correlations.loc[selected].to_string())
    print(f"Saved reduced dataset to {SELECTED_PATH}")
    return selected


if __name__ == "__main__":
    select_features()
