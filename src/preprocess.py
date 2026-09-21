"""Clean and encode the UCI CKD CSV dataset."""

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / "data" / "ckd_raw.csv"
CLEAN_PATH = ROOT / "data" / "ckd_clean.csv"


def clean_dataset(input_path: Path = RAW_PATH, output_path: Path = CLEAN_PATH) -> pd.DataFrame:
    frame = pd.read_csv(input_path)
    frame = frame.replace({"?": pd.NA, "": pd.NA})
    frame = frame.dropna(axis=0, thresh=max(1, int(frame.shape[1] * 0.5)))
    target = "class"

    for column in frame.columns:
        if column == target:
            continue
        numeric = pd.to_numeric(frame[column], errors="coerce")
        if numeric.notna().sum() >= frame[column].notna().sum() * 0.8:
            frame[column] = numeric.fillna(numeric.median())
        else:
            mode = frame[column].mode(dropna=True)
            frame[column] = frame[column].fillna(mode.iloc[0] if not mode.empty else "unknown")
            categories = {value: index for index, value in enumerate(sorted(frame[column].unique()))}
            frame[column] = frame[column].map(categories)

    frame[target] = frame[target].astype(str).str.strip().str.lower().map({"ckd": 1, "notckd": 0})
    frame = frame.dropna(subset=[target]).astype({target: int})
    output_path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(output_path, index=False)
    print(f"Saved {len(frame)} cleaned rows to {output_path}")
    return frame


if __name__ == "__main__":
    clean_dataset()
