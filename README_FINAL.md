# Uber Fare Prediction — RouteIQ Final Package

This package groups the latest available analytics project files and the latest RouteIQ interactive Flask/map UI into one folder.

## Folders

- `analytics_project/` — EDA and modeling source, notebooks, data, reports, tests, and the original Flask app.
- `routeiq_web_app/` — branded RouteIQ Flask UI, Leaflet map assets, favicon, logo assets, and ownership footer.

## Important verification note

These are the latest available project packages combined for convenience; this packaging step does not retrain a model or prove that the RouteIQ UI is connected to a saved trained model. The RouteIQ package currently contains no `.joblib`/`.pkl` model artifact. Before presenting it as fully integrated, verify the app's model-loading/training behavior and run the tests in `analytics_project/`.

## Run the analytics app

Open a terminal in `analytics_project/`, create/activate a virtual environment, then run:

```bash
pip install -r requirements.txt
python app.py
```

## Run the RouteIQ UI

Open a separate terminal in `routeiq_web_app/`, create/activate a virtual environment, then run:

```bash
pip install -r requirements.txt
python app.py
```

If either app expects a model or additional generated artifact, follow its README and training instructions. Do not assume the two apps share a model automatically.

## Additional User-Interactive Analytics App

A separate Streamlit dashboard is included at `analytics_project/interactive_dashboard/app.py`. It complements the Flask RouteIQ prediction app; it does not replace it. The dashboard provides interactive EDA, Plotly charts, global filters, data quality, correlation exploration, and CSV export.

Run from `analytics_project/`:

```powershell
py -m pip install -r interactive_dashboard/requirements.txt
py -m streamlit run interactive_dashboard/app.py
```

The dashboard reads `data/raw/sample_50000.csv` from the existing project package. It is descriptive analytics and does not retrain or change the saved prediction model.


## Navigate between the two local apps

- RouteIQ Fare Prediction (Flask): `http://127.0.0.1:5000`
- Uber Fare Interactive Analytics (Streamlit): `http://127.0.0.1:8501`

Each app includes a link to open the other in a new browser tab. Both servers must be running for both links to work. Start Flask with `python -m flask --app routeiq_web_app.app run --debug` from the project root, and start Streamlit with `python -m streamlit run analytics_project/interactive_dashboard/app.py` from the same root.
