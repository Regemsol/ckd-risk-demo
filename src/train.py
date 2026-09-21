"""Train and evaluate the single KNN CKD classifier."""

from pathlib import Path

import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "ckd_selected.csv"
MODEL_PATH = ROOT / "models" / "knn_ckd.pkl"
TEST_PATH = ROOT / "data" / "ckd_test.csv"


def train_model() -> tuple[Pipeline, pd.DataFrame, pd.Series, pd.DataFrame, pd.Series]:
    frame = pd.read_csv(DATA_PATH)
    features = frame.drop(columns="class")
    target = frame["class"]
    x_train, x_test, y_train, y_test = train_test_split(
        features, target, test_size=0.2, stratify=target, random_state=42
    )
    model = Pipeline([("scale", StandardScaler()), ("knn", KNeighborsClassifier(n_neighbors=5))])
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)
    print(f"Accuracy: {accuracy_score(y_test, predictions):.4f}")
    print(f"Precision: {precision_score(y_test, predictions, zero_division=0):.4f}")
    print(f"Recall: {recall_score(y_test, predictions, zero_division=0):.4f}")
    print(f"F1-score: {f1_score(y_test, predictions, zero_division=0):.4f}")
    print("Confusion matrix:")
    print(confusion_matrix(y_test, predictions))
    print("Classification report:")
    print(classification_report(y_test, predictions, target_names=["not CKD", "CKD"], zero_division=0))
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    pd.concat([x_test.reset_index(drop=True), y_test.reset_index(drop=True).rename("class")], axis=1).to_csv(TEST_PATH, index=False)
    print(f"Saved model to {MODEL_PATH}")
    return model, x_train, y_train, x_test, y_test


if __name__ == "__main__":
    train_model()
