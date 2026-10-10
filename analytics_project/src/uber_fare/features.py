"""Shared raw-input feature engineering for training and inference."""
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

EARTH_KM = 6371.0088
# Approximate documented reference coordinates (latitude, longitude), degrees.
REFERENCES = {
    "jfk": (40.6413, -73.7781),
    "ewr": (40.6895, -74.1745),
    "lga": (40.7769, -73.8740),
    "sol": (40.6892, -74.0445),
    "nyc": (40.7128, -74.0060),
}

def haversine_km(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(np.radians, [np.asarray(lat1), np.asarray(lon1), np.asarray(lat2), np.asarray(lon2)])
    dlat, dlon = lat2-lat1, lon2-lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1)*np.cos(lat2)*np.sin(dlon/2)**2
    return 2 * EARTH_KM * np.arcsin(np.sqrt(np.clip(a, 0, 1)))

class UberFeatureEngineer(BaseEstimator, TransformerMixin):
    """Accept raw form-like fields; output engineered numeric and optional categorical features."""
    def __init__(self, include_categoricals=True):
        self.include_categoricals = include_categoricals
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        df = X.copy() if isinstance(X, pd.DataFrame) else pd.DataFrame(X, columns=self.feature_names_in_)
        dt = pd.to_datetime(df["pickup_datetime"], errors="coerce")
        out = pd.DataFrame(index=df.index)
        for c in ["pickup_latitude", "pickup_longitude", "dropoff_latitude", "dropoff_longitude", "passenger_count"]:
            out[c] = pd.to_numeric(df[c], errors="coerce")
        out["distance_km"] = haversine_km(out.pickup_latitude, out.pickup_longitude, out.dropoff_latitude, out.dropoff_longitude)
        for name, (lat, lon) in REFERENCES.items():
            out[f"{name}_dist_km"] = haversine_km(out.pickup_latitude, out.pickup_longitude, lat, lon)
        out["bearing_sin"] = np.sin(np.arctan2(np.sin(np.radians(out.dropoff_longitude-out.pickup_longitude))*np.cos(np.radians(out.dropoff_latitude)), np.cos(np.radians(out.pickup_latitude))*np.sin(np.radians(out.dropoff_latitude))-np.sin(np.radians(out.pickup_latitude))*np.cos(np.radians(out.dropoff_latitude))*np.cos(np.radians(out.dropoff_longitude-out.pickup_longitude))))
        out["hour_sin"] = np.sin(2*np.pi*dt.dt.hour/24)
        out["hour_cos"] = np.cos(2*np.pi*dt.dt.hour/24)
        out["weekday_sin"] = np.sin(2*np.pi*dt.dt.weekday/7)
        out["weekday_cos"] = np.cos(2*np.pi*dt.dt.weekday/7)
        out["month_sin"] = np.sin(2*np.pi*(dt.dt.month-1)/12)
        out["month_cos"] = np.cos(2*np.pi*(dt.dt.month-1)/12)
        out["year"] = dt.dt.year
        if self.include_categoricals:
            for c in ["Car Condition", "Weather", "Traffic Condition"]:
                if c in df.columns: out[c] = df[c].astype("object")
        return out
