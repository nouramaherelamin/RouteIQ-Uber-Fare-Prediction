"""Dataset loading and deterministic, documented cleaning rules."""
from pathlib import Path
import numpy as np
import pandas as pd

NYC_BOUNDS = {"lat_min": 40.45, "lat_max": 41.05, "lon_min": -74.30, "lon_max": -73.60}
COORDS = ["pickup_longitude", "pickup_latitude", "dropoff_longitude", "dropoff_latitude"]

def load_clean_data(path):
    df = pd.read_csv(path)
    # Source coordinate columns are radians despite the schema implying longitude/latitude.
    for col in COORDS:
        df[col] = np.degrees(pd.to_numeric(df[col], errors="coerce"))
    df["pickup_datetime"] = pd.to_datetime(df["pickup_datetime"], errors="coerce")
    # Drop invalid target, unparsable timestamps, and geographically invalid trips.
    df = df.loc[df["fare_amount"].gt(0) & df["pickup_datetime"].notna()].copy()
    p_ok = df.pickup_latitude.between(NYC_BOUNDS["lat_min"], NYC_BOUNDS["lat_max"]) & df.pickup_longitude.between(NYC_BOUNDS["lon_min"], NYC_BOUNDS["lon_max"])
    d_ok = df.dropoff_latitude.between(NYC_BOUNDS["lat_min"], NYC_BOUNDS["lat_max"]) & df.dropoff_longitude.between(NYC_BOUNDS["lon_min"], NYC_BOUNDS["lon_max"])
    zero = (df.pickup_latitude.eq(0) & df.pickup_longitude.eq(0)) | (df.dropoff_latitude.eq(0) & df.dropoff_longitude.eq(0))
    df = df.loc[p_ok & d_ok & ~zero].copy()
    # Use timestamp-derived features as source of truth, avoiding inconsistent stored values.
    df["hour"] = df.pickup_datetime.dt.hour
    df["day"] = df.pickup_datetime.dt.day
    df["month"] = df.pickup_datetime.dt.month
    df["weekday"] = df.pickup_datetime.dt.weekday
    df["year"] = df.pickup_datetime.dt.year
    return df.reset_index(drop=True)
