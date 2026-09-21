# CKD Risk Demo: How the Project Works

## 1. What This Project Does

This project is a small machine-learning demonstration for predicting chronic kidney disease (CKD) risk. It uses medical laboratory and patient-history values from the UCI Chronic Kidney Disease dataset and predicts one of two labels:

- `CKD`: the model predicts that the patient belongs to the CKD class.
- `Not CKD`: the model predicts that the patient belongs to the non-CKD class.

This is an academic screening demonstration, not a medical diagnosis. A real clinical decision must always be made by a qualified healthcare professional.

## 2. The Complete Flow

```text
Raw CKD CSV
    |
    v
Preprocessing: clean missing values and encode categories
    |
    v
Feature selection: choose the five strongest correlations
    |
    v
Train/test split: 80% training data and 20% test data
    |
    v
KNN classifier: learn from similar training patients
    |
    v
Evaluation: calculate accuracy, precision, recall, F1-score
    |
    v
Notebook demo: predict labels for manually entered patients
```

## 3. Dataset

The dataset is the UCI Chronic Kidney Disease dataset. It contains 400 patient records, 24 clinical predictor fields, and one target field named `class`.

Examples of the original fields include:

- `hemo`: hemoglobin level
- `pcv`: packed cell volume
- `sg`: urine specific gravity
- `htn`: whether the patient has hypertension
- `rbcc`: red blood cell count
- `class`: the target label, either `ckd` or `notckd`

The raw file is stored in `data/ckd_raw.csv`. The dataset has missing values represented by `?`, which is common in medical datasets.

## 4. Preprocessing

The file `src/preprocess.py` prepares the data for machine learning.

1. It loads `data/ckd_raw.csv` using pandas.
2. It treats `?` and blank values as missing values.
3. It removes records with too much missing information.
4. It fills missing numeric values with the median of that column. The median is used because it is less affected by unusually high or low medical values than the mean.
5. It fills missing categorical values with the most common value, called the mode.
6. It converts categorical values into numeric values so that the machine-learning algorithm can use them. For example, `yes` and `no` become numeric categories.
7. It converts the target into `1` for CKD and `0` for not CKD.
8. It saves the result as `data/ckd_clean.csv`.

## 5. Feature Selection

The file `src/feature_selection.py` calculates the Pearson correlation between every cleaned feature and the encoded target class. A correlation score close to `1` or `-1` indicates a stronger relationship with the target. The script ranks features using the absolute value of the correlation because both positive and negative relationships are useful.

The five selected features in this run are:

| Feature | Absolute correlation |
| --- | ---: |
| `hemo` | 0.726368 |
| `pcv` | 0.673129 |
| `sg` | 0.659504 |
| `htn` | 0.590438 |
| `rbcc` | 0.566163 |

Keeping only five features makes the demo easier to explain and keeps it focused on the strongest relationships in this dataset. The selected dataset is saved to `data/ckd_selected.csv`, and the scores are saved to `data/selected_features.csv`.

Correlation does not prove that a feature causes CKD. It only measures how strongly the feature and target vary together in this dataset.

## 6. Train/Test Split

The file `src/train.py` separates the selected dataset into:

- 80% training data: used by the model to learn patterns.
- 20% test data: kept aside to evaluate how well the trained model works on unseen records.

The split is stratified, which keeps the CKD/not-CKD class proportions similar in both sets. `random_state=42` makes the split reproducible, so the same commands produce the same result.

## 7. The KNN Classifier

KNN means K-nearest neighbors. It predicts a new patient by comparing that patient with nearby patients in the training data.

This project uses `n_neighbors=5`, so the model considers the five most similar training examples. The majority class among those five neighbors becomes the prediction.

Before KNN runs, the five features are standardized using `StandardScaler`. This is important because the features have different units and ranges. Scaling prevents a feature with larger numerical values from unfairly dominating the distance calculation.

Only one classifier is used here: KNN. This keeps the implementation small and clear for the CIA-1 Part 5 demonstration.

The trained model is saved as `models/knn_ckd.pkl` using joblib.

## 8. Evaluation Results

The test set contains 80 records. The current reproducible run produces:

```text
Accuracy: 0.9375
Precision: 0.9787
Recall: 0.9200
F1-score: 0.9485
Confusion matrix:
[[29  1]
 [ 4 46]]
```

Meaning of the metrics:

- **Accuracy**: the proportion of all test predictions that were correct.
- **Precision**: among patients predicted as CKD, the proportion that were actually CKD.
- **Recall**: among actual CKD patients, the proportion the model detected.
- **F1-score**: a combined measure of precision and recall.
- **Confusion matrix**: shows correct and incorrect predictions for each class.

The matrix uses rows for the true label and columns for the predicted label. In this run, 29 non-CKD patients and 46 CKD patients were classified correctly.

## 9. Notebook Demonstration

The file `notebooks/demo.ipynb` demonstrates the saved model in four stages:

1. Load the model and test data and display the selected features.
2. Predict the test labels and plot a seaborn confusion-matrix heatmap.
3. Print the scikit-learn classification report.
4. Create three manual sample patient rows and print their predicted labels.

The final cell is the live part of the demonstration. It uses values for the same five features used during training: `hemo`, `pcv`, `sg`, `htn`, and `rbcc`.

## 10. How to Explain the Live Prediction

A sample explanation during the presentation could be:

> This row represents one manually entered patient using the five features selected during preprocessing. The saved KNN model compares the row with similar patients from its training data. It returns either CKD or Not CKD. This result is only a machine-learning screening output and should not be treated as a medical diagnosis.

## 11. Relation to the Reference Paper

The reference paper, “Hybrid AI-Based Chronic Kidney Disease Risk Prediction,” combines multiple algorithms: KNN, SVM, and EBT. That is a hybrid ensemble approach because several models contribute to the overall prediction system.

This repository implements only a small subset for CIA-1 Part 5:

- one KNN classifier instead of a KNN+SVM+EBT hybrid;
- five selected features instead of the full feature workflow;
- a clear preprocessing, training, evaluation, and live-demo pipeline.

The purpose is to demonstrate the implementation idea clearly, not to reproduce the entire research system.

## 12. Important Limitations

- The dataset is relatively small, with 400 records.
- The model is trained on one dataset and may not generalize to other hospitals or populations.
- Correlation-based feature selection does not establish medical causation.
- The model is not clinically validated.
- The output is a classroom demonstration and must not be used for diagnosis or treatment decisions.

## 13. Short Presentation Script

1. “This project demonstrates a lightweight CKD risk classifier using the UCI CKD dataset.”
2. “First, missing values are cleaned and categorical values are converted into numeric form.”
3. “Then, the five features with the strongest absolute correlations to the target are selected.”
4. “The data is split into 80% training and 20% testing records.”
5. “A scaled KNN classifier with five neighbors is trained.”
6. “The model achieves 93.75% accuracy and an F1-score of 0.9485 on this test split.”
7. “Finally, the notebook predicts CKD or Not CKD for manually entered sample patients.”
8. “This is a partial implementation of the paper's hybrid approach, using only one KNN classifier for the CIA-1 Part 5 requirement.”
