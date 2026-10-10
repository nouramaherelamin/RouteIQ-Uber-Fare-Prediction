# Phase D/E status — Model comparison and Flask deployment

## Implemented
- Flask app factory with `/`, `/predict`, and `/health` routes.
- Pipeline and metadata are loaded once during app creation, not once per request.
- Raw form schema is passed to the persisted pipeline; feature engineering is not duplicated in the route.
- HTML form uses date/time and numeric inputs, with responsive CSS.
- Server-side validation covers missing values, parse errors, NYC coordinate bounds, passenger count, identical locations, and date range.
- Unit tests cover core validation cases and geographic feature functions.

## Not yet complete
- No trained model artifact is present in this project folder at this point. Run `python -m src.uber_fare.train` after dependencies are installed.
- Model comparison metrics and the categorical feature-ablation decision must be based on the actual completed run; they must not be fabricated.
- The app cannot return a fare until `models/uber_fare_pipeline_v1.joblib` is created by training.
- The required screenshots must be captured from a real local browser session after a valid model is available.

## Run locally
```bash
python -m pip install -r requirements.txt
python -m src.uber_fare.train
python app.py
```
Open `http://127.0.0.1:5000` and check `/health`.
