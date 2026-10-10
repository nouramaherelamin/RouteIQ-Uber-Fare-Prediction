# Uber Fare — Interactive Analytics Dashboard

This is a separate Streamlit analytics app based on the user's supplied `app.py` example. It complements (does not replace) the existing Flask RouteIQ prediction app.

## Features

- Overview KPIs and demand/fare summaries
- Fare distribution and hourly fare analysis
- Demand-by-hour exploration
- Passenger, car-condition and traffic comparisons
- Distance, weather and airport-distance exploration
- Correlation explorer and numerical heatmap
- Searchable data explorer with CSV download
- Data-quality cards
- Global interactive filters for hour, car condition, weather, traffic, passenger count, year and month
- Dark dashboard styling, Plotly charts, responsive layout, and the author's LinkedIn/GitHub footer

## Dataset lookup order

The app uses the first existing file in this order:

1. `interactive_dashboard/uber_fare_eda_clean.csv`
2. `data/processed/uber_fare_eda_clean.csv`
3. `data/raw/sample_50000.csv`

The final path points to the existing project sample, so no duplicate dataset is required. Non-positive fares are excluded for fare analytics. If the source coordinate/bearing columns are in radians, the app converts them to degrees for human-readable exploration. The app is descriptive only and does not train a model or change saved model artifacts.

## Run on Windows

From the `analytics_project` directory:

```powershell
py -m pip install -r interactive_dashboard/requirements.txt
py -m streamlit run interactive_dashboard/app.py
```

If `py` is unavailable, use `python` in both commands.

## Important distinction

- `routeiq_web_app/`: Flask prediction interface and map picker.
- `analytics_project/interactive_dashboard/`: Streamlit interactive EDA dashboard.

These apps have separate purposes and can run independently.


### Dependency repair
If Streamlit shows `cannot import name lazy_df_adapters`, reinstall the dashboard dependencies in the project virtual environment:

```powershell
python -m pip install --force-reinstall -r analytics_project/interactive_dashboard/requirements.txt
```

The dashboard uses the mint/cyan/charcoal palette and a bundled car visual (`assets/taxi.png`).


### Theme update
The dashboard uses a standalone neon-mint/cyan car asset and a restrained charcoal/forest-green palette. Install the pinned dashboard dependencies inside the project virtual environment before launch.


## Approved visual theme — Executive Emerald

The dashboard uses Deep Black `#05090B`, Dark Panel `#0D1519`, Mint Green `#2FE6B3`, Electric Cyan `#35C7E8`, Mint Glow `#8FFFC5`, Panel Border `#24434A`, Primary Text `#F2F5F6`, Secondary Text `#9AAAB4`, and Muted Teal `#164B4A`. Existing analytics pages and filter logic are retained.


## Approved visual theme

The dashboard uses the **Neon Luxury** direction: deep-black and charcoal panels, mint-green and electric-cyan accents, restrained neon borders, a wide cinematic hero layout with the existing car asset, and balanced KPI/chart spacing. All analytics pages and global filters remain in place. Use the project virtual environment when launching Streamlit so the pinned runtime is used.
