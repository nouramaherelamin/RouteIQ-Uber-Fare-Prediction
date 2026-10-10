import numpy as np
from src.uber_fare.features import haversine_km

def test_same_point_distance_is_zero():
    assert abs(float(haversine_km(40.7, -74.0, 40.7, -74.0))) < 1e-9

def test_distance_is_positive_for_different_points():
    assert float(haversine_km(40.7, -74.0, 40.8, -73.9)) > 0
