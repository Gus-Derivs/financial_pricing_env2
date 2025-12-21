import pandas as pd
from typing import Dict


class ZeroCouponCurve:
    """
    Bootstrapped zero-coupon curve from Treasury par yields
    """

    def __init__(self, tenors, discount_factors):
        self.tenors = tenors
        self.discount_factors = discount_factors

    def df(self, tenor: float) -> float:
        return self.discount_factors[tenor]


def load_treasury_par_curve(file_path: str,valuation_date: str) -> Dict[float, float]:
    """
    Load Treasury par yields for a given date
    Returns dict {tenor_in_years: par_rate_decimal}
    """
    df = pd.read_csv(file_path)
    df["Date"] = pd.to_datetime(df["Date"])

    row = df[df["Date"] == valuation_date]
    if row.empty:
        raise ValueError("Valuation date not found in data")

    row = row.iloc[0]

    tenor_map = {
        "1 Mo": 1/12,
        "3 Mo": 3/12,
        "6 Mo": 6/12,
        "1 Yr": 1,
        "2 Yr": 2,
        "5 Yr": 5,
        "10 Yr": 10,
        "30 Yr": 30
    }

    par_rates = {}
    for col, tenor in tenor_map.items():
        rate = row[col]
        if pd.notna(rate):
            par_rates[tenor] = rate / 100  # % → decimal

    return par_rates


def bootstrap_zero_curve(
    par_rates: Dict[float, float],
    frequency: int = 1
) -> ZeroCouponCurve:
    """
    Bootstrap discount factors from par rates
    Assumes annual coupons by default
    """
    tenors = sorted(par_rates.keys())
    dfs = {}

    for i, T in enumerate(tenors):
        c = par_rates[T] / frequency

        if i == 0:
            dfs[T] = 1 / (1 + c)
        else:
            pv_coupons = sum(
                c * dfs[t] for t in tenors[:i]
            )
            dfs[T] = (1 - pv_coupons) / (1 + c)

    return ZeroCouponCurve(tenors, dfs)
