"""Load the persisted end-to-end pipeline once and serve predictions."""
from pathlib import Path
import json
import joblib
import pandas as pd

class PredictionService:
    def __init__(self, model_path, metadata_path):
        self.model_path = Path(model_path)
        self.metadata_path = Path(metadata_path)
        if not self.model_path.exists():
            raise FileNotFoundError(f"Trained pipeline not found: {self.model_path}. Run python -m src.uber_fare.train first.")
        self.pipeline = joblib.load(self.model_path)
        self.metadata = json.loads(self.metadata_path.read_text()) if self.metadata_path.exists() else {}

    def predict(self, row):
        frame = pd.DataFrame([row])
        prediction = float(self.pipeline.predict(frame)[0])
        if not (-5 <= prediction <= 500):
            raise ValueError("The model returned a fare outside the demo's plausibility range. Please review the trip details.")
        return max(0.0, prediction)
