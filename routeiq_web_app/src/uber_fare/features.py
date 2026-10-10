"""Feature engineering used by the Task 2 Uber fare pipeline.

Keep the module path src.uber_fare.features and class name stable: joblib
artifacts may refer to this import path when they are loaded by Flask.
"""
import math
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

_REFERENCE_POINTS = {
    'jfk_dist_km': (40.6413, -73.7781),
    'ewr_dist_km': (40.6895, -74.1745),
    'lga_dist_km': (40.7769, -73.8740),
    'sol_dist_km': (40.6892, -74.0445),
    'nyc_dist_km': (40.7128, -74.0060),
}

def _haversine(lat1, lon1, lat2, lon2):
    r = 6371.0088
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat, dlon = lat2-lat1, lon2-lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1)*np.cos(lat2)*np.sin(dlon/2)**2
    return 2*r*np.arcsin(np.sqrt(np.clip(a, 0, 1)))

class UberFeatureEngineer(BaseEstimator, TransformerMixin):
    """Create distance, bearing and cyclical time features from raw trip columns."""
    def __init__(self, include_categoricals=True):
        self.include_categoricals = include_categoricals

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        x = X.copy() if isinstance(X, pd.DataFrame) else pd.DataFrame(X)
        dt = pd.to_datetime(x['pickup_datetime'], errors='coerce')
        for col in ['pickup_latitude','pickup_longitude','dropoff_latitude','dropoff_longitude']:
            x[col] = pd.to_numeric(x[col], errors='coerce')
        plat, plon = x['pickup_latitude'], x['pickup_longitude']
        dlat, dlon = x['dropoff_latitude'], x['dropoff_longitude']
        x['distance_km'] = _haversine(plat, plon, dlat, dlon)
        lat1, lat2 = np.radians(plat), np.radians(dlat)
        dlon_rad = np.radians(dlon-plon)
        by = np.sin(dlon_rad)*np.cos(lat2)
        bx = np.cos(lat1)*np.sin(lat2)-np.sin(lat1)*np.cos(lat2)*np.cos(dlon_rad)
        bearing = (np.degrees(np.arctan2(by, bx))+360) % 360
        x['bearing_sin'] = np.sin(np.radians(bearing))
        for name, (rlat, rlon) in _REFERENCE_POINTS.items():
            x[name] = _haversine(plat, plon, rlat, rlon)
        hour = dt.dt.hour.fillna(0)
        weekday = dt.dt.weekday.fillna(0)
        month = dt.dt.month.fillna(1)
        x['hour_sin'] = np.sin(2*np.pi*hour/24)
        x['hour_cos'] = np.cos(2*np.pi*hour/24)
        x['weekday_sin'] = np.sin(2*np.pi*weekday/7)
        x['weekday_cos'] = np.cos(2*np.pi*weekday/7)
        x['month_sin'] = np.sin(2*np.pi*(month-1)/12)
        x['month_cos'] = np.cos(2*np.pi*(month-1)/12)
        x['year'] = dt.dt.year
        if not self.include_categoricals:
            x = x.drop(columns=['Car Condition','Weather','Traffic Condition'], errors='ignore')
        return x.replace([np.inf, -np.inf], np.nan)
