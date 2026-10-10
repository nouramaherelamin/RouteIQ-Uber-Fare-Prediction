# Phase C — Task 2 status

## Implemented
- Deterministic source-data cleaning and radian-to-degree conversion in `src/uber_fare/data.py`.
- Shared feature engineering in `src/uber_fare/features.py`.
- Pipeline factory, train/test split, 5-fold CV, categorical ablation, model comparison, RandomizedSearchCV, hold-out metrics, model persistence, and chronological robustness check in `src/uber_fare/train.py`.
- Notebook documentation in `notebooks/02_preprocessing_modeling.ipynb`.

## Execution status
The full training run did not finish within the execution time limit in this environment. Therefore no completed model comparison, final model selection, or trustworthy test metrics are claimed here. Run `python -m src.uber_fare.train` from the repository root in a local environment and inspect the generated report files after successful completion.

## Important caveats
- The input CSV has 50,000 rows; this file is not confirmed to be the exact `final_internship_data.csv` named in the assignment PDF.
- Airport/landmark coordinates in `features.py` are documented approximate public coordinates. They replace unreliable supplied distance columns, but the choice of reference points should be stated in the report.
- The primary random split is the assignment-compatible 80/20 split. A chronological 2015 check is supplementary due to observed fare drift.
