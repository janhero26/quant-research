import sys
sys.path.append(".")

import pandas as pd
from metrics.performance import compute_metrics

def test_positive_cagr():
    # equity verdoppelt sich ueber 12 monate -> CAGR = 100%
    equity = pd.DataFrame({
        "date": pd.date_range("2020-01-31", periods=13, freq="ME"),
        "equity": [100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 195, 198, 200]
    })
    m = compute_metrics(equity)
    # nach 12 monaten von 100 auf 200 -> ungefaehr 100% CAGR
    assert m["cagr"] > 0.85
    assert m["cagr"] < 0.95

def test_drawdown_is_negative_or_zero():
    equity = pd.DataFrame({
        "date": pd.date_range("2020-01-31", periods=5, freq="ME"),
        "equity": [100, 120, 90, 110, 130]
    })
    m = compute_metrics(equity)
    # groesster drawdown war von 120 auf 90 = -25%
    assert m["max_drawdown"] < 0
    assert abs(m["max_drawdown"] - (-0.25)) < 0.01

def test_no_drawdown_when_only_rising():
    equity = pd.DataFrame({
        "date": pd.date_range("2020-01-31", periods=4, freq="ME"),
        "equity": [100, 110, 120, 130]
    })
    m = compute_metrics(equity)
    # nie gefallen -> drawdown = 0
    assert m["max_drawdown"] == 0