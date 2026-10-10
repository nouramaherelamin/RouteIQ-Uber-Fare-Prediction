# RouteIQ — Fare Prediction

Flask + Leaflet interactive fare-estimation demo with the RouteIQ branding.

## Included
- RouteIQ app icon and favicon
- Full-color OpenStreetMap tiles
- Pickup/drop-off markers that can be selected or dragged
- Route visualization and direct-distance feature summary
- Flask prediction endpoint integration

## Run locally
1. Install dependencies: `py -m pip install -r requirements.txt`
2. Place your already-trained pipeline at `models/uber_fare_pipeline_v1.joblib`.
3. Ensure `src/uber_fare/features.py` matches the exact feature engineering class used when training the saved model.
4. Run: `py app.py`
5. Open `http://127.0.0.1:5000`.

The map uses OpenStreetMap tiles and public OSRM/Nominatim demo services, so an internet connection is needed for map tiles, road routes, and place labels. Fare prediction requires the existing trained pipeline; this archive does not contain a model artifact.
