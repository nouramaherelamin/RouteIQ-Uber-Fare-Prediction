<div align="center">

# 🚕 RouteIQ
### Uber Fare Prediction & Interactive Analytics

**Explore trip patterns. Understand fare drivers. Estimate ride fares.**

<p>
  <a href="https://nouramaherelamin-route-iq-uber-fare-prediction.vercel.app/">
    <img src="https://img.shields.io/badge/🚘%20Live%20Fare%20Prediction-Open%20App-85FFC2?style=for-the-badge&labelColor=151918" alt="Open RouteIQ Fare Prediction">
  </a>
  <a href="https://nouramaherelamin-uber-fare-prediction-dashboard.streamlit.app/">
    <img src="https://img.shields.io/badge/📊%20Live%20Analytics-Open%20Dashboard-22D3EE?style=for-the-badge&labelColor=151918" alt="Open Analytics Dashboard">
  </a>
</p>

<p>
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flask-Web%20App-000000?style=flat-square&logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/Streamlit-Analytics-FF4B4B?style=flat-square&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/scikit--learn-Machine%20Learning-F7931E?style=flat-square&logo=scikitlearn&logoColor=white" alt="scikit-learn">
  <img src="https://img.shields.io/badge/Plotly-Interactive%20Charts-3F4F75?style=flat-square&logo=plotly&logoColor=white" alt="Plotly">
</p>

*A data analytics and machine learning project for exploring Uber fare patterns and estimating trip fares using trip details and engineered geographic features.*

</div>

---

## 🧭 Quick Navigation

