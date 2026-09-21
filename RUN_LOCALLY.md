# Run CKD Risk Demo Locally

These commands run the project from a fresh clone. Run each command separately from the project directory.

## Windows PowerShell

### 1. Clone the repository

```powershell
git clone https://github.com/Regemsol/ckd-risk-demo.git
cd ckd-risk-demo
```

### 2. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run this once in the current terminal and activate again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Run preprocessing

```powershell
python src\preprocess.py
```

Expected result:

```text
Saved 400 cleaned rows to ...\data\ckd_clean.csv
```

### 5. Select the five features

```powershell
python src\feature_selection.py
```

Expected selected features:

```text
hemo    0.726368
pcv     0.673129
sg      0.659504
htn     0.590438
rbcc    0.566163
```

### 6. Train and evaluate the KNN model

```powershell
python src\train.py
```

The script prints accuracy, precision, recall, F1-score, the confusion matrix, and saves the model to `models\knn_ckd.pkl`.

### 7. Open the demo notebook

```powershell
jupyter notebook notebooks\demo.ipynb
```

Run the notebook cells from top to bottom. The final cell predicts `CKD` or `Not CKD` for three sample patients.

### 8. Deactivate the environment

```powershell
deactivate
```

## Linux or macOS

### 1. Clone the repository

```bash
git clone https://github.com/Regemsol/ckd-risk-demo.git
cd ckd-risk-demo
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the pipeline

```bash
python src/preprocess.py
python src/feature_selection.py
python src/train.py
```

### 5. Open the demo notebook

```bash
jupyter notebook notebooks/demo.ipynb
```

### 6. Deactivate the environment

```bash
deactivate
```

## Expected training metrics

The committed dataset and pipeline should produce approximately:

```text
Accuracy: 0.9375
Precision: 0.9787
Recall: 0.9200
F1-score: 0.9485
Confusion matrix:
[[29  1]
 [ 4 46]]
```

If `ModuleNotFoundError: No module named 'pandas'` appears, activate `.venv` and run the dependency installation command again. If `pip` says that `src/preprocess.py` is an invalid requirement, the install and Python commands were pasted onto one line; run them separately.
