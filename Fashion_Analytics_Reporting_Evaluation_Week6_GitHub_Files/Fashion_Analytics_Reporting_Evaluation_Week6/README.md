# Fashion Analytics – Reporting, Evaluation and Presentation (Week 6)

**Internship:** Yuva Intern – Junior Data Analyst  
**Prepared by:** Sowmiya R

## Project overview
This project brings together the internship's fashion analytics workflow:

1. Data foundation and data quality checks (Week 5)
2. Weekly demand forecasting (Week 4)
3. Forecast evaluation using time-based validation and multiple metrics
4. Communicating results with clear visuals and business recommendations

The report describes a forecasting framework using a Seasonal Naive baseline, SARIMA or Prophet, and XGBoost, combined as a weighted ensemble.

## Key figures stated in the report
The report explicitly identifies these as **simulated demonstration results**, not results from a real company dataset:

- Data quality scores improved from 84–94% before cleaning to 97–100% after cleaning across the displayed dimensions.
- Ensemble WAPE: 15.6%; Seasonal Naive baseline WAPE: 27.5%.
- SARIMA/Prophet WAPE: 19.8%; XGBoost WAPE: 17.2%.
- The report describes the ensemble error as roughly 43% lower than the baseline.

Do not present these values as independently reproduced results. They are copied from the supplied Week 6 report and are illustrative.

## Repository structure

```text
Fashion-Analytics-Reporting-Evaluation-Week6/
├── README.md
├── requirements.txt
├── .gitignore
├── Week6_Final_Report_Fashion_Analytics.doc
├── src/
│   └── evaluate_forecasts.py
├── data/
│   └── README.md
└── outputs/
    └── README.md
```

## Setup

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

## Run the evaluation script

Prepare a CSV file with these columns:

- `actual`: actual weekly units sold
- `seasonal_naive`: baseline forecast
- `sarima_prophet`: SARIMA or Prophet forecast
- `xgboost`: XGBoost forecast
- `ensemble`: combined forecast

Then run:

```bash
python src/evaluate_forecasts.py data/forecast_evaluation.csv
```

The script reports WAPE, MAE, RMSE, MAPE (excluding zero actuals), and forecast bias for each model. It does not train forecasting models; it evaluates forecast columns supplied in the CSV.

## Evaluation approach
The report recommends:
- Time-based holdout of the most recent 12–13 weeks
- Walk-forward (rolling-origin) validation
- Comparison against a Seasonal Naive benchmark
- Residual and bias checks
- Segment-level evaluation by category, region and season
- Translating forecast errors into business impact

## Notes and limitations
- The supplied report's charts and figures use simulated data.
- No real business dataset is included in this repository.
- Model scores from a real dataset must be calculated separately and validated before operational use.
