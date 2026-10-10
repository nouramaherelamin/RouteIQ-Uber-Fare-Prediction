"""Validation for raw Flask form input."""
from datetime import datetime

NYC_BOUNDS = {"lat_min": 40.45, "lat_max": 41.05, "lon_min": -74.30, "lon_max": -73.60}

class InputValidationError(ValueError):
    pass

def parse_trip(form):
    required = ["pickup_datetime", "pickup_latitude", "pickup_longitude", "dropoff_latitude", "dropoff_longitude", "passenger_count"]
    missing = [k for k in required if not str(form.get(k, "")).strip()]
    if missing:
        raise InputValidationError("Please complete all required fields: " + ", ".join(missing))
    try:
        dt = datetime.fromisoformat(form["pickup_datetime"])
        vals = {k: float(form[k]) for k in ["pickup_latitude", "pickup_longitude", "dropoff_latitude", "dropoff_longitude"]}
        passengers = int(form["passenger_count"])
    except (TypeError, ValueError):
        raise InputValidationError("Enter a valid date/time and numeric values in every location field.")
    if not (NYC_BOUNDS["lat_min"] <= vals["pickup_latitude"] <= NYC_BOUNDS["lat_max"] and NYC_BOUNDS["lat_min"] <= vals["dropoff_latitude"] <= NYC_BOUNDS["lat_max"]):
        raise InputValidationError("Latitude must be within the supported NYC area (40.45 to 41.05 degrees).")
    if not (NYC_BOUNDS["lon_min"] <= vals["pickup_longitude"] <= NYC_BOUNDS["lon_max"] and NYC_BOUNDS["lon_min"] <= vals["dropoff_longitude"] <= NYC_BOUNDS["lon_max"]):
        raise InputValidationError("Longitude must be within the supported NYC area (-74.30 to -73.60 degrees).")
    if passengers not in range(1, 7):
        raise InputValidationError("Passenger count must be an integer from 1 to 6.")
    if vals["pickup_latitude"] == vals["dropoff_latitude"] and vals["pickup_longitude"] == vals["dropoff_longitude"]:
        raise InputValidationError("Pickup and drop-off coordinates are identical. Please check the trip locations.")
    if dt.year < 2009 or dt.year > datetime.now().year:
        raise InputValidationError("Choose a trip date from 2009 through the current year supported by this demo.")
    row = {"pickup_datetime": dt, **vals, "passenger_count": passengers}
    # Categorical values are added only when selected by the ablation decision.
    for col, allowed in {"Car Condition": ["Good", "Bad", "Very Good", "Excellent"], "Weather": ["sunny", "stormy", "rainy", "windy", "cloudy"], "Traffic Condition": ["Flow", "Dense", "Congested"]}.items():
        value = form.get(col, "")
        if value:
            if value not in allowed:
                raise InputValidationError(f"Invalid value for {col}.")
            row[col] = value
    return row
