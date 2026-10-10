"""Flask UI for Uber fare prediction. Requires a trained pipeline artifact."""
from pathlib import Path
from flask import Flask, render_template, request
from src.uber_fare.predict import PredictionService
from src.uber_fare.validation import parse_trip, InputValidationError

ROOT = Path(__file__).resolve().parent

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.update(SECRET_KEY="local-demo-change-me")
    if test_config:
        app.config.update(test_config)
    model_path = app.config.get("MODEL_PATH", ROOT / "models/uber_fare_pipeline_v1.joblib")
    metadata_path = app.config.get("METADATA_PATH", ROOT / "models/model_metadata.json")
    service = None
    try:
        service = PredictionService(model_path, metadata_path)
    except FileNotFoundError as exc:
        app.logger.warning(str(exc))
    app.extensions["prediction_service"] = service

    @app.get("/")
    def index():
        return render_template("index.html", values={}, error=None, model_ready=service is not None)

    @app.post("/predict")
    def predict():
        values = request.form.to_dict()
        if service is None:
            return render_template("index.html", values=values, error="The trained model is not installed yet. Run the training script and restart the app.", model_ready=False), 503
        try:
            row = parse_trip(request.form)
            fare = service.predict(row)
            return render_template("result.html", fare=fare, trip=row)
        except InputValidationError as exc:
            return render_template("index.html", values=values, error=str(exc), model_ready=True), 400
        except Exception:
            app.logger.exception("Prediction failed")
            return render_template("index.html", values=values, error="We couldn't calculate a fare from these details. Please review the trip and try again.", model_ready=True), 400

    @app.get("/health")
    def health():
        return {"status": "ok", "model_loaded": service is not None}, (200 if service is not None else 503)

    return app

app = create_app()
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