- [Project Overview](#-project-overview)
- [Live Applications](#-live-applications)
- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Dataset & Modeling](#-dataset--modeling)
- [Model Results](#-model-results)
- [Run Locally](#-run-locally)
- [Tests & Training](#-tests--training)
- [Troubleshooting](#-troubleshooting)
- [Limitations](#-limitations)
- [Author](#-author)

---

## 🧭 Project Overview

RouteIQ explores NYC Uber trip data and predicts a trip's fare using
trip details such as pickup/drop-off coordinates, trip distance, pickup
time, passenger count, and other engineered features.

The project has two separate user-facing applications:

1.  **RouteIQ Fare Prediction** --- a Flask web app for entering trip
    details and requesting an estimated fare.
2.  **Uber Fare EDA / Interactive Analytics** --- a Streamlit dashboard
    for exploring fare distributions, demand patterns, distance,
    passengers, weather/car/traffic fields, airport-related fields,
    correlations, and data quality.

They run as separate local services, but provide navigation links to
move between them. Keep the analytics dashboard, Flask app, training
code, tests, data, and notebooks as separate components; each has a
different purpose.

## 🚀 Live Applications

| Application | What it does | Open |
|---|---|---|
| **RouteIQ Fare Prediction** | Flask-based trip interface with pickup/drop-off selection and fare estimation. | [**Launch Predictor ↗**](https://nouramaherelamin-route-iq-uber-fare-prediction.vercel.app/) |
| **Uber Fare Analytics** | Streamlit dashboard for exploring fare distributions, trip patterns, relationships, and data quality. | [**Launch Dashboard ↗**](https://nouramaherelamin-uber-fare-prediction-dashboard.streamlit.app/) |

> **Note:** These are two separately deployed applications. The links connect the two experiences, but they do not run inside one shared server.

## 🧩 Main Applications

### 1. RouteIQ Fare Prediction (Flask)

-   Interactive trip input and fare prediction.
-   Map-oriented pickup/drop-off selection where supported by the
    current app.
-   Uses the trained model artifact when it is available and configured.
-   Runs locally at `http://127.0.0.1:5000`.

### 2. Uber Fare EDA --- Interactive Analytics (Streamlit)

-   Dark automotive-inspired interface with neon mint and cyan accents.
-   Interactive sidebar filters; charts update to reflect the selected
    data.
-   Overview KPIs and dedicated analysis sections.
-   Data explorer and data-quality inspection.
-   Runs locally at `http://localhost:8501`.

## ✨ Features

### Analytics Dashboard

-   Overview of filtered trips, average/median fare, and
    distance/passenger metrics where available.
-   Fare distribution and fare comparisons by time.
-   Demand analysis by hour and weekday.
-   Passenger analysis.
-   Car and traffic analysis.
-   Distance analysis.
-   Weather analysis.
-   Airport-related analysis.
-   Correlation explorer.
-   Data explorer with downloadable filtered data (if enabled in the
    current version).
-   Data-quality summary.
-   Shared filters and a reset-filters control.
-   CSS transitions and hover effects for dashboard components where
    supported by the current version.

### Machine Learning

-   Data cleaning and feature engineering.
-   Haversine distance feature.
-   Train/test split with a fixed random seed in the documented
    workflow.
-   Preprocessing and model evaluation.
-   Comparison of multiple regression models.
-   Model serialization for application use.

## 🛠️ Technology Stack

| Tool | Role |
|---|---|
| **Python** | Main language |
| **pandas / NumPy / SciPy** | Data preparation, analysis, and numerical operations |
| **scikit-learn** | Feature engineering, regression, and model evaluation |
| **Plotly** | Interactive visualizations |
| **Flask** | Fare prediction web application |
| **Streamlit** | Interactive analytics dashboard |
| **joblib** | Saving and loading the trained model |
| **Jupyter** | EDA and modeling notebooks |
| **pytest** | Automated tests |

## 📁 Project Structure

The exact structure can vary slightly between project revisions. The
main folders are expected to resemble:

``` text
RouteIQ_Uber_Fare_Prediction_Final/
├── README_FINAL.md
├── requirements.txt
├── .venv/                              # Local virtual environment (created by you)
├── routeiq_web_app/                    # Flask prediction app
├── analytics_project/
│   ├── data/
│   │   ├── raw/                        # Original CSV dataset
│   │   └── processed/                  # Cleaned/processed datasets
│   ├── notebooks/                      # Project notebooks
│   ├── src/
│   │   └── uber_fare/
│   │       ├── features.py
│   │       ├── validation.py
│   │       └── train.py
│   ├── tests/
│   │   ├── test_features.py
│   │   └── test_validation.py
│   └── interactive_dashboard/
│       ├── app.py                      # Streamlit dashboard
│       ├── requirements.txt            # Dashboard dependencies
│       └── assets/
│           └── taxi.png                # Taxi/car image asset
└── ...
```

If a folder or notebook has a different name in your downloaded
revision, use the actual filename present in that revision.

## 🗂️ Dataset & Data Quality

The working sample referenced in the project is `sample_50000.csv` with
50,000 rows and 26 columns. The exact fields available to a particular
dashboard section depend on the CSV version loaded.

The workflow has accounted for the following data-quality observations
in the analyzed sample:

-   50,000 source rows.
-   9 non-positive fare records were excluded from the EDA dashboard
    view, leaving 49,991 positive-fare rows.
-   Coordinate and bearing fields may be stored in radians in the source
    and need consistent conversion before they are treated as degrees.
-   Repeated `key` values are not necessarily duplicate trips and should
    not be deduplicated solely on that field.
-   Invalid coordinates should be handled using a documented,
    deterministic cleaning rule.
-   Distance and airport-distance features should be recomputed from
    cleaned coordinates if they are used for modeling.

Place the CSV in the location expected by the version you are running.
The dashboard checks its configured candidate paths, typically
including:

-   `analytics_project/interactive_dashboard/uber_fare_eda_clean.csv`
-   `analytics_project/data/processed/uber_fare_eda_clean.csv`
-   `analytics_project/data/raw/sample_50000.csv`

## 🤖 Machine Learning Workflow

1.  Load and inspect the source data.
2.  Clean invalid target values and invalid trip records using the
    project's documented rules.
3.  Create engineered trip features, including geographic distance where
    applicable.
4.  Split the data into training and test partitions before fitting
    learned preprocessing.
5.  Fit preprocessing and model steps using training data only.
6.  Compare candidate regression models using cross-validation on
    training data.
7.  Evaluate the selected model on the held-out test set.
8.  Save the fitted model pipeline and metadata for use by the
    prediction app.
9.  Validate input data in the web app before requesting predictions.

The model should be retrained from the project's training module when
the dataset, features, or model configuration changes. Do not use
test-set results to tune the model.

## 📈 Model Results

The following are results reported by a prior local training run; they
are included as reference values, not a guarantee that a new run will
reproduce them exactly.

| Model | Test MAE | Test RMSE | Test R² |
|---|---:|---:|---:|
| Hist Gradient Boosting | 1.7535 | 3.7394 | 0.8434 |
| Random Forest | 1.8294 | 3.7406 | 0.8433 |
| Tuned Random Forest | 1.8186 | 3.7563 | 0.8420 |
| Ridge Regression | 2.2395 | 4.4382 | 0.7794 |
| Decision Tree | 2.2210 | 4.4619 | 0.7770 |

-   **MAE**: average absolute fare prediction error, in the target fare
    units (dollars for the referenced run).
-   **RMSE**: penalizes larger prediction errors more heavily.
-   **R²**: proportion of target variance explained by the model.

A chronological evaluation was also reported for training on 2009--2014
and testing on 2015: MAE ≈ 1.9634, RMSE ≈ 3.8115, R² ≈ 0.8744. Use the
latest output from your own run for formal reporting.

## 💻 Run Locally

### 1. Open the project folder

Extract the ZIP, then open PowerShell in the project root:

``` powershell
cd C:\Users\noura\RouteIQ_Uber_Fare_Prediction_Final
```

Change the path if you extracted the project elsewhere.

### 2. Create and activate a virtual environment

``` powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation for this terminal session, run:

``` powershell
Set-ExecutionPolicy -Scope Process Bypass
.\.venv\Scripts\Activate.ps1
```

### 3. Install the main dependencies

``` powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Install the dashboard dependencies

The Streamlit dashboard has its own dependency file:

``` powershell
python -m pip install -r analytics_project/interactive_dashboard/requirements.txt
```

The `streamlit` package must be installed into the same Python
environment used to launch the dashboard. If `python -m streamlit` says
`No module named streamlit`, install the dashboard requirements while
the project's `.venv` is activated.

## ▶️ Start the Applications

Run the two applications in **separate PowerShell terminals**. Activate
`.venv` in each terminal if needed.

### Terminal 1 --- Flask prediction app

From the project root:

``` powershell
python -m flask --app routeiq_web_app.app run --debug
```

Open: **http://127.0.0.1:5000**

### Terminal 2 --- Streamlit analytics dashboard

From the project root:

``` powershell
python -m streamlit run analytics_project/interactive_dashboard/app.py
```

Open: **http://localhost:8501**

### Move between the apps

Use the navigation link in the dashboard to open RouteIQ Predictor, and
the analytics link in the Flask app to return to the dashboard. Both
local servers must be running for cross-navigation to work. The links
open the other app in a separate browser tab; they do not merge the two
frameworks into one server.

## 🧪 Tests

From the project root with the virtual environment active:

``` powershell
python -m pytest -q
```

A previously reported run completed with `7 passed`. Run the tests again
after making changes and use the output from your own machine as the
current status.

## 🔁 Retrain the Model

From the project root:

``` powershell
cd analytics_project
python -m src.uber_fare.train
```

Return to the project root afterwards:

``` powershell
cd ..
```

The training process prints cleaning counts,
cross-validation/model-comparison metrics, selected model parameters,
and chronological evaluation metrics. It may take a while, especially
for Random Forest cross-validation.

## 📓 Jupyter Notebooks

The project includes notebooks for exploration and modeling. Open them
using Jupyter from the project environment:

``` powershell
python -m jupyter lab
```

or:

``` powershell
python -m jupyter notebook
```

Then open the notebook from the project's `analytics_project/notebooks/`
folder (or the notebook folder included in your downloaded version). Run
cells in order, especially where later cells depend on data cleaning or
engineered features from earlier cells.

## 🧰 Troubleshooting

### `Could not open requirements.txt`

Make sure PowerShell is in the project root and that the file exists
there. For the dashboard-specific requirements, use the full relative
path:

``` powershell
python -m pip install -r analytics_project/interactive_dashboard/requirements.txt
```

### `ModuleNotFoundError: No module named 'streamlit'`

``` powershell
python -m pip install -r analytics_project/interactive_dashboard/requirements.txt
python -m streamlit run analytics_project/interactive_dashboard/app.py
```

### `ModuleNotFoundError: No module named 'src'` when collecting tests

Run tests from the project root, not from an unrelated folder:

``` powershell
python -m pytest -q
```

If the error persists, verify the package layout under
`analytics_project/src/uber_fare/` and use the project's intended
environment.

### Streamlit dataframe import error (`lazy_df_adapters`)

This indicates an incompatible or incomplete Streamlit installation.
With the project virtual environment activated, reinstall the dashboard
requirements:

``` powershell
python -m pip install --force-reinstall -r analytics_project/interactive_dashboard/requirements.txt
```

Then restart Streamlit. If it persists, inspect the installed version
with:

``` powershell
python -m pip show streamlit
```

### The dashboard cannot find the CSV

Check that the CSV exists in one of the configured candidate paths
listed in the [Dataset](#dataset) section. Confirm the column names
match the data version used by the app.

### Port already in use

Stop the existing process with `Ctrl+C`, or configure a different port.
For Streamlit, for example:

``` powershell
python -m streamlit run analytics_project/interactive_dashboard/app.py --server.port 8502
```

## ⚠️ Limitations & Notes

-   Flask and Streamlit are local development servers, not production
    deployment servers.
-   The prediction app requires the correct trained model artifact and
    compatible input schema.
-   Dashboard charts depend on the columns present in the loaded
    dataset.
-   Visual effects vary by browser and Streamlit version.
-   Model metrics are historical run outputs; rerun training to produce
    updated results.
-   Never commit secrets, virtual environments, cache folders, or
    private datasets to a public repository unless they are intended to
    be shared.

# Author
<div align="center">
  
**Noura Maher Elamin**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Profile-0A66C2?style=for-the-badge\&logo=linkedin\&logoColor=white)](https://www.linkedin.com/in/nouramaherelamin/)
[![GitHub](https://img.shields.io/badge/GitHub-Profile-181717?style=for-the-badge\&logo=github\&logoColor=white)](https://github.com/nouramaherelamin)

---

**RouteIQ** · Uber Fare Prediction & Interactive Analytics</div>
