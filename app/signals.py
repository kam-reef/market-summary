import pandas as pd


def moving_average(series, window):
    return series.rolling(window).mean()


def percent_change(series, days):
    if len(series) <= days:
        return float("nan")
    return (series.iloc[-1] / series.iloc[-days] - 1) * 100


def _latest_numeric(value):
    """
    Accepts:
    - float/int/str
    - pandas Series
    - pandas DataFrame with a 'close' column
    Returns latest float or None.
    """
    if value is None:
        return None

    if isinstance(value, (int, float)):
        return float(value)

    if isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            return None

    if isinstance(value, pd.Series):
        s = pd.to_numeric(value, errors="coerce").dropna()
        return float(s.iloc[-1]) if not s.empty else None

    if isinstance(value, pd.DataFrame):
        if "close" in value.columns:
            s = pd.to_numeric(value["close"], errors="coerce").dropna()
            return float(s.iloc[-1]) if not s.empty else None
        return None

    return None


def mortgage_signal(rate):
    if rate is None:
        return "Unknown"
    if rate < 5.75:
        return "Favorable"
    elif rate < 6.75:
        return "Neutral"
    else:
        return "Unfavorable"


def income_spread_signal(spread):
    # spread = SPDIVY - DGS10
    if spread is None:
        return "Unknown"
    if spread > 0.25:
        return "Equity Income Advantage"
    elif spread < -0.25:
        return "Bond Yield Advantage"
    return "Near Parity"


def compute_signals(data, macro_data):
    macro_data = macro_data or {}

    spy = data["SPY"].copy()
    qqq = data["QQQ"].copy()
    arkk = data["ARKK"].copy()
    vix = data["VIX"].copy()
    tnx = data["TNX"].copy()
    ovx = data["OVX"].copy()

    signals = {}
    snapshot = {}

    # Moving averages
    spy["ma200"] = moving_average(spy["close"], 200)
    qqq["ma100"] = moving_average(qqq["close"], 100)

    # Latest values
    spy_price = float(spy["close"].iloc[-1])
    spy_ma200 = float(spy["ma200"].iloc[-1]) if pd.notna(spy["ma200"].iloc[-1]) else float("nan")

    qqq_price = float(qqq["close"].iloc[-1])
    qqq_ma100 = float(qqq["ma100"].iloc[-1]) if pd.notna(qqq["ma100"].iloc[-1]) else float("nan")

    arkk_change = float(percent_change(arkk["close"], 63))

    vix_level = float(vix["close"].iloc[-1])
    tnx_level = float(tnx["close"].iloc[-1])
    ovx_level = float(ovx["close"].iloc[-1])

    mortgage_rate = _latest_numeric(macro_data.get("MORTGAGE30US"))
    mortgage_condition = mortgage_signal(mortgage_rate)

    sp_div_yield = _latest_numeric(macro_data.get("SPDIVY"))
    dgs10_macro = _latest_numeric(macro_data.get("DGS10"))
    ten_year_for_spread = dgs10_macro if dgs10_macro is not None else tnx_level

    income_spread = None
    if sp_div_yield is not None and ten_year_for_spread is not None:
        income_spread = sp_div_yield - ten_year_for_spread

    income_spread_regime = income_spread_signal(income_spread)

    # Core signals
    signals["SPY_below_200MA"] = bool(pd.notna(spy_ma200) and spy_price < spy_ma200)
    signals["SPY_above_200MA"] = bool(pd.notna(spy_ma200) and spy_price > spy_ma200)
    signals["QQQ_above_100MA"] = bool(pd.notna(qqq_ma100) and qqq_price > qqq_ma100)
    signals["ARKK_3mo_drop"] = bool(pd.notna(arkk_change) and arkk_change <= -15)
    signals["VIX_over_25"] = vix_level > 25
    signals["VIX_under_20"] = vix_level < 20

    # Macro signals
    signals["TNX_above_4"] = tnx_level > 4.0
    signals["TNX_below_3"] = tnx_level < 3.0
    signals["OVX_low"] = ovx_level < 60
    signals["OVX_high"] = ovx_level > 90
    signals["OVX_mid"] = 60 <= ovx_level <= 90

    # Mortgage regime
    signals["Mortgage_favorable"] = mortgage_rate is not None and mortgage_rate < 5.75
    signals["Mortgage_neutral"] = mortgage_rate is not None and 5.75 <= mortgage_rate < 6.75
    signals["Mortgage_unfavorable"] = mortgage_rate is not None and mortgage_rate >= 6.75

    # Income spread
    signals["IncomeSpread_positive"] = income_spread is not None and income_spread > 0
    signals["IncomeSpread_negative"] = income_spread is not None and income_spread < 0
    signals["IncomeSpread_near_parity"] = income_spread is not None and abs(income_spread) <= 0.25

    # Snapshot
    snapshot["SPY"] = {
        "price": round(spy_price, 2),
        "ma200": round(spy_ma200, 2) if pd.notna(spy_ma200) else None
    }

    snapshot["QQQ"] = {
        "price": round(qqq_price, 2),
        "ma100": round(qqq_ma100, 2) if pd.notna(qqq_ma100) else None
    }

    snapshot["ARKK"] = {
        "three_month_change_percent": round(arkk_change, 2) if pd.notna(arkk_change) else None
    }

    snapshot["VIX"] = {"level": round(vix_level, 2)}
    snapshot["TNX"] = {"yield": round(tnx_level, 2)}
    snapshot["OVX"] = {
        "level": round(ovx_level, 2),
        "regime": "low" if ovx_level < 60 else "high" if ovx_level > 90 else "mid"
    }

    snapshot["mortgage"] = {
        "rate": round(mortgage_rate, 2) if mortgage_rate is not None else None,
        "condition": mortgage_condition
    }

    snapshot["income_spread"] = {
        "sp_div_yield": round(sp_div_yield, 2) if sp_div_yield is not None else None,
        "ten_year_yield": round(ten_year_for_spread, 2) if ten_year_for_spread is not None else None,
        "spread": round(income_spread, 2) if income_spread is not None else None,
        "regime": income_spread_regime
    }

    return signals, snapshot