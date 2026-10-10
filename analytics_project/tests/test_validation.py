import pytest
from src.uber_fare.validation import parse_trip, InputValidationError

VALID = {
    "pickup_datetime": "2015-05-15T18:30",
    "pickup_latitude": "40.7580", "pickup_longitude": "-73.9855",
    "dropoff_latitude": "40.7306", "dropoff_longitude": "-73.9352",
    "passenger_count": "1",
}

def test_valid_trip_parses_to_raw_schema():
    row = parse_trip(VALID)
    assert row["passenger_count"] == 1
    assert row["pickup_latitude"] == 40.758
    assert "pickup_datetime" in row

def test_missing_field_rejected():
    bad = dict(VALID); bad["pickup_latitude"] = ""
    with pytest.raises(InputValidationError, match="complete all required"):
        parse_trip(bad)

def test_out_of_range_coordinate_rejected():
    bad = dict(VALID); bad["pickup_latitude"] = "0"
    with pytest.raises(InputValidationError, match="Latitude"):
        parse_trip(bad)

def test_invalid_passenger_count_rejected():
    bad = dict(VALID); bad["passenger_count"] = "9"
    with pytest.raises(InputValidationError, match="Passenger count"):
        parse_trip(bad)

def test_identical_locations_rejected():
    bad = dict(VALID); bad["dropoff_latitude"] = bad["pickup_latitude"]; bad["dropoff_longitude"] = bad["pickup_longitude"]
    with pytest.raises(InputValidationError, match="identical"):
        parse_trip(bad)
