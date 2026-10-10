# Data Dictionary and Schema Reconciliation — Phase 1

## Dataset provenance and current limitation

- Required dataset name in the Task 1 brief: `final_internship_data.csv`.
- User-selected final dataset: `final_internship_data.xlsx`.
- Dataset actually available and audited in this workspace: `sample_50000(6).csv` (50,000 rows × 26 columns).
- **Important:** `final_internship_data.xlsx` was not found in `/mnt/data` during Phase 1. Therefore, this dictionary describes the observed `sample_50000.csv` schema only and must be verified against the final XLSX before the later phases use it as the modeling source.

## Observed columns

| Column | Observed type (CSV inference) | Meaning / Phase 1 handling |
|---|---|---|
| `User ID` | integer-like | User identifier; exclude from predictive features because it is an identifier, not a trip attribute. |
| `User Name` | string | Personal/name field; exclude from model features. |
| `Driver Name` | string | Driver name; exclude from model features. |
| `Car Condition` | string/category | Vehicle condition. Observed levels must be audited; evaluate only via train-fold CV ablation. |
| `Weather` | string/category | Weather category at pickup. Preserve observed spelling/case until a documented normalization step. |
| `Traffic Condition` | string/category | Traffic category. Preserve observed spelling/case until a documented normalization step. |
| `key` | datetime-like string | Timestamp-like key; equals `pickup_datetime` in all 50,000 rows in this audit. Repeated values can be distinct trips; do not deduplicate by key. |
| `fare_amount` | float | Regression target, USD. Nine non-positive targets are present; later modeling cohort should exclude target errors by a documented rule. |
| `pickup_datetime` | datetime-like string | Trip pickup timestamp; canonical raw temporal input for feature engineering. |
| `pickup_longitude` | float | Pickup longitude in radians in the supplied CSV; convert to degrees at ingestion and validate against the documented NYC bounds. |
| `pickup_latitude` | float | Pickup latitude in radians in the supplied CSV; convert to degrees at ingestion and validate against the documented NYC bounds. |
| `dropoff_longitude` | float | Drop-off longitude in radians in the supplied CSV; convert to degrees at ingestion and validate against the documented NYC bounds. |
| `dropoff_latitude` | float | Drop-off latitude in radians in the supplied CSV; convert to degrees at ingestion and validate against the documented NYC bounds. |
| `passenger_count` | integer-like | Passenger count. 165 rows have value zero; investigate/document validity before modeling. |
| `hour` | integer-like | Supplied hour feature; validate against `pickup_datetime`, then prefer shared feature engineering from the canonical timestamp. |
| `day` | integer-like | Day of month, not day of week. |
| `month` | integer-like | Month derived from pickup timestamp; validate against timestamp. |
| `weekday` | integer-like | Day of week; audit notes use 0=Monday. |
| `year` | integer-like | Year derived from pickup timestamp; validate against timestamp. |
| `jfk_dist` | float | Supplied distance to JFK; audit shows supplied values are inconsistent with recomputation from documented reference coordinates. Do not use directly as a model feature. |
| `ewr_dist` | float | Supplied distance to EWR; audit shows supplied values are inconsistent with recomputation. Do not use directly as a model feature. |
| `lga_dist` | float | Supplied distance to LGA; audit shows supplied values are inconsistent with recomputation. Do not use directly as a model feature. |
| `sol_dist` | float | Supplied distance to Statue of Liberty reference; audit shows supplied values are inconsistent with recomputation. Do not use directly as a model feature. |
| `nyc_dist` | float | Supplied distance to Times Square reference; audit shows supplied values are inconsistent with recomputation. Do not use directly as a model feature. |
| `distance` | float | Supplied trip distance; it matches haversine computed from the supplied coordinates to numerical precision, including potentially invalid coordinates. Recompute from validated coordinates in the shared feature transformer. |
| `bearing` | float | Supplied bearing appears to be in radians; verify the convention and derive consistently from validated coordinates rather than trusting this column as-is. |

## Observed schema differences from the PDFs

1. The Task 1 PDF names `final_internship_data.csv`; the selected file name is `final_internship_data.xlsx`, while only `sample_50000(6).csv` was present for this run.
2. The observed schema uses snake_case for many columns and spaces in `User ID`, `Car Condition`, and `Traffic Condition`.
3. The observed data has `weekday` (day of week) and `day` (day of month); it does not have a `Week` column.
4. The observed data includes `year` and `nyc_dist`, which are additional fields compared with the PDF's abbreviated data dictionary.
5. `key` is a datetime-like string and exactly matches `pickup_datetime` for this audited sample. It is not a safe deduplication key.
6. The coordinate columns and bearing appear to be radians. Coordinates must be converted to degrees at ingestion because the UI/raw prediction schema uses degrees.
7. The supplied airport/landmark distance fields do not agree with recomputation using documented reference points and are excluded in favor of shared feature engineering.
8. The supplied `distance` column agrees with haversine on the supplied coordinate values, but that does not establish the coordinates are valid.

## Phase 1 audit facts from the actual run

- Shape: 50,000 × 26.
- Null cells: 0.
- Exact duplicate rows: 0.
- Non-positive fares: 9 (6 negative).
- Zero passenger count: 165.
- Repeated `key` values after first occurrence: 445.
- `key` equals `pickup_datetime`: 50,000 / 50,000.
- Rows outside the NYC bounding box at either endpoint: 1,103 (2.206% of rows), using the current script's documented bounds.
- Raw exact `(0, 0)` coordinate pairs: pickup 953; drop-off 955.
- Possible swapped-coordinate pattern: 19 pickup endpoints and 19 drop-off endpoints; this heuristic must be validated before cleaning.
- The measured 1,103 out-of-bounds rows differ from the preliminary estimate of ~1,047. The audit output is the source of truth for this sample; investigate rule details before Phase 2 cleaning.
- Supplied `distance` vs haversine correlation: 1.0; median absolute difference approximately `5.97e-12` km.
- Median supplied/recomputed distance ratio on valid pickup-bbox rows: JFK ~2.00, EWR ~1.94, LGA ~2.02, Statue of Liberty ~2.01, Times Square ~4.77. These supplied columns should not be used directly.

## Confirmed project decisions

- Audit `sample_50000.csv` as preliminary data only; use `final_internship_data.xlsx` as the intended final dataset once it is provided and audited.
- Remove rows with clearly invalid pickup or drop-off coordinates using a deterministic, documented rule before the train/test split, while preserving audit counts.
- Compare models with and without `Car Condition`, `Weather`, and `Traffic Condition` using training-only cross-validation; keep these variables only if CV supports them.
- Apply fixed data-error rules before splitting (for example, invalid coordinates and non-positive target fares); fit all learned transformations only within training/CV pipelines.
