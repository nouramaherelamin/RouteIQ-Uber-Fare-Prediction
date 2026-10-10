from pathlib import Path
from datetime import datetime
import sys
import math
import uuid
import joblib
import pandas as pd
from flask import Flask, render_template, request, jsonify

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
ANALYTICS_DIR = PROJECT_ROOT / 'analytics_project'
# Make the analytics project's `src` package importable when loading the fitted sklearn pipeline.
if str(ANALYTICS_DIR) not in sys.path:
    sys.path.insert(0, str(ANALYTICS_DIR))
MODEL_CANDIDATES = [
    BASE_DIR / 'models' / 'uber_fare_pipeline_v1.joblib',
    BASE_DIR / 'uber_fare_pipeline_v1.joblib',
    ANALYTICS_DIR / 'models' / 'uber_fare_pipeline_v1.joblib',
    BASE_DIR / 'final_regression_pipeline.joblib',
]
MODEL_PATH = next((p for p in MODEL_CANDIDATES if p.exists()), None)
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# The fitted pipeline is loaded once at startup. The model file is supplied from the existing Task 2 project.
model = None
model_load_error = None
if MODEL_PATH:
    try:
        model = joblib.load(MODEL_PATH)
    except Exception as exc:
        model_load_error = str(exc)
else:
    model_load_error = 'Model file not found. Copy models/uber_fare_pipeline_v1.joblib from your existing Task 2 project.'

NYC_BOUNDS = {'south': 40.49, 'north': 40.92, 'west': -74.28, 'east': -73.68}
DEFAULTS = {
    'pickup_datetime': '2015-05-15T18:30', 'passenger_count': '1',
    'pickup_latitude': '40.7580', 'pickup_longitude': '-73.9855',
    'dropoff_latitude': '40.7306', 'dropoff_longitude': '-73.9352',
}

# Approximate reference coordinates used to derive model inputs (km).
REFERENCES = {
    'jfk_dist_km': (40.6413, -73.7781),
    'ewr_dist_km': (40.6895, -74.1745),
    'lga_dist_km': (40.7769, -73.8740),
    'sol_dist_km': (40.6892, -74.0445),
    'nyc_dist_km': (40.7128, -74.0060),
}

def haversine_km(lat1, lon1, lat2, lon2):
    r = 6371.0088
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = math.radians(lat2-lat1), math.radians(lon2-lon1)
    a = math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return 2*r*math.asin(min(1.0, math.sqrt(a)))

def initial_bearing_deg(lat1, lon1, lat2, lon2):
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dl = math.radians(lon2-lon1)
    y = math.sin(dl)*math.cos(p2)
    x = math.cos(p1)*math.sin(p2)-math.sin(p1)*math.cos(p2)*math.cos(dl)
    return (math.degrees(math.atan2(y, x)) + 360) % 360

def parse_datetime(raw):
    try:
        dt = datetime.fromisoformat(raw)
    except (TypeError, ValueError):
        raise ValueError('Choose a valid pickup date and time.')
    if not (2009 <= dt.year <= 2015):
        raise ValueError('Pickup date must be between 2009 and 2015, matching the training data.')
    return dt

def build_row(form):
    dt = parse_datetime(form.get('pickup_datetime', ''))
    try:
        passengers_raw = float(form.get('passenger_count', ''))
        if not passengers_raw.is_integer():
            raise ValueError
        passengers = int(passengers_raw)
    except (TypeError, ValueError):
        raise ValueError('Passenger count must be a whole number.')
    if not 1 <= passengers <= 6:
        raise ValueError('Passenger count must be between 1 and 6.')
    def coord(name, label, lo, hi):
        try: x = float(form.get(name, ''))
        except (TypeError, ValueError): raise ValueError(f'{label} must be a valid number.')
        if not math.isfinite(x) or not lo <= x <= hi:
            raise ValueError(f'{label} must be between {lo} and {hi}.')
        return x
    plat = coord('pickup_latitude', 'Pickup latitude', NYC_BOUNDS['south'], NYC_BOUNDS['north'])
    plon = coord('pickup_longitude', 'Pickup longitude', NYC_BOUNDS['west'], NYC_BOUNDS['east'])
    dlat = coord('dropoff_latitude', 'Drop-off latitude', NYC_BOUNDS['south'], NYC_BOUNDS['north'])
    dlon = coord('dropoff_longitude', 'Drop-off longitude', NYC_BOUNDS['west'], NYC_BOUNDS['east'])
    distance = haversine_km(plat, plon, dlat, dlon)
    if distance < 0.05:
        raise ValueError('Pickup and drop-off are almost the same point. Choose two different locations.')
    bearing = initial_bearing_deg(plat, plon, dlat, dlon)
    row = {
        'pickup_datetime': dt,
        'pickup_latitude': plat,
        'pickup_longitude': plon,
        'dropoff_latitude': dlat,
        'dropoff_longitude': dlon,
        'passenger_count': passengers,
        # The selected trained pipeline's feature engineer recomputes these deterministically.
        'Car Condition': 'Good', 'Weather': 'sunny', 'Traffic Condition': 'Flow Traffic',
    }
    return pd.DataFrame([row]), {'distance_km': distance, 'bearing_deg': bearing, 'passengers': passengers, 'pickup': dt.strftime('%b %d, %Y · %I:%M %p')}

@app.get('/')
def home():
    return render_template('index.html', defaults=DEFAULTS, model_ready=model is not None, model_error=model_load_error)

@app.post('/api/predict')
def predict():
    if model is None:
        return jsonify(ok=False, error=f'Model is not ready. {model_load_error}'), 503
    try:
        X, meta = build_row(request.form)
        value = float(model.predict(X)[0])
        if not math.isfinite(value):
            raise ValueError('The model returned a non-finite prediction. Please check the trip details.')
        value = max(0.0, value)
        return jsonify(ok=True, prediction=round(value, 2), distance=f"{meta['distance_km']:.2f}", bearing=f"{meta['bearing_deg']:.1f}°", passengers=meta['passengers'], pickup=meta['pickup'], request_id=uuid.uuid4().hex)
    except ValueError as exc:
        return jsonify(ok=False, error=str(exc)), 400
    except Exception as exc:
        app.logger.exception('Prediction failed')
        return jsonify(ok=False, error='Prediction failed. Check that the saved Task 2 pipeline and its feature module match this app.'), 500

@app.get('/health')
def health():
    return jsonify(status='ok' if model is not None else 'model_missing', model_loaded=model is not None, model_path=str(MODEL_PATH) if MODEL_PATH else None, error=model_load_error)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)
