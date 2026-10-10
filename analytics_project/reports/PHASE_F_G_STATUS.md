# Phase F/G — Testing, Documentation and Presentation

## Verified in this workspace
- `python -m pytest -q`: **7 passed** (unit tests only).
- Existing tests cover geographic feature helpers and input validation.

## Not yet verified
- Model training and hyperparameter search have not completed successfully in this workspace.
- No final model artifact or trustworthy model comparison table is available yet.
- Flask browser workflow and `/health` have not been tested end-to-end with a trained model.
- UI evidence screenshots must be captured by a person from the real local browser; do not fabricate them.

## Required real-browser evidence
Save the following under `evidence/screenshots/`:
1. `ui_test_01_short_trip_form.png`
2. `ui_test_01_short_trip_result.png`
3. `ui_test_02_airport_trip_form.png`
4. `ui_test_02_airport_trip_result.png`
5. `ui_test_03_cross_borough_form.png`
6. `ui_test_03_cross_borough_result.png`
7. `ui_test_04_invalid_input.png`

For each valid case, record the entered coordinates, pickup datetime, passenger count, and predicted fare in a small evidence log. For invalid input, show the validation message and confirm there is no error page.

## Final acceptance checklist
- [ ] Run audit from a fresh environment and inspect `reports/audit.json`.
- [ ] Re-run notebooks from top to bottom; ensure figures and interpretations are present.
- [ ] Confirm the deterministic cleaning count and explain each excluded row category.
- [ ] Train baseline and tuned models with preprocessing inside each CV fold.
- [ ] Run categorical feature ablation using training CV only.
- [ ] Freeze model choice before evaluating the held-out test set.
- [ ] Report MAE, RMSE and R² in fare dollars; distinguish CV from test results.
- [ ] Save one complete pipeline and metadata, then load it in a fresh process.
- [ ] Run `python -m pytest -q`.
- [ ] Run Flask locally; verify `/health` and three successful plus one invalid browser test.
- [ ] Capture the seven real screenshots listed above.
- [ ] Update README with actual metrics and model justification; never leave placeholder or invented scores.
- [ ] Confirm submission rubric total with instructor: Task 3 rubric rows sum to 110 points.
