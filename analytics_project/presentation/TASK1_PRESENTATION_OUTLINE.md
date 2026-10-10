# Task 1 Presentation — Uber Fare Prediction

Use this as a slide outline. Add only insights reproduced from the final EDA notebook; do not treat preliminary values as conclusions.

1. **Title & objective** — Understanding factors associated with NYC Uber fares.
2. **Dataset and schema audit** — 50,000 rows, 26 columns; source differs from the PDF schema.
3. **Data quality first** — source coordinates are radians; explain conversion, NYC geographic validation, and cleaning log.
4. **Q1: Passenger count vs fare** — scatter/summary plot; distinguish association from causation.
5. **Q2: Car condition vs fare** — group distributions and a suitable nonparametric test.
6. **Q3: Fare by hour** — mean/uncertainty and per-hour sample counts.
7. **Q4: Traffic vs fare** — group distributions and test result.
8. **Q5: Trip distance vs fare** — scatter/hexbin, Pearson and Spearman; avoid claiming strongest predictor from correlation alone.
9. **Q6: Demand by hour** — hourly counts and hour-by-weekday pattern.
10. **Q7: Weather vs distance** — group distributions after handling invalid geographic rows.
11. **Q8: Airport proximity vs fare** — use recomputed documented distances, not suspect supplied distance columns.
12. **New questions** — fare drift over years, zero-distance trips, weekend effect, geographic pickup pattern.
13. **Key limitations and implications** — skewed fares, 2015 partial year, possible synthetic-looking categoricals, geographic bounds.
14. **Transition to Task 2** — decisions that EDA informs; explain leakage-safe preprocessing.

For each question slide, use the pattern: question → why this plot/test → chart → evidence-based interpretation → limitation.
