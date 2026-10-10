"""Reproducible audit for sample_50000.csv. Run: python -m src.uber_fare.audit"""
from pathlib import Path
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
CSV = ROOT / "data" / "raw" / "sample_50000.csv"
OUT = ROOT / "reports" / "audit.json"
# NYC-area bounds used as a conservative validity check after converting radians to degrees.
BOUNDS = {"lat_min": 40.45, "lat_max": 41.05, "lon_min": -74.30, "lon_max": -73.60}
COORDS = ["pickup_longitude", "pickup_latitude", "dropoff_longitude", "dropoff_latitude"]

def haversine_km(lat1, lon1, lat2, lon2):
    r = 6371.0
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat, dlon = lat2-lat1, lon2-lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1)*np.cos(lat2)*np.sin(dlon/2)**2
    return 2*r*np.arcsin(np.sqrt(np.clip(a, 0, 1)))

def main():
    df = pd.read_csv(CSV)
    report = {"file": str(CSV.relative_to(ROOT)), "shape": list(df.shape),
              "columns": list(df.columns), "missing_values_total": int(df.isna().sum().sum()),
              "missing_by_column": {k:int(v) for k,v in df.isna().sum().items()},
              "exact_duplicate_rows": int(df.duplicated().sum()),
              "key_duplicate_rows_after_first": int(df["key"].duplicated().sum()),
              "user_id_unique": bool(df["User ID"].is_unique)}
    dt = pd.to_datetime(df["pickup_datetime"], errors="coerce")
    report["pickup_datetime_min"] = str(dt.min())
    report["pickup_datetime_max"] = str(dt.max())
    report["datetime_parse_failures"] = int(dt.isna().sum())
    report["datetime_derived_columns_match_fraction"] = {}
    for col, vals in {"hour":dt.dt.hour,"day":dt.dt.day,"month":dt.dt.month,"weekday":dt.dt.weekday,"year":dt.dt.year}.items():
        report["datetime_derived_columns_match_fraction"][col] = float((pd.to_numeric(df[col], errors="coerce").to_numpy() == vals.to_numpy()).mean())
    # Raw coordinates are radians; convert before geographical validation.
    deg = df[COORDS].copy()
    deg["pickup_longitude"] = np.degrees(deg["pickup_longitude"])
    deg["pickup_latitude"] = np.degrees(deg["pickup_latitude"])
    deg["dropoff_longitude"] = np.degrees(deg["dropoff_longitude"])
    deg["dropoff_latitude"] = np.degrees(deg["dropoff_latitude"])
    zero_pickup = (deg.pickup_latitude.eq(0) & deg.pickup_longitude.eq(0))
    zero_dropoff = (deg.dropoff_latitude.eq(0) & deg.dropoff_longitude.eq(0))
    pickup_ok = deg.pickup_latitude.between(BOUNDS['lat_min'], BOUNDS['lat_max']) & deg.pickup_longitude.between(BOUNDS['lon_min'], BOUNDS['lon_max'])
    dropoff_ok = deg.dropoff_latitude.between(BOUNDS['lat_min'], BOUNDS['lat_max']) & deg.dropoff_longitude.between(BOUNDS['lon_min'], BOUNDS['lon_max'])
    valid = pickup_ok & dropoff_ok & ~zero_pickup & ~zero_dropoff
    report["coordinate_units"] = "radians in source CSV; degrees after conversion"
    report["nyc_bounds_degrees"] = BOUNDS
    report["zero_zero_pickups"] = int(zero_pickup.sum())
    report["zero_zero_dropoffs"] = int(zero_dropoff.sum())
    report["rows_outside_bounds_or_invalid_coordinates"] = int((~valid).sum())
    report["invalid_coordinate_fraction"] = float((~valid).mean())
    report["fare_summary"] = {k:float(v) for k,v in df.fare_amount.describe(percentiles=[.5,.9,.95,.99]).items()}
    report["fare_skew"] = float(df.fare_amount.skew())
    report["fare_nonpositive_rows"] = int((df.fare_amount <= 0).sum())
    report["fare_below_2_5_rows"] = int((df.fare_amount < 2.5).sum())
    report["passenger_count_counts"] = {str(k):int(v) for k,v in df.passenger_count.value_counts(dropna=False).sort_index().items()}
    report["categorical_levels"] = {c: {str(k):int(v) for k,v in df[c].value_counts(dropna=False).items()} for c in ["Car Condition","Weather","Traffic Condition"]}
    report["bearing_source_range"] = [float(df.bearing.min()), float(df.bearing.max())]
    report["bearing_units_note"] = "Values appear to be radians; verify range and distribution before conversion."
    report["distance_check"] = {"median_abs_difference_km": float(np.nanmedian(np.abs(df.distance - haversine_km(deg.pickup_latitude,deg.pickup_longitude,deg.dropoff_latitude,deg.dropoff_longitude)))),
                                 "note": "Computed after degree conversion; invalid coordinates can make this comparison meaningless."}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    print(f"\nSaved: {OUT}")

if __name__ == "__main__": main()
