"""Evaluate supplied weekly forecast columns against actual demand.

Usage:
    python src/evaluate_forecasts.py data/forecast_evaluation.csv

Required columns:
    actual, seasonal_naive, sarima_prophet, xgboost, ensemble
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

MODEL_COLUMNS = ["seasonal_naive", "sarima_prophet", "xgboost", "ensemble"]


def calculate_metrics(actual: pd.Series, forecast: pd.Series) -> dict[str, float]:
    errors = forecast - actual
    denominator = actual.abs().sum()
    nonzero = actual != 0

    return {
        "MAE": float(errors.abs().mean()),
        "RMSE": float(np.sqrt(np.mean(np.square(errors)))),
        "WAPE_percent": float(errors.abs().sum() / denominator * 100) if denominator else float("nan"),
        "MAPE_percent": float((errors[nonzero].abs() / actual[nonzero].abs()).mean() * 100)
        if nonzero.any() else float("nan"),
        "Bias_units": float(errors.mean()),
    }


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python src/evaluate_forecasts.py <path-to-csv>")
        return 2

    input_path = Path(sys.argv[1])
    if not input_path.exists():
        print(f"Input file not found: {input_path}")
        return 2

    frame = pd.read_csv(input_path)
    required = ["actual", *MODEL_COLUMNS]
    missing = [column for column in required if column not in frame.columns]
    if missing:
        print("Missing required columns:", ", ".join(missing))
        return 2

    frame = frame[required].apply(pd.to_numeric, errors="coerce").dropna()
    if frame.empty:
        print("No complete numeric rows available for evaluation.")
        return 2

    actual = frame["actual"]
    results = {
        model: calculate_metrics(actual, frame[model])
        for model in MODEL_COLUMNS
    }
    result_frame = pd.DataFrame(results).T
    result_frame.index.name = "Model"
    print(result_frame.round(3).to_string())

    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / "forecast_evaluation_metrics.csv"
    result_frame.to_csv(output_path)
    print(f"\nSaved metrics to: {output_path}")
    print("Reminder: evaluate on a time-based holdout; do not randomly shuffle time-series rows.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
